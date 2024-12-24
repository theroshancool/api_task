from django.db import models


class App(models.Model):
    app_name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.app_name} ({self.version})"

    def to_dict(self):
        return {
            "id": self.id,
            "app_name": self.app_name,
            "version": self.version,
            "description": self.description,
        }
