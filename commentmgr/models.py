from django.db import models
from repobrowser.models import Repository
from django.contrib.auth.models import User


class Comment(models.Model):
    user = models.ForeignKey(User)
    repo_id = models.ForeignKey(Repository)
    repo_revision = models.IntegerField()
    file_path = models.CharField(max_length=500)
    line_number = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField()