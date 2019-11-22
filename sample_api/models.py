from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('Category', blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    def parents(self):
        parents = []
        if self.parent is not None:
            parents.append(self.parent)
            parents += self.parent.parents()
        return parents

    def siblings(self):
        return Category.objects.filter(parent=self.parent).exclude(pk=self.pk)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
