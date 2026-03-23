from django.db import models

class Texts(models.Model):
    stage_tag = models.CharField(max_length=50)
    order = models.IntegerField()
    content = models.TextField()
    
    def __str__(self):
        return f"[{self.stage_tag}] {self.order}: {self.content[:10]}"

class GatekeeperFlag(models.Model):
    flag = models.BooleanField()
    
    def __str__(self):
        return f"flag is {self.flag}"
    
class MinisterFlags(models.Model):
    flag = models.BooleanField()
    
    def __str__(self):
        return f"flag{self.id} is {self.flag}"