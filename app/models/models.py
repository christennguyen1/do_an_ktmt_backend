def serialize_item(item):
    item['_id'] = str(item['_id'])  # Chuyển ObjectId thành string
    return item
