import json

with open('supermarkets_google_places.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total = sum(len(v) for v in data.values())

print(f'Cadenas encontradas: {len(data)}')
print(f'Total supermercados: {total}')
print('\nPor cadena:')
for k, v in data.items():
    print(f'  {k}: {len(v)} supermercados')
