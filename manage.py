from scrapy import cmdline

def main():
    spider_name = 'area_spider'
    # cmdline.execute(f'scrapy crawl {spider_name}'.split())
    cmdline.execute(f'scrapy crawl {spider_name} -o ./areacode/spiders/area.csv'.split())

if __name__ == '__main__':
    main()