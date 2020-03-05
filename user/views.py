from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer,Resume,Education,Experience,UserSubscription
from .forms import UserRegisterForm, AddResumeForm, UpdateResume,UpdateExprience,UpdateEducation,UserUpdateForm,ProfileUpdateForm
# Create your views here.
from django.contrib.auth.models import User
from job.models import job

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cust , created= User.objects.get_or_create(username=form.cleaned_data['username'],email=form.cleaned_data['email'])
            Customer.objects.create(user=cust,Type=form.cleaned_data['Type'])
            cust.set_password(form.cleaned_data['password'])
            cust.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def AddResume(request):
    if request.user.customer.Type == 'CN':
        if request.method == 'POST':
            form = AddResumeForm(request.POST,request.FILES)
            if form.is_valid():
                resume = Resume.objects.create( profession_title=form.cleaned_data['profession_title'],
                                                location=form.cleaned_data['location'],
                                                photo=form.cleaned_data['photo'],
                                                resume_content=form.cleaned_data['resume_content'],
                                                name=request.user.customer
                                                )
                Education.objects.create(school_name=form.cleaned_data['school_name'],
                                        qualifications=form.cleaned_data['qualifications'],
                                        start_end_date=form.cleaned_data['Ed_start_end_date'],
                                        notes=form.cleaned_data['Ed_notes'],
                                        name=resume
                                        )
                Experience.objects.create(employer=form.cleaned_data['employer'],
                                        job_title=form.cleaned_data['job_title'],
                                        start_end_date=form.cleaned_data['Ex_start_end_date'],
                                        notes=form.cleaned_data['Ex_notes'],
                                        name=resume
                                        )

                return redirect('job-home')
        else:
            form = AddResumeForm()
        return render(request, 'user/addResume.html', {'form': form})


@login_required
def MyResume(request):
    if request.user.customer.Type == 'CN':
        context= {
            'resume' : Resume.objects.filter(name=request.user.customer),
        }
        return render(request,'user/Myresume.html',context)
@login_required
def manageProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user.customer)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.customer)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Create a subscription if does not exists 
            try:
                UserSubscription.objects.get(name=request.user)
            except UserSubscription.DoesNotExist:
                    subscription = UserSubscription.objects.create(sub_status='None',
                    name=request.user)
            try:
                cust=Customer.objects.get(user=request.user)
                cust.form_completed=True
                cust.save()
            except:
                pass
            messages.success(request, f'Your account has been updated!')
            return redirect('/')

    else:
        user_form = UserUpdateForm(instance=request.user.customer)
        profile_form = ProfileUpdateForm(instance=request.user.customer)

    context = {
        'u_form': user_form,
        'p_form': profile_form
    }

    return render(request, 'user/profile.html', context)
    
@login_required
def viewResume(request,pk):
     if request.user.customer.Type == 'CN':
        
        context= {
            'resume' : Resume.objects.get(id=pk),
            'education' : Education.objects.filter(name_id=pk),
            'experience' : Experience.objects.filter(name_id=pk),
        }
        return render(request,'user/viewResume.html',context)   

@login_required
def updateResume(request,pk):
    if request.user.customer.Type == 'CN':
        if request.method=='POST':
            form_R = UpdateResume(request.POST,request.FILES,instance=Resume.objects.get(id=pk))
            form_Ed = UpdateEducation(request.POST,instance=Education.objects.get(name_id=pk))
            form_Ex = UpdateExprience(request.POST,instance=Experience.objects.get(name_id=pk))

            if form_R.is_valid() and form_Ed.is_valid() and form_Ex.is_valid():
                form_R.save()
                form_Ed.save()
                form_Ex.save()
                # username = form_U.cleaned_data.get('username')
                # messages.success(request, f'Successfully updated {username}!')
                return redirect('user-myresume')
        else:
            form_R = UpdateResume(request.POST,request.FILES)
            form_Ed = UpdateEducation(request.POST)
            form_Ex = UpdateExprience(request.POST)

        context = {
            'form_R':form_R,
            'form_Ed':form_Ed,
            'form_Ex':form_Ex,
        }   
        return render(request,'user/updateResume.html',context)

@login_required
def deleteResume(request,r_pk):
    if request.user.customer.Type == 'CN':
        Resume.objects.filter(id=r_pk).delete()
    return redirect('user-myresume')


#new added
@login_required
def SelectResume(request,j_pk):
    if request.user.customer.Type == 'CN':
        context= {
            'resume' : Resume.objects.filter(name=request.user.customer),
            'job' : {
                'id' : j_pk
            }
        }
        return render(request,'user/selectResume.html',context)

@login_required
def userApplied(request,j_pk,r_id):
    resume=Resume.objects.get(id=r_id)
    if request.user.customer.Type == 'CN' and request.user.customer == resume.name:
        
        job_obj = job.objects.get(id=j_pk)
        job_obj.applications.add(resume)
        job_obj.save()
        return render(request,'user/confirmed.html')
    else:
        return redirect('job-home')

