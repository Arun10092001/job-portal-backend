from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    salary_range = models.CharField(max_length=15, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Applications(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'ShortListed'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired')
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicants = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)
