
from django.db.models.fields import Field
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from django.db.models import F

from.models import Employee
from customers.models import Customer
import calendar
from calendar import weekday


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
            "customers_today": customers_today,
            #'one_time': one_time,
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
def confirm(request):
    Customer = apps.get_model('customers.Customer')
    logged_in_user = request.user
    try:
        logged_in_employees = Employee.objects.get(user=logged_in_user)
        update_customers =  Customer.objects.filter(id=0)
        customer_balance = update_customers.update(balance=+20)
        form = Customer(request.POST or None)
        is_valid = True
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:confirm'))   


    context= {
        'customer_balance': customer_balance
            
        }
    return render(request, 'employees/confirm.html') 



    

    