import requests

url = 'http://localhost:8000/devices/'

myobj = {
    'id':0,
    'name':'UBU-CLI-LYO-0003',
    'os':'ubuntu 22.04'
}

requests.post(url, json=myobj)