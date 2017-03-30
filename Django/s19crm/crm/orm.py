#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os

from django.core.paginator import Paginator
objects = ['john','paul','george','ringo','lucy','meiry','checy','wind','flow','rain']
# 3条数据为一页，实例化分页对象
p = Paginator(objects,3)
print p.count  # 10 对象总共10个元素
print p.num_pages
# 4 对象可分4页
print p.page_range
# xrange(1, 5) 对象页的可迭代范围

page1 = p.page(1)  # 取对象的第一分页对象
print page1.object_list  # 第一分页对象的元素列表['john', 'paul', 'george']
print page1.number  # 第一分页对象的当前页值 1

page2 = p.page(2)  # 取对象的第二分页对象
print page2.object_list  # 第二分页对象的元素列表 ['ringo', 'lucy', 'meiry']
print page2.number  # 第二分页对象的当前页码值 2

print page1.has_previous()  # 第一分页对象是否有前一页 False
print page1.has_other_pages()  # 第一分页对象是否有其它页 True

print page2.has_previous()  # 第二分页对象是否有前一页 True
print page2.has_next()  # 第二分页对象是否有下一页 True
print page2.next_page_number()  # 第二分页对象下一页码的值 3
print page2.previous_page_number()  # 第二分页对象的上一页码值 1
print page2.start_index()  # 第二分页对象的元素开始索引 4
print page2.end_index()  # 第2分页对象的元素结束索引 6
print 'zzzz'
print page1.paginator.page_range



