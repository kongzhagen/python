#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__Author__ = 'Kongzhagen'

from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect

perm_dic = {
    'view_customer_list':['customer_list','GET',[]],  # 权限字段(view)，URL,GET,参数
    'view_customer_info':['customer_detail','GET',[]],
    'edit_own_customer_info':['customer_detail','POST',['test']],
}

def perm_check(*args, **kwargs):
    request = args[0]
    url_resovle_obj = resolve(request.path_info)
    current_url_namespace = url_resovle_obj.url_name
    print "url namespace:",current_url_namespace
    matched_flag = False
    matched_perm_key = None
    if current_url_namespace is not None:
        print "find perm ..."
        for perm_key in perm_dic:
            perm_val = perm_dic[perm_key]
            if len(perm_val) == 3:
                url_namespace,request_method,request_args = perm_val
                print(url_namespace,current_url_namespace)
                if url_namespace == current_url_namespace:
                    if request.method == request_method:
                        if not request_args:
                            matched_flag = True
                            matched_perm_key = perm_key
                            print 'matched ...'
                            break
                        else:
                            for request_arg in request_args:
                                request_method_func = getattr(request,request_method)
                                if request_method_func.get(request_arg) is not None:
                                    matched_flag = True
                                else:
                                    matched_flag = False
                                    print "request arg[%s] not matched"%request_arg
                                    break
                            if matched_flag == True:
                                print "--passed permission check --"
                                matched_perm_key = perm_key
                                break
    else:
        return True

    if matched_flag == True:
        perm_str = 'crm.%s'%matched_perm_key
        if request.user.has_perm(perm_str):
            print "\033[42;1m ------no permission check-------\033[0m"
            return True
        else:
            print "\033[41;1m -------no permission --------\033[0m"
            print request.user,perm_str
    else:
        print "\033[41;1m ------no matched permission ----- \033[0m"

def check_permission(func):
    def wrapper(*args, **kwargs):
        print "--start check perms",args[0]
        if not perm_check(*args, **kwargs):
            return render(args[0],'crm/403.html')
        return func(*args, **kwargs)
    return wrapper

