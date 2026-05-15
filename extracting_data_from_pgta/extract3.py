import json

def extract_pgta_data(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        return "Unknown", {}

    title = "Unknown"
    json_obj = {}

    title_idx = data.find(b'TITL')
    if title_idx != -1:
        start = title_idx + 8
        end = data.find(b'\x00', start)
        if end != -1:
            title = data[start:end].decode('utf-8', errors='ignore')

    json_idx = data.find(b'{"loc"')
    if json_idx != -1:
        end = data.find(b'\x00', json_idx)
        if end != -1:
            json_string = data[json_idx:end].decode('utf-8', errors='ignore')
            try:
                json_obj = json.loads(json_string)
            except json.JSONDecodeError:
                pass 

    return title, json_obj


def getJsonFields(json_obj, field_name, alt_value = 'none'):
    return json_obj.get(field_name) or alt_value