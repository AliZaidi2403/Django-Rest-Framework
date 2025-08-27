import requests

endpoint = "http://127.0.0.1:8000/api/"

get_response = requests.get(endpoint, params={"abc": 123}, json={"query": "hello world"})

print(get_response.status_code) #return the status code of the response
print(get_response.text) # return the response body as a string 
print(get_response.json()) #it parses the JSON response body and gives you the corresponding Python object (list or dict).\
#Lets take two examples of JSON response body:
#1 { "id": 1, "name": "Ali", "active": true}
#res.json() will return {'id': 1, 'name': 'Ali', 'active': True}
#2 [ { "id": 1, "name": "Ali", "active": true}, { "id": 2, "name": "Veli", "active": false} ]
#res.json() will return [{'id': 1, 'name': 'Ali', 'active': True}, {'id': 2, 'name': 'Veli', 'active': False}]