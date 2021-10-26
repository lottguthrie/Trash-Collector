from django.db.models.fields import NullBooleanField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
from django.views import generic

# from trash_collector.customers.views import one_time_pickup
from.models import Employee
from customers.models import Customer
import calendar



# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employees = Employee.objects.get(user=logged_in_user)
        today = date.today()
        day_of_week = calendar.day_name[today.weekday()]
        todays_pickup = Customer.objects.filter(weekly_pickup = day_of_week)
        customers_today =todays_pickup.filter(zip_code = logged_in_employees.zip_code)
        # one_time = Customer.objects.filter(one_time_pickup = today)
        # non_suspended = Customer.objects.filter(suspend_end = "No")
        
        context = {
            'logged_in_employees': logged_in_employees,
            'today': today,
            'day_of_week': day_of_week,
            'todays_pickup': todays_pickup,
            "customers_today": customers_today,
            # 'one_time': one_time,
            # 'non_suspended': non_suspended
            
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')    

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employees = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employees': logged_in_employees
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def detail(request, customer_id):
    logged_in_user = request.user
    logged_in_employees = Employee.objects.get(user=logged_in_user)
    customer_from_db = Customer.objects.get(pk=customer_id)
    return render(request, 'customers/detail.html', {'customers': customer_from_db})

@login_required
def edit(request, customer_id):
    logged_in_user = request.user
    logged_in_employees = Employee.objects.get(user=logged_in_user)
    customer_from_db = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        customer_from_db.customer_id = request.POST.get('customer_id')
        customer_from_db.name = request.POST.get('name')
        customer_from_db.address = request.POST.get('address')
        customer_from_db.zip_code = request.POST.get('zip_code')
        customer_from_db.weekly_pickup = request.POST.get('weekly_pickup')
        customer_from_db.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        Customer = apps.get_model('customers.Customer')
        all_customers = Customer.objects.all()
        context = {
            'customers': customer_from_db,
            'all_customers': all_customers
        }
        return render(request, 'customers/edit_profile.html', context)

@login_required
def delete(request, customer_id):
    logged_in_user = request.user
    logged_in_employees = Employee.objects.get(user=logged_in_user)
    customer_from_db = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        customer_from_db.name = request.POST.get('name')
        customer_from_db.address = request.POST.get('address')
        customer_from_db.zip_code = request.POST.get('zip_code')
        customer_from_db.weekly_pickup = request.POST.get('weekly_pickup')
    customer_from_db.delete()
    return HttpResponseRedirect(reverse('players:index'))

class CustomerListView(generic.ListView):
    # Generic views often require you to tell it what model it will be based on, where the template is located,
    # and what name the template will be using for the context object. 
    # There are other settings that may be used as well!
    model = Customer
    template_name = 'customers/customers.html'
    context_object_name = 'customers'

    # This queryset will find all the players who share a team with the player
    def get_queryset(self):
        # use apps.get_model to find the Team model from the teams app. No need to import!
        Customer = apps.get_model('customers.Customer')
        # query for the Team object with the pk that got passed in from the url path in urls.py
        # self.kwargs contains the named arguments passed in from the url, in this case 'team'
        self.customer = get_object_or_404(Customer, name=self.kwargs['customer'])
        # query set will return all the Player objects whose team matches the team we just found
        return Customer.objects.filter(weekly_pickup=self.customer)

    # We use this to add an additional property to our context object, in this case the name of the team
    # This allows our template to display more than just the results of the queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        #First we retrieve the context dictionary
        context = super().get_context_data(**kwargs)
        #Then we add an additional key to it
        context['customer_name'] = self.customer.name
        return context