from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Kpi(models.Model):
    date = models.DateField(auto_now_add=True)
    weeks = models.PositiveIntegerField()
    activity = models.CharField(max_length=255)
    kpi = models.CharField(max_length=255)
    baseline = models.DecimalField(max_digits=10, decimal_places=2)
    plan = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.kpi} - On Week {self.weeks}"




class KpiDetails(models.Model):
    kpi = models.ForeignKey(Kpi, on_delete=models.CASCADE, related_name='details')
    progress = models.FloatField()
    achievement = models.FloatField(blank=True, null=True)  # ✅ no default, set in save()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.kpi.plan:
            self.achievement = (self.progress / float(self.kpi.plan)) * 100
        else:
            self.achievement = 0
        super().save(*args, **kwargs)