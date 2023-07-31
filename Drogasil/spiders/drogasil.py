from Drogasil.config.tools import get_config
from Drogasil.items import DrogasilItem
from urllib.parse import urljoin
from math import ceil
import scrapy

env = get_config()

class DrogasilSpider(scrapy.Spider):
    name = "drogasil"
    allowed_domains = ["drogasil.com.br"]

    def start_requests(self):
        initial_routes = ['cosmeticos.html']
        domain = 'https://www.drogasil.com.br'

        for route in initial_routes:
            relative_url = urljoin(domain, route)
            yield scrapy.Request( url = relative_url,
                                  callback = self.parse_category_urls,
                                  meta = {'route': route,
                                          'domain': domain})
    def parse_category_urls(self, response):

        route = response.meta['route']
        domain = response.meta['domain']

        categories = response.css('#filter-categories ol li a::attr(href)').getall()

        for category in categories:
            if route in category:
                category_url = urljoin(domain, category)
            else:
                domain = urljoin(domain, route)
                category_url = urljoin(domain, category.split('/')[-1])

            yield scrapy.Request(url = category_url,
                                 callback = self.parse_relative_page,
                                 meta = {'domain': domain,
                                         'route': route})

    def parse_relative_page(self, response):

        domain = response.meta['domain']

        sub_categories = response.css('#filter-categories ol li a::attr(href)').getall()
        for sub_category in sub_categories:

            sub_category_url = urljoin(domain, sub_category)
            yield scrapy.Request(url = sub_category_url,
                                 callback = self.parse_page,
                                 meta = {'current_page': sub_category_url,
                                         'page_num': 1})

    def parse_page(self, response):

        current_page = response.meta['current_page']
        page = response.meta['page_num']

        product_pages = response.css(
            'div[class*="ProductCardStyle"] > a.LinkNext::attr(href)'
        ).getall()

        for product_page in product_pages:
            yield scrapy.Request(url = product_page,
                                 callback = self.parse_product)

        if page == 1:

            total_results = int(response.css('div[class*="FoundStyles"] p::text').get())
            number_pages = ceil(
                total_results / env.get('page_patterns').get('results_per_page'))

            for page_num in range(2, number_pages):
                next_page = f"{current_page}?p={page_num}"
                yield scrapy.Request(url = next_page,
                                     callback =self.parse_page,
                                     meta = {'current_page': current_page,
                                             'page_num': page_num})

    def parse_product(self, response):

        item = DrogasilItem()

        item['url'] = response.url,
        item['sku'] = response.css('table tbody tr:nth-child(1) div::text').get(),
        item['EAN'] = response.css('table tbody tr:nth-child(2) div::text').get(),
        item['product'] = response.css('h1[class*="TitleStyles"]::text').get(),
        item['brand'] = response.css('li.brand::text').get(),
        item['quantity'] = response.css('li.quantity::text').get(),
        item['weight'] = response.css(
            'table tbody th:contains("Peso (kg)") + td div::text').get(),
        item['manufacturer'] = response.css(
            'table tbody th:contains("Fabricante") + td a::text').get(),
        item['description'] = response.css(
            'div[class*="ProductDescriptionStyle"] p::text').getall()

        yield item