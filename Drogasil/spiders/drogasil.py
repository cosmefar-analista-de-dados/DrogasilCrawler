from Drogasil.config.tools import get_config
from Drogasil.items import DrogasilItem
from urllib.parse import urljoin
from math import ceil
import scrapy

env = get_config()
item_selectors = env.get('selectors').get('items')
attr_selectors = env.get('selectors').get('attributes')
class DrogasilSpider(scrapy.Spider):
    name = env.get('meta').get('crawler')
    allowed_domains = [
        allowed_domain for allowed_domain in env.get('meta').get('allowed_domains')
    ]

    def start_requests(self):
        initial_routes = [route for route in env.get('meta').get('routes')]
        domain = env.get('meta').get('url')

        for route in initial_routes:
            relative_url = urljoin(domain, route)
            yield scrapy.Request( url = relative_url,
                                  callback = self.parse_category_urls,
                                  meta = {'route': route,
                                          'domain': domain})
    def parse_category_urls(self, response):

        route = response.meta['route']
        domain = response.meta['domain']

        categories = response.css(attr_selectors.get('css').get('categories')).getall()

        for category in categories:

            category_url = urljoin(domain, category)

            yield scrapy.Request(url = category_url,
                                 callback = self.parse_relative_page,
                                 meta = {'domain': domain,
                                         'route': route})

    def parse_relative_page(self, response):

        domain = response.meta['domain']

        sub_categories = response.css(attr_selectors.get('css').get('sub_categories')).getall()
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
            attr_selectors.get('css').get('product_page')
        ).getall()

        for product_page in product_pages:
            yield scrapy.Request(url = product_page,
                                 callback = self.parse_product,
                                 meta = {'current_page': current_page
                                         })

        if page == 1:

            total_results = int(response.css(
                attr_selectors.get('css').get('total_results')).get())
            number_pages = ceil(
                total_results / env.get('page_patterns').get('results_per_page'))

            for page_num in range(2, number_pages):
                next_page = f"{current_page}?p={page_num}"
                yield scrapy.Request(url = next_page,
                                     callback =self.parse_page,
                                     meta = {'current_page': current_page,
                                             'page_num': page_num
                                             })

    def parse_product(self, response):

        current_page = response.meta['current_page']
        item = DrogasilItem()

        item['url'] = response.url,
        item['sku'] = response.css(item_selectors.get('css').get('sku')).get(),
        item['EAN'] = response.css(item_selectors.get('css').get('EAN')).get(),
        item['product'] = response.css(item_selectors.get('css').get('product_name')).get(),
        item['brand'] = response.css(item_selectors.get('css').get('brand')).get(),
        item['quantity'] = response.css(item_selectors.get('css').get('volume')).get(),
        item['weight'] = response.css(item_selectors.get('css').get('weight')).get(),
        item['manufacturer'] = response.css(item_selectors.get('css').get('manufacturer')).get(),
        item['description'] = response.css(item_selectors.get('css').get('description')).getall(),
        item['category'] = current_page,
        item['sub_category'] = current_page
        item['price'] = response.css(item_selectors.get('css').get('price')).getall()

        yield item