from django.shortcuts import render,redirect
import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def dashboard(request):
    return render(request,'crm/dashboard.html')

def customers(request):
    cus_list = models.Customer.objects.all()
    paginator = Paginator(cus_list,2,2)
    page = request.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request,'crm/customers.html',{"cus_list":customer})

import forms
def customerInfo(request,customer_id):
    customer_obj = models.Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        form = forms.customerForm(request.POST, instance=customer_obj)
        if form.is_valid():
            form.save()
            baseUrl = "/".join(request.path.split("/")[:-2])
            print baseUrl
            return redirect(baseUrl)
    else:
        form = forms.customerForm(instance=customer_obj)
    return render(request, 'crm/customers_detail.html', {'cust_info':form})

