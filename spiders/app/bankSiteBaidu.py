#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from selenium import webdriver
import time
import Mysql

class getWebSiteNearby(object):
    def __init__(self):
        self.browser = self.openBaseUrl()
        self.data2db()
        self.browser.quit()

    def openBaseUrl(self):
        browser = webdriver.Firefox()
        baseUrl = 'http://map.baidu.com/'
        try:
            browser.get(baseUrl)
            browser.implicitly_wait(10)
            return browser
        except Exception as e:
            self.browser.quit()
            print e
            exit(1)

    def siteNearby(self,args):
        # 输入网点信息并查询,args=[u'北京',u'中国邮政储蓄银行三里河支行',u'银行','ATM']
        self.browser.refresh()
        time.sleep(10)
        city = args.pop(0)
        banksite = args.pop(0)
        print city,banksite
        textButton = self.browser.find_element_by_id('sole-input')
        textButton.clear()
        textButton.send_keys(banksite.decode('utf8'))
        self.browser.find_element_by_id('search-button').click()
        time.sleep(10)
        # 选择要查询的元素
        search_key = banksite.replace("中国邮政储蓄银行",'')
        # 是否能找到搜索的站点
        banks = self.browser.find_element_by_xpath('//ul[@class="poilist"]')
        try:
            ser = banks.find_element_by_partial_link_text(search_key)
            banksite_ser = ser.text
            ser.click()
        except:
            with open("banksite_bad.txt",'a') as fp:
                fp.write('%s未取到数据 \n'%banksite)
            return

        # 附近搜索
        self.browser.find_element_by_xpath('//span[@class="buttons-nearby-text"]').click()
        print '%s开始取数 ...'%banksite
        items = []
        for each in args:
            # 网点附近的搜索目标
            serButton = self.browser.find_element_by_id("nearby-input")
            serButton.clear()
            serButton.send_keys(each.decode('utf8'))
            self.browser.find_element_by_id("search-button").click()
            time.sleep(10)
            subSelector = self.browser.find_elements_by_xpath('//ul[@class="poilist"]/li')
            for sub in subSelector:
                tmp = self.parser(each,sub)
                if not tmp:
                    continue
                tmp['banksite'] = banksite.decode('utf8')
                tmp['banksite_ser'] = banksite_ser
                tmp['city'] = city.decode('utf8')
                tmp['type'] = each.decode('utf8')
                # 数据出现重复，说明此类型的数据取数已出现问题，退出程序
                if tmp in items:
                    break
                print tmp['name']
                items.append(tmp)
            # 下一页
            Flag = True
            while Flag:
                try:
                    self.browser.find_element_by_link_text("下一页>").click()
                    time.sleep(3)
                    subSelector = self.browser.find_elements_by_xpath('//ul[@class="poilist"]/li')
                    for sub in subSelector:
                        tmp = self.parser(each,sub)
                        # 如果解析为空值，则继续解析一下项
                        if not tmp:
                            continue
                        tmp['banksite'] = banksite.decode('utf8')
                        tmp['banksite_ser'] = banksite_ser
                        tmp['city'] = city.decode('utf8')
                        tmp['type'] = each.decode('utf8')
                        if tmp in items:
                            Flag = False
                            break
                        print tmp['name']
                        if tmp['dis'][-1] == u'里':
                            print '%s大于1公里,退出...'%tmp['name']
                            Flag = False
                            continue
                        else:
                            items.append(tmp)
                except Exception as e:
                    break
        print '%s取数结束.......'%banksite
        return items

    # 传参：附近搜索目标，每个li
    def parser(self,each,sub):
        item = {}
        # 去除广告
        try:
            sub.find_element_by_partial_link_text("广告")
            return item
        except:
            pass
        # 银行不取atm
        if each == '银行':
            try:
                sub.find_element_by_partial_link_text("ATM")
                return item
            except:
                item['name'] = sub.find_element_by_xpath('.//a[@class="n-blue"]').text
        else:
            item['name'] = sub.find_element_by_xpath('.//a[@class="n-blue"]').text
        try:
            dis = sub.find_element_by_xpath('.//div[@class="mt_5 h_20"]/span').text
        except:
            try:
                dis = sub.find_element_by_xpath('.//span[@class="float-r n-grey"]').text
            except:
                dis = sub.find_element_by_xpath('.//span[@class="span_right"]/span').text
        item['dis'] = dis
        # 公交地铁不取地址
        if each in ['公交','地铁']:
            addr = u'未知'
        else:
            try:
                addr = sub.find_element_by_xpath('.//div[@class="row addr"]/span').text
            except:
                addr = u'未知'
        item['addr'] = addr
        return item

    def data2db(self):
        with open('banksites','r') as fp:
            all_lines = fp.readlines()
        for i in all_lines:
            site = i.split(',')
            datas = self.siteNearby(site)
            if datas:
                for line in datas:
                    Mysql.db_ins.IntoTab('banksitesnearby_new',line)

if __name__ == '__main__':
    getWebSiteNearby()
