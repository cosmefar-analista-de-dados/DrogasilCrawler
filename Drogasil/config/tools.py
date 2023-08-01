import json

_config = {
    'meta': {
        'author': 'gabriel-barata',
        'version': '0.1',
        'crawler': 'drogasil',
        'url': 'https://www.drogasil.com.br',
        'allowed_domains': [
            'drogasil.com.br'
        ],
        'routes': [
            'cosmeticos.html',
            'beleza.html'
        ]
    },
    'selectors': {
        'items': {
            'css' : {
                'product_name': 'h1[class*="TitleStyles"]::text',
                'brand': 'li.brand::text',
                'volume': 'li.quantity::text',
                'sku': 'table tbody tr:nth-child(1) div::text',
                'manufacturer': 'table tbody th:contains("Fabricante") + td a::text',
                'EAN' : 'table tbody tr:nth-child(2) div::text',
                'weight': 'table tbody th:contains("Peso (kg)") + td div::text',
                'description': 'div[class*="ProductDescriptionStyle"] p::text',
                'price': 'div[class*="ThirdColumnStyles"] div.price-box .price ::text'
            }
        },
        'attributes': {
            'css': {
                'categories': '#filter-categories ol li a::attr(href)',
                'sub_categories': '#filter-categories ol li a::attr(href)',
                'product_page': 'div[class*="ProductCardStyle"] > a.LinkNext::attr(href)',
                'total_results': 'div[class*="FoundStyles"] p::text'
                }
            }
        },
    'page_patterns': {
        'results_per_page': 48
    }
}

def get_config(load_from_file = False):
    if load_from_file:
        with open('config.json', 'r') as f:
            return json.load(f)
    return _config

def generate_config():
    with open('config.json', 'w') as f:
        return json.dump(_config, f, indent = 4)

if __name__ == '__main__':
    generate_config()