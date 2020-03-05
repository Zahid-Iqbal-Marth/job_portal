from django.db import models
from django.contrib.auth.models import User
from user.models import Customer,Resume
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class job(models.Model):
    job_title = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    discription = models.TextField()
    company_name = models.CharField(max_length=30)
    company_logo = models.ImageField(default='default.jpg',upload_to='company_logo')
    website_url = models.URLField()
    post_date = models.DateField(default=timezone.now)

    job_poster = models.ForeignKey(Customer,on_delete=models.CASCADE)
    applications = models.ManyToManyField(Resume)

    def __str__(self):
        return self.job_title
    
    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})
class Package(models.Model):
    package_type=models.CharField(max_length=30,default='')
    price= models.IntegerField(default=0)
    job_posting_limit=models.IntegerField(default=0)
    resume_view_limit=models.IntegerField(default=0)
    job_posted_time=models.IntegerField(default=0)