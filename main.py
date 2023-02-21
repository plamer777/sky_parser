import json
from container import parse_manager
from utils import load_from_json


schools = load_from_json('data/school_data.json')
loaded = parse_manager.parse_all(schools)

with open('data/result.json', 'w',  encoding='utf-8') as f:
    json.dump(loaded, f)

print(loaded)








