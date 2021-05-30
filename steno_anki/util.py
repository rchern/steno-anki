def generate_identifier(s):
    return int.from_bytes(s.encode(), 'little')

def split_strip(items, separator):
    return map(lambda i: i.strip(), items.split(separator))
