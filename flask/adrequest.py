import requests

# response = requests.post('http://127.0.0.1:5000/ads/',
                         # json={'header': 'Продам пепелац', 'description': 'Продам пепелац с гравицапой',
                               # 'owner': 'portvein777'})
response = requests.get('http://127.0.0.1:5000/ads/6')
print(response.status_code)
print(response.json())
