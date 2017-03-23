#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from s19crm import settings


os.environ['DJANGO_SETTINGS_MODULE'] = 's19crm.settings'
import django
django_setup()




