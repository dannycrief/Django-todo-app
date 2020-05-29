from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def allthr():
    for tc in TodoItem.category.through.objects.all():
        print("[%3d]  %d -item|cat- %d  ::  %s @ %s" %
              (tc.id, tc.todoitem_id, tc.category_id,
               TodoItem.objects.get(id=tc.todoitem_id),
               Category.objects.get(id=tc.category_id)))


class Category(models.Model):
    slug = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    todo_count = models.PositiveIntegerField(default=0)

    high_priority = models.PositiveIntegerField(default=0)
    medium_priority = models.PositiveIntegerField(default=0)
    low_priority = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return f'{self.name} ({self.slug})'


class TodoItem(models.Model):
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3

    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, "High priority"),
        (PRIORITY_MEDIUM, "Medium priority"),
        (PRIORITY_LOW, "Low priority"),
    ]

    description = models.TextField("Description")
    is_completed = models.BooleanField("Done", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    priority = models.IntegerField(
        "Priority", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])
