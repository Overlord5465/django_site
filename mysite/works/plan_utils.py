from __future__ import annotations

from django.db.models import Max

from works.models import IndividualPlan, PlanStage


DEFAULT_ROOT_TITLES = (
    "Содержание",
    "Теоретическая часть",
    "Практическая часть",
    "Оформление (нормы по методичке)",
)


def leaf_stages_queryset(plan: IndividualPlan):
    """Пункты без подпунктов — по ним считается прогресс."""
    parent_ids = set(
        plan.stages.exclude(parent_id__isnull=True).values_list("parent_id", flat=True)
    )
    return plan.stages.exclude(id__in=parent_ids)


def plan_progress_percent(plan: IndividualPlan) -> tuple[int, int, int]:
    """Возвращает (процент, выполнено листьев, всего листьев)."""
    leaves = leaf_stages_queryset(plan)
    total = leaves.count()
    if not total:
        return 0, 0, 0
    done = leaves.filter(is_done=True).count()
    pct = int(round(done / total * 100))
    return pct, done, total


def flatten_plan_stages(plan: IndividualPlan) -> list[tuple[PlanStage, int]]:
    """DFS: список (этап, глубина) для отображения дерева."""
    if not plan:
        return []
    stages = list(plan.stages.all().order_by("order", "id"))
    by_parent: dict[int | None, list[PlanStage]] = {}
    for s in stages:
        by_parent.setdefault(s.parent_id, []).append(s)
    out: list[tuple[PlanStage, int]] = []

    def walk(node: PlanStage, depth: int) -> None:
        out.append((node, depth))
        for ch in by_parent.get(node.id, []):
            walk(ch, depth + 1)

    for r in by_parent.get(None, []):
        walk(r, 0)
    return out


def seed_default_stages(plan: IndividualPlan) -> None:
    if plan.stages.exists():
        return
    mx = plan.stages.aggregate(m=Max("order"))["m"] or -1
    for i, title in enumerate(DEFAULT_ROOT_TITLES):
        PlanStage.objects.create(
            plan=plan,
            parent=None,
            title=title,
            order=mx + 1 + i,
        )


def reconcile_parent_done(stage: PlanStage) -> None:
    """После выполнения подпункта поднимаемся вверх и помечаем родителей, если все дети выполнены."""
    from django.utils import timezone

    p = stage.parent
    while p:
        siblings = list(p.children.all())
        if not all(s.is_done for s in siblings):
            break
        if not p.is_done:
            p.is_done = True
            p.done_at = timezone.now()
            p.save(update_fields=["is_done", "done_at"])
        p = p.parent
