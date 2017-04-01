#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__Author = 'Kongzhagen'
from django.forms import ModelForm
import models

class customerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(customerForm, self).__init__(*args, **kwargs)
        # self.fields['qq'].widget.attrs['class'] = "form-control"
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})