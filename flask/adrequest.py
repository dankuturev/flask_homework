import requests

response = requests.post('http://127.0.0.1:5000/ads/',
                         json={'header': 'Куплю слона', 'description': 'Ну вот реально хочу купить слона',
                               'owner': 'vasyan666'})
print(response.status_code)
print(response.json())