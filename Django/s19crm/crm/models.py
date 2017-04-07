# Create your models here.
#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User

course_type_choices = (('online', u'网络班'),
                       ('offline_weekend', u'面授班(周末)'),
                       ('offline_fulltime', u'面授班(脱产)'),)

class School(models.Model):
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)
    city = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)
    school = models.ForeignKey('School')

    def __unicode__(self):
        return self.name

    # 设置3个权限字段，拥有权限者可操作此表(在admin中授权用户)
    class Meta:
        permissions = (
            ('view_customer_list',u"查看客户列表"),  # 权限字段名称及其解释
            ('view_customer_info',u"查看客户详情"),
            ('edit_own_customer_info',u"修改自己的客户信息"),
        )

class Customer(models.Model):
    qq = models.CharField(max_length=64,unique=True)
    name = models.CharField(max_length=32,blank=True,null=True)
    phone = models.BigIntegerField(blank=True,null=True)
    course = models.ForeignKey('Course')

    type = models.CharField(max_length=64,choices=course_type_choices)
    consult_memo = models.TextField()
    source_type_choices = (('qq',u"qq群"),
                   ('referral',u"内部转介绍"),
                   ('51cto',u"51cto"),
                   ('agent',u"招生代理"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(max_length=64,choices=source_type_choices)
    referral_from = models.ForeignKey('self',blank=True,null=True,related_name="referraled_who")
    status_choice = (('signed',u"已报名"),
                      ('unregistered',u"未报名"),
                      ('graduated',u"已毕业"),
                      ('drop-off',u'退学'),
                      )
    status = models.CharField(choices=status_choice, max_length=64)
    consultant = models.ForeignKey('UserProfile', verbose_name=u'课程顾问')
    class_list = models.ManyToManyField("classList", blank=True)
    date = models.DateField(u'咨询日期', auto_now_add=True)
    def __unicode__(self):
        return '%s(%s)' % (self.qq, self.name)

class CustomerTrackRecord(models.Model):
    customer = models.ForeignKey(Customer)
    track_record= models.TextField(u"跟踪记录")
    track_date = models.DateField()
    follower = models.ForeignKey(UserProfile)
    status_choices = ((1, u"近期无报名计划"),
                      (2, u"2个月内报名"),
                      (3, u"1个月内报名"),
                      (4, u"2周内报名"),
                      (5, u"1周内报名"),
                      (6, u"2天内报名"),
                      (7, u"已报名"),
                      )
    status = models.IntegerField(u"状态",choices=status_choices)
    def __unicode__(self):
        return self.customer

class Course(models.Model):
    name = models.CharField(max_length=64,unique=True)
    online_price = models.IntegerField()
    offline_price = models.IntegerField()
    introduction = models.TextField()

    def __unicode__(self):
        return self.name

class classList(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    semester = models.IntegerField(verbose_name=u'学期')
    course_type = models.CharField(max_length=64, choices=course_type_choices, default='offline_weekend')
    teachers = models.ManyToManyField(UserProfile)
    start_date = models.DateField()
    graudate_date = models.DateField()

    def __unicode__(self):
        return '%s(%s)(%s)' % (self.course.name, self.course_type, self.semester)

    class Meta:
        unique_together = ('course', 'semester', 'course_type')


class courseRecord(models.Model):
    class_obj = models.ForeignKey(classList)
    day_num = models.IntegerField(u"第几节课")
    course_date = models.DateField(auto_now_add=True,verbose_name=u"上课时间")
    teacher = models.ForeignKey(UserProfile)
    # students = models.ManyToManyField(Customer)
    def __unicode__(self):
        return '%s,%s' % (self.class_obj, self.day_num)
    class Meta:
        unique_together = ('class_obj', 'day_num')

class StudyRecord(models.Model):
    course_record = models.ForeignKey(courseRecord)
    student = models.ForeignKey(Customer)
    record_choices = (('checked', u"已签到"),
                      ('late', u"迟到"),
                      ('noshow', u"缺勤"),
                      ('leave_early', u"早退"),
                      )
    record = models.CharField(u"状态", choices=record_choices, max_length=64)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (0, 'D'),
                     (-1, 'N/A'),
                     (-100, 'COPY'),
                     (-1000, 'FAIL'),
                     )
    score = models.IntegerField(u"本节成绩", choices=score_choices, default=-1)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(u"备注", max_length=255, blank=True, null=True)
    def __unicode__(self):
        return '%s,%s,%s' % (self.course_record, self.student, self.record)
