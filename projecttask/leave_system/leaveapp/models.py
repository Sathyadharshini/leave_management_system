from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Leave(models.Model):
    LEAVE_TYPES = [
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Earned', 'Earned'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    leave_balance = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    from .models import EmployeeProfile

    if created:
        # Only create profile for non-superusers
        if not instance.is_superuser:
            EmployeeProfile.objects.create(user=instance)
    else:
        try:
            instance.employeeprofile.save()
        except EmployeeProfile.DoesNotExist:
            pass  # Avoid crashing if user has no profile




