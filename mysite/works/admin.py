from django.contrib import admin

from users.department_admin_access import DepartmentAdminFullAccessMixin

from works.models import (
    IndividualPlan,
    Notification,
    PlanStage,
    StudentTopicProposal,
    Tag,
    Topic,
    TopicApplication,
    Work,
)


@admin.register(Work)
class WorkAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ("name", "author", "scientific_director", "status", "created_at")


class TopicAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    pass


class TopicApplicationAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    pass


class StudentTopicProposalAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    pass


class TagAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    pass


class NotificationAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    pass


class IndividualPlanAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    pass


class PlanStageAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    pass


admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicApplication, TopicApplicationAdmin)
admin.site.register(StudentTopicProposal, StudentTopicProposalAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(IndividualPlan, IndividualPlanAdmin)
admin.site.register(PlanStage, PlanStageAdmin)
