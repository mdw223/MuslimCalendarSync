import requests

def get_public_ip():
    ip_response = requests.get("https://api.ipify.org?format=json")
    ip_data = ip_response.json()
    public_ip = ip_data['ip']
    return public_ip

def get_geo_data_from_public_ip(public_ip):    
    geo_response = requests.get(f"https://ipapi.co/{public_ip}/json/")
    geo_data = geo_response.json()
    return geo_data

public_ip = get_public_ip()
geo_data = get_geo_data_from_public_ip(public_ip)

city = geo_data['city']
region = geo_data['region'] 
region_short = geo_data['region_code'] 
country = geo_data['country_name'] # United States
county_short = geo_data['country_code'] #US
latitude = geo_data['latitude']
longitude = geo_data['longitude']

print(f"City: {city}")
print(f"Region: {region}")
print(f"Country: {country}")
print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")

# ask user to input either IP address or Country and zipcode