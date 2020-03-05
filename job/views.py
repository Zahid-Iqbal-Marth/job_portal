from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import job,Package
from user.models import UserSubscription
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from user.models import Resume,Education,Experience
from django.urls import reverse_lazy
from .forms import SearchForm,PostCreateForm
from django.conf import settings # new
import stripe # new
from django.contrib import messages
from django.template.response import TemplateResponse
stripe.api_key = settings.STRIPE_SECRET_KEY # new
import datetime
from django.utils import timezone
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            return redirect('post-search', form.cleaned_data['search'])
    else:
        form = SearchForm()
    context= {
        'jobs' : job.objects.all(),
        'form':form
    }
    return render(request,'job/home.html',context)




class PostListView(ListView):
    model = job
    #model variable represent the class/db_table to which this view belongs to.
    template_name='job/home.html'
    context_object_name='jobs'
    ordering=['post_date']

class PostDetailView(DetailView):
    model = job
    template_name='job/post_detail.html'
@login_required
def PostCreateView(request):
    
    context= {
    'packages' : Package.objects.all(),
    'key' : settings.STRIPE_PUBLISHABLE_KEY,
    
    }
    if request.user.customer.Type=='EM':
        try:  
            subs=UserSubscription.objects.get(name_id=request.user)
        except UserSubscription.DoesNotExist:
            messages.info(request,"You have not subscribed to any plan")
            return render(request,'job/pricing-tables.html',context)
    
    sub_package=Package.objects.get(id=subs.package_id)
    jobs_posted=job.objects.filter(job_poster=request.user.customer).count()
    if not subs.sub_status:
        messages.info(request,"You have not subscribed to any plan")
        return render(request,'job/pricing-tables.html',context)

        
    if (jobs_posted<sub_package.job_posting_limit) :

        if request.method == 'POST':
            form=PostCreateForm(request.POST , request.FILES )
            if form.is_valid():
                form.instance.job_poster=request.user.customer
                form.save()
                #new
                return redirect('user-myjob')
        else:
            form_class=PostCreateForm
            form={'form':form_class}
            return render(request,'job/post_create.html',form)
    else :
        messages.info(request,"You have exceeded job posting limit kindly subscribe new plan")
        return render(request,'job/pricing-tables.html',context)

    
'''
class PostCreateView(LoginRequiredMixin,CreateView):
    # if self.request.user.customer.Type == 'EM':
    model = job
    fields=['job_title','location','discription','company_name','website_url']
    template_name='job/post_create.html'
    success_url='/' 
    def form_valid(self,form):
        form.instance.job_poster=self.request.user.customer
        return super().form_valid(form)

    '''
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = job
    fields=['job_title','location','discription','company_name','website_url']
    template_name='job/post_create.html'
    #success=<'any url'> // on success
    # success_url='post/my/'
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user.customer == post.job_poster :
            return True
        return False

    def get_success_url(self):         
        return reverse_lazy('post-detail', args = (self.object.id,))


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = job
    template_name='job/post_confirm_delete.html'
    success_url='/'
    def test_func(self):
        post = self.get_object()
        if self.request.user.customer == post.job_poster :
            return True
        return False


@login_required
def MyJobs(request):
    if request.user.customer.Type == 'EM':
        context= {
            'jobs' : job.objects.filter(job_poster=request.user.customer),
        }
        return render(request,'job/myjobs.html',context)  

@login_required
def ViewPricingTable(request):
    if request.user.customer.Type == 'EM':
        context= {
        'packages' : Package.objects.all(),
        'key' : settings.STRIPE_PUBLISHABLE_KEY
        
        }
        return render(request,'job/pricing-tables.html',context)
#new added
@login_required
def viewCheckoutPage(request,pk):
    if request.user.customer.Type == 'EM':
        context= {
            'packages' : Package.objects.all(),
            'key' : settings.STRIPE_PUBLISHABLE_KEY
            
            }
        if request.user.customer.form_completed == False:
            messages.info(request,"Your Need to add profile Information first")
            
            return render(request,'job/pricing-tables.html',context)
        try:
            check_package=Package.objects.get(id=pk)
        except Package.DoesNotExist:
            return render(request,'job/pricing-tables.html',context)
        checkout={
            'package' :check_package,
            'key' : settings.STRIPE_PUBLISHABLE_KEY
        }
        return render(request,'job/checkout.html',checkout)
@login_required
def Charge(request,pk):
    if request.user.customer.Type == 'EM':      
        context= {
        'packages' : Package.objects.all(),
        'key' : settings.STRIPE_PUBLISHABLE_KEY,
        
        }
        
        if request.method == 'POST':
            check_user=request.user
            try:
                package=Package.objects.get(id=pk)
            except:
                return render(request,'job/pricing-tables.html',context)
            

            try:
                try:
                    subscriber=UserSubscription.objects.get(name_id=request.user)
                except UserSubscription.DoesNotExist:
                    subscriber=UserSubscription.objects.create(sub_status='None',
                    name=request.user) 
                if not subscriber.stripe_cust_id:
                    stripe_cust=stripe.Customer.create(
                    name=check_user.first_name,
                    email=check_user.email,
                    phone=check_user.customer.phone,
                    address={
                        'line1' :check_user.customer.country,
                        'country':check_user.customer.country,
                        'state': check_user.customer.state,
                        'city':check_user.customer.city,
                        'postal_code':check_user.customer.zip_code,
                    })
                    subscriber.stripe_cust_id=stripe_cust['id']
                else: 
                    stripe_cust=stripe.Customer.retrieve(subscriber.stripe_cust_id)
                
                            
                
                stripe_card=stripe.Customer.create_source(
                stripe_cust['id'],
                source=request.POST['stripeToken'],
                )
                
                charge = stripe.Charge.create(
                    amount=(package.price)*100, # it is in docs, multiply 100 for cents 
                    currency='usd',
                    customer=stripe_cust,
                    description='AllNet Employer charge',
                    source=stripe_card['id'],
                    metadata={'integration_check': 'accept_a_payment'},
                )
                stripe.PaymentIntent.create(
                    amount=(package.price)*100,
                    currency="usd", 
                    payment_method=stripe_card,
                    payment_method_types=["card"],
                    confirm=True,
                    customer=stripe_cust,
                )
            except stripe.error.CardError as e:
                messages.info(request,"Your Card has been declined")
                return render(request,'job/pricing-tables.html',context)
            
            
            subscriber.package_id=pk
            subscriber.paid_count=1
            subscriber.sub_status='Subscribed'
            subscriber.sub_date=timezone.now()
            subscriber.save()


            sub_context={
                'package':package
            }
            
            return render(request,'job/charge.html',sub_context)
        else:
        
            return render(request,'job/pricing-tables.html',context)

@login_required
def applicants(request,pk):
    if request.user.customer.Type == 'EM':
        j=job.objects.get(id=pk)
        context= {
            'resume' :j.applications.all(),
            'job' : {
                'id' : pk
            }
        }
        return render(request,'job/applicants.html',context) 

@login_required
def detailApplicants(request,j_pk,r_pk):
     if request.user.customer.Type == 'EM':
        
        context= {
            'resume' : Resume.objects.get(id=r_pk),
            'education' : Education.objects.filter(name_id=r_pk),
            'experience' : Experience.objects.filter(name_id=r_pk),
        }
        return render(request,'job/detailApplicants.html',context) 


def Search(request,SearchWord):
    context= {
        'jobs' : job.objects.filter(job_title__icontains=SearchWord) | job.objects.filter(discription__icontains=SearchWord) | job.objects.filter(company_name__icontains=SearchWord)
    }   
    return render(request,'job/myjobs.html',context) 
