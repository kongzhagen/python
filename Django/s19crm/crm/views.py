from django.shortcuts import render
import models

# Create your views here.
def dashboard(request):
    return render(request,'crm/dashboard.html')

def customers(request):
    cus_list = models.Customer.objects.all()
    return render(request,'crm/customers.html',{"cus_list":cus_list})