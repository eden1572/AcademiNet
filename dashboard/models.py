from django.db import models

class DashboardLink(models.Model):
    name = models.CharField(max_length=100, default="Default Name")
    url = models.URLField(default="https://example.com")

    class Meta:
        verbose_name_plural = "Dashboard Links"

    def __str__(self):
        return self.name
