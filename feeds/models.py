from django.db import models


class Item(models.Model):
    title = models.CharField(verbose_name="Title", max_length=200)
    description = models.TextField(verbose_name="Description")
    link = models.URLField(verbose_name="Link")
    comments = models.URLField(verbose_name="Comments Link")
    pub_date = models.DateTimeField(
        verbose_name="Published Date", null=True, blank=True)
    guid = models.IntegerField(verbose_name="GUID", default=0)

    class Meta:
        db_table = "feeds_items"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    title = models.CharField(verbose_name="Category",
                             max_length=50, unique=True)
    items = models.ManyToManyField(Item, related_name="categories")

    class Meta:
        db_table = "feeds_categories"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.title}"
