from unidecode import unidecode
def try_index_strip(value):
    # this function applies on all fields except for 'sub_category'
    try:
        return value[0].strip()
    except IndexError:
        return value
    except  AttributeError:
        return value[0]

def try_decode_upper(value):
    # this function applies on the fields ['product', 'brand', 'manufacturer', 'description']
    try:
        return unidecode(value.upper())
    except AttributeError:
        return value

def try_turn_float(value):
    # this function applies only to the 'weight' field
    try:
        return float(value)
    except AttributeError:
        return value

def try_turn_int(value):
    # this function applies only to the 'sku' and 'EAN' fields
    try:
        return int(value)
    except AttributeError:
        return value

def parse_category(value: str, sub_category = False) -> str:
    # this function parses the categories
    values_list = value.split('/')

    if not sub_category:
        return values_list[-2].upper()

    return values_list[-1].upper().replace('.HTML', "")