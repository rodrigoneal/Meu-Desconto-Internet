import requests

url = "https://community-open-weather-map.p.rapidapi.com/weather"

querystring = {"callback":"test","id":"2172797","lang":"Portuguese - pt","units":"%22metric%22 or %22imperial%22","mode":"xml%2C html","q":"Rio de Janeiro%2Crj"}

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': "822a7712b7msh74a188351f16783p1c02fdjsn97e226bcb5fc"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)