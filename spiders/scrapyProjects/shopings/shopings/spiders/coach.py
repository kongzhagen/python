# -*- coding: utf-8 -*-
import scrapy
from shopings.items import ShopingsItem

class CoachSpider(scrapy.Spider):
    name = "coach"
    allowed_domains = ["coachaustralia.com"]
    start_urls = ['https://coachaustralia.com/catalog/men']
    # start_urls = ['https://coachaustralia.com/product/manhattan-backpack-in-mixed-leathers']

    def parse(self, response):
        if response.url.startswith("https://coachaustralia.com/product/"):
            item = ShopingsItem()
            title = response.xpath('//div[@class="product-title"]/h1/span/text()').extract()
            desc = response.xpath('//div[@class="product-description sanitize-description"]//ul/li/text()').extract()
            price = response.xpath('//div[@class="product-price"]/div/span/text()').extract()
            pic = response.xpath('//div[@class="picture"]/img/@src').extract()
            item['title'] = title[0]
            item['desc'] = desc
            item['price'] = price[0]
            item['pic'] = pic[0]
            yield item

        if response.url == 'https://coachaustralia.com/catalog/men':
            subSelector = response.xpath('//h2[@class="product-title"]/a/@href').extract()
            urls = []
            for sub in subSelector:
                tmp ='https://coachaustralia.com' + sub
                yield self.make_requests_from_url(tmp)
