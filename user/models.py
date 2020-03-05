from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE = [
        ('EM','Employer'),
        ('CN', 'Candidate'),
        ('NN', 'None'),
    ]
    Type = models.CharField(
    max_length=2,
    choices=TYPE,
    default='NN'
    )
    country=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    zip_code=models.CharField(max_length=10,null=True)
    phone=models.CharField(max_length=20,null=True)
    form_completed=models.BooleanField(default=False) # this field checks if form is completed or not 

    def __str__(self):
        return "%s %s" % (self.user, self.Type)

class Resume(models.Model):
    profession_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_pics')
    resume_content = models.CharField(max_length=500)
    name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return "%s %s" % (self.name, self.profession_title)


class Education(models.Model):
    school_name = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)
    start_end_date = models.CharField(max_length=100)
    notes = models.CharField(max_length=300)
    name=models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.name, self.school_name)

class Experience(models.Model):
    employer = models.CharField(max_length=100)
    job_title = models.CharField(max_length=50)
    start_end_date = models.CharField(max_length=100)
    notes = models.CharField(max_length=300)
    name=models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.name, self.job_title)
class UserSubscription(models.Model):
    package_id=models.IntegerField(null=True)
    paid_count=models.IntegerField(default=0)
    sub_date=models.DateField(null=True)
    stripe_cust_id=models.CharField(max_length=200)
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    sub_status=models.CharField(max_length=100)# UserSubscription status