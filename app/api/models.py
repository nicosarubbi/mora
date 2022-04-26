import json
from django.db import models


class Database(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.name}"



class Resource(models.Model):
    name = models.CharField(max_length=40)
    resource_name = models.CharField(max_length=40)
    pk_name = models.CharField(max_length=40)
    database = models.ForeignKey(Database, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}: {self.name}"


class Item(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    data = models.JSONField(default={})

    def __str__(self):
        data = self.data.copy()
        data['id'] = self.pk
        return json.dumps(data)
