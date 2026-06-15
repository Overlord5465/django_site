from pathlib import Path

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True, db_index=True)
    attachment = models.FileField(upload_to="chat_attachments/", blank=True, null=True)

    @property
    def attachment_basename(self) -> str:
        """Имя файла с расширением для отображения в чате."""
        if not self.attachment:
            return ""
        return Path(self.attachment.name).name

    class Meta:
        ordering = ('timestamp',)
        indexes = [
            models.Index(fields=["sender", "recipient", "timestamp"]),
        ]

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.content[:20]}..."