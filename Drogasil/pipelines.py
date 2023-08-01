import Drogasil.utils.process as p
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

class DrogasilCleaning:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        # values are being returned into lists
        for field in fields:
            if field not in ["sub_category"]:
                value = adapter.get(field)
                adapter[field] = p.try_index_strip(value)

        # treating the description field, that was stored as a list
        value = adapter.get('description')
        adapter['description'] = '. '.join(value)

        for field in fields:
            if field in ['product', 'brand', 'manufacturer', 'description']:
                value = adapter.get(field)
                adapter[field] = p.try_decode_upper(value)

        value = adapter.get('weight')
        adapter['weight'] = p.try_turn_float(value)

        for field in fields:
            if field in ['sku', 'EAN']:
                value = adapter.get(field)
                adapter[field] = p.try_turn_int(value)

        value = adapter.get('category')
        adapter['category'] = p.parse_category(value)

        value = adapter.get('sub_category')
        adapter['sub_category'] = p.parse_category(value, sub_category = True)

        return item

class SaveToMySQL:
    def __init__(self):
        pass