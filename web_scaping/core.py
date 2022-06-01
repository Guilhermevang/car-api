from bs4 import BeautifulSoup
import requests
import re
from objConfig import obj_config
import json
import uuid

"""

Brands:
  tesla-brand-197, dodge-brand-32, alfa-romeo-brand-11, aston-martin-brand-36,
  lamborghini-brand-38, renault-brand-99, toyota-brand-40, rolls-royce-brand-109,
  volkswagen-brand-80, koenigsegg-brand-28, bmw-brand-86, chevrolet-brand-156...
  
Site:
  https://www.auto-data.net

"""

brand_name = 'tesla-brand-197'
standard_url = 'https://www.auto-data.net'
scrap_url = f'{standard_url}/en/{brand_name}/'

def call(url):
  req = requests.get(url)
  return BeautifulSoup(req.text, 'html.parser')

def getCarsList():
  soup = call(scrap_url)
  table = soup.find('ul', { 'class': 'modelite' })
  cars_links = table.find_all('a', { 'class': 'modeli' })
  cars_list = []

  for car_link in cars_links:
    car_generations = getCarGenerations(car_link["href"])
    for generation_url in car_generations:
      power_models = getCarPowerModels(generation_url)
      for power_model_url in power_models:
        info = getCarInfo(power_model_url)
        cars_list.append(info)
  return cars_list

def getCarGenerations(url):
  car_url = f'{standard_url}{url}'
  soup = call(car_url)
  generation_cards = soup.find_all('a', { 'class': 'position' })
  urls = []

  last_generation_url = None
  for card in generation_cards:
    if last_generation_url != card['href']:
      urls.append(card['href'])
    last_generation_url = card['href']
  return urls

def getCarPowerModels(url):
  generation_url = f'{standard_url}{url}'
  soup = call(generation_url)
  power_models = soup.find_all('tr', { 'class': 'i' })
  urls = []

  last_power_model_url = None
  for model in power_models:
    power_model_url = model.find('a')['href']
    if last_power_model_url != power_model_url:
      urls.append(power_model_url)
    last_power_model_url = power_model_url
  return urls

def getCarInfo(url):
  power_model_url = f'{standard_url}{url}'
  soup = call(power_model_url)
  info = {}

  table = soup.find('table', { 'class': 'cardetailsout car2' })
  table_rows = table.find_all('tr')

  for row in table_rows:
    if row.get('class') != ['no']:
      header, value = (row.th, row.td)
      clean_header = header.text.strip().lower()
      header_text = obj_config.get(clean_header)
      if header_text:
        info[header_text] = value.text.strip()
  info['id'] = str(uuid.uuid4())
  return info

cars_list = getCarsList()

# OPEN JSON FILE, SET IT TO A VARIABLE AND ADD THE NEW DATA TO IT
data = []
with open('../data.json', 'r') as json_file:
  data = json.load(json_file)
  data.extend(cars_list)
  with open('../data.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)