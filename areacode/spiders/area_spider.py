# -*- coding: utf-8 -*-
import scrapy

from areacode.items import AreacodeItem

base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'

class AreaSpiderSpider(scrapy.Spider):
    name = 'area_spider'
    allowed_domains = ['www.stats.gov.cn']
    # 直接发送get请求
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html']



    # url = 'https://www.qiushibaike.com/8hr/page/{}'
    # page = 1

    # 该方法直接发送post请求，也是一个重写方法，使用时先将start_urls去掉
    # def start_requests(self):
    #     post_url = 'https://fanyi.baidu.com/langdetect'
    #     form_data = {
    #         'query': 'hello'
    #     }
    #     yield scrapy.FormRequest(url=post_url, formdata=form_data, callback=self.parse)


    # 解析函数，重写这个方法，发送请求之后，响应来了就会调用这个方法，函数有一个参数response就是响应内容，该函数对返回有一个要求，必须返回可迭代对象
    def parse(self, response):
        # 可以使用css
        province_list = response.css('.provincetr > td > a')
        for province in province_list:
            item = AreacodeItem()
            item['name'] = province.css('a::text').extract_first()
            url_param = province.css('a::attr(href)').extract_first()
            para = url_param.split('.')[0]
            item['code'] = para.ljust(6, '0')
            next_url = base_url + url_param
            # 将获取的属性存放到对象中
            item['parent_id'] = None
            yield item

            # 向每个省份发送请求
            yield scrapy.Request(url=next_url, callback=self.parse_province, meta={'parent': item['code'], 'para': para})


    def parse_province(self, response):
        # 通过response的meta属性，获取参数item
        parent= response.meta['parent']
        para = response.meta['para']

        city_list = response.css('.citytr')
        for city in city_list:
            item = AreacodeItem()
            item['code'] = city.css('td:first-child > a::text').extract_first()
            item['name'] = city.css('td:last-child > a::text').extract_first()
            city_para = city.css('td:first-child > a::attr(href)').extract_first()
            item['parent_id'] = parent
            yield item

            # 向每个市发送请求
            if city_para:
                next_url = base_url + city_para
                yield scrapy.Request(url=next_url, callback=self.parse_city, meta={'parent': item['code'], 'para': para})

    def parse_city(self, response):
        parent = response.meta['parent']
        para = response.meta['para']
        county_list = response.css('.countytr')
        for county in county_list:
            item = AreacodeItem()
            item['code'] = county.css('td:first-child > a::text').extract_first()
            item['name'] = county.css('td:last-child > a::text').extract_first()
            if not item['code']:
                item['code'] = county.css('td:first-child::text').extract_first()
            if not item['name']:
                item['name'] = county.css('td:last-child::text').extract_first()
            county_para = county.css('td:first-child > a::attr(href)').extract_first()
            item['parent_id'] = parent
            yield item

            # 向每个区/县发送请求
            if county_para:
                next_url = base_url + f'{para}/' + county_para
                yield scrapy.Request(url=next_url, callback=self.parse_county, meta={'parent': item['code']})

    def parse_county(self, response):
        parent = response.meta['parent']
        town_list = response.css('.towntr')
        for town in town_list:
            item = AreacodeItem()
            item['code'] = town.css('td:first-child > a::text').extract_first()
            item['name'] = town.css('td:last-child > a::text').extract_first()
            item['parent_id'] = parent

            yield item

        # county_list =
            # item = {
            #     'code': code,
            #     'name': name,
            #     'parent_id': None
            # }
        # # 获取所有的省份, 得到的是Selector对象
        # province_list = response.xpath('//tr[@class="provincetr"]')
        # for otr in province_list:
        #     td_list = otr.xpath('./td')
        #     for otd in td_list:
        #         try:
        #             name = otd.xpath('.//text()').extract()[0]
        #             url_param = otd.xpath('./a/@href').extract()[0]
        #             code = url_param.split('.')[0].ljust(12, '0')
        #             next_url = f'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/{url_param}'
        #             item = {
        #                 'code': code,
        #                 'name': name,
        #                 'parent_id': None
        #             }
        #             items.append(item)
        #         except Exception as e:
        #             print(e)
        # print(len(items))
        #
        # 接着发送请求，爬取下一页
        # if self.page <= 5:
        #     self.page += 1
        #     url = self.url.format(self.page)
        #     # 向拼接成功的url发送请求
        #     yield scrapy.Request(url, callback=self.parse)