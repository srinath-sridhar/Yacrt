from django.db import models
from django.contrib.auth.models import Group, User


class Repository(models.Model):
    repo_name = models.CharField(max_length=100)
    repo_description = models.CharField(max_length=200)
    repo_url = models.CharField(max_length=200)
    repo_access_group = models.ForeignKey(Group)
    repo_vc_system = models.CharField(max_length=15)
    repo_created_by = models.ForeignKey(User)
    