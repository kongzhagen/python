# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib
import os
base_dir = r"C:\s19crm\scrapyprojects\shopings\shopings\pic_men"

class ShopingsPipeline(object):
    def process_item(self, item, spider):
        print item['pic'] + ' start ...'
        with open('coachaustralia.txt','a') as fp:
            fp.write(item['title'].strip() + '\n' + item['price'].strip() + '\n')
            for each in item['desc']:
                fp.write(each+'\n')
            fp.write('\n')
        pic_name = os.path.basename(item['pic'])
        file_name = os.path.join(base_dir,pic_name)
        urllib.urlretrieve(item['pic'],filename=file_name)
