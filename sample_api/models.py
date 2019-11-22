from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('Category', blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
