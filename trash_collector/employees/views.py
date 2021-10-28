
from django.db.models.fields import Field
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date, datetime


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
        todays_pickup = Customer.objects.filter(weekly_pickup=day_of_week) | Customer.objects.filter(one_time_pickup=today)
        customers_today =todays_pickup.filter(zip_code=logged_in_employees.zip_code) and todays_pickup.exclude(date_of_last_pickup=today)
        non_suspended = customers_today.exclude(suspend_start__lt=today, suspend_end__gt=today)         
        context = {
            'logged_in_employees': logged_in_employees,
            'today': today,
            'day_of_week': day_of_week,
            'todays_pickup': todays_pickup,
            'customers_today': customers_today,
            'non_suspended': non_suspended     
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
def confirm(request, customer_id):
    try:
        Customer = apps.get_model('customers.Customer')
        customer_pickup = Customer.objects.get(id = customer_id)
        customer_pickup.balance += 20
        customer_pickup.date_of_last_pickup = datetime.now()
        customer_pickup.save()

        return render(request, 'employees/confirm.html')
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))




    

def weekly_pickup(request):
    Customer = apps.get_model('customers.Customer')
    # logged_in_user = request.user
    # logged_in_employees = Employee.objects.get(user=logged_in_user)
    today = date.today()

    if request.method =="POST":
        day_entered = request.POST.get('weekly_pickup')
        customers_today = Customer.objects.filter(weekly_pickup=day_entered)

    # try:
    #     
    #     day_of_week = calendar.day_name[today.weekday()]
    #     todays_pickup = Customer.objects.filter(weekly_pickup=day_of_week)
    #     customers_today =todays_pickup.filter(zip_code=logged_in_employees.zip_code)
    #     week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    #     selected_day = customers_today.filter(weekly_pickup=week_days)

        context = {
            # 'logged_in_employees': logged_in_employees,
            'today': today,
            'day_entered':day_entered,    
            'customers_today': customers_today   
    }
        return render(request, 'employees/weekly_pickup.html', context)
    
    else:
        return render(request, 'employees/weekly_pickup.html')

    #     return HttpResponseRedirect(reverse('employees:weekly_pickup'))

        
       
            
           
        
    
