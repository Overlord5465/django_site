                                      

from __future__ import annotations

from django.db import migrations, models


def copy_latest_docx_from_versions(apps, schema_editor):
    Work = apps.get_model("works", "Work")
    WorkVersion = apps.get_model("works", "WorkVersion")

    for w in Work.objects.all().iterator():
                                                      
        latest_docx = None
        latest_any = None
        for v in WorkVersion.objects.filter(work_id=w.id).order_by("-uploaded_at"):
            if latest_any is None:
                latest_any = v
            name = (getattr(v, "file", None).name or "").lower() if getattr(v, "file", None) else ""
            if name.endswith(".docx"):
                latest_docx = v
                break
        v = latest_docx or latest_any
        if not v or not getattr(v, "file", None):
            continue

                                                                                
        w.docx_file = v.file
        w.docx_uploaded_at = v.uploaded_at
        w.docx_uploaded_by_id = v.uploaded_by_id
        w.docx_comment = v.comment or ""
        w.docx_is_final = bool(v.is_final)
        w.save(
            update_fields=[
                "docx_file",
                "docx_uploaded_at",
                "docx_uploaded_by",
                "docx_comment",
                "docx_is_final",
            ]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0028_remove_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="docx_file",
            field=models.FileField(blank=True, null=True, upload_to="work_docs/"),
        ),
        migrations.AddField(
            model_name="work",
            name="docx_uploaded_at",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="work",
            name="docx_uploaded_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="uploaded_work_docx",
                to="accounts.user",
            ),
        ),
        migrations.AddField(
            model_name="work",
            name="docx_comment",
            field=models.CharField(blank=True, default="", max_length=300),
        ),
        migrations.AddField(
            model_name="work",
            name="docx_is_final",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.RunPython(copy_latest_docx_from_versions, migrations.RunPython.noop),
        migrations.DeleteModel(name="WorkVersion"),
    ]

