import json

data = []
with open('data.json') as json_file:
  data = json.load(json_file)

def Find(key, value):
  for item in data:
    if value.lower() in item.get(key.lower()):
      return item
  return -1

def FindAll(key = None, value = None, limit = 10):
  if key == None and value == None:
    return(data[:limit])
    
  result = []
  for i, item in enumerate(data):
    if result.__len__() == limit:
      break
      
    if key.lower() in item.keys():
      if value.lower() in item.get(key.lower()).lower():
        result.append(item)
  return result