from django.shortcuts import render
import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def dashboard(request):
    return render(request,'crm/dashboard.html')

def customers(request):
    cus_list = models.Customer.objects.all()
    paginator = Paginator(cus_list,1,2)
    page = request.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request,'crm/customers.html',{"cus_list":customer})