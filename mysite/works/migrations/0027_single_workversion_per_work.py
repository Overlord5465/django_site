from __future__ import annotations

                                      

from django.db import migrations, models


def dedupe_workversions(apps, schema_editor):
    """
    Before adding a UNIQUE(work) constraint, ensure there is at most one
    WorkVersion per Work.

    We keep the latest by uploaded_at, with id as a tiebreaker.
    """

    WorkVersion = apps.get_model("works", "WorkVersion")

                                   
    dup_work_ids = (
        WorkVersion.objects.values_list("work_id", flat=True)
        .order_by()
        .annotate(cnt=models.Count("id"))
        .filter(cnt__gt=1)
    )

    for work_id in dup_work_ids.iterator():
        keep = (
            WorkVersion.objects.filter(work_id=work_id)
            .order_by("-uploaded_at", "-id")
            .first()
        )
        if not keep:
            continue
        WorkVersion.objects.filter(work_id=work_id).exclude(id=keep.id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0026_remove_workversion_review"),
    ]

    operations = [
        migrations.RunPython(dedupe_workversions, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="workversion",
            constraint=models.UniqueConstraint(fields=("work",), name="uniq_single_version_per_work"),
        ),
    ]

