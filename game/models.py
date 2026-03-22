
from django.db import models

class Texts(models.Model):
    stage_tag = models.CharField(max_length=50)
    order = models.IntegerField()
    content = models.TextField()
    
    def __str__(self):
        return f"[{self.stage_tag}] {self.order}: {self.content[:10]}"


