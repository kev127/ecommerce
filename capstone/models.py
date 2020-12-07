from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class RecentWork(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media")

    def __str__(self):
        return self.title
