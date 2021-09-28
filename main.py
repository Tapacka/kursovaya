import requests
import datetime
import time
from tqdm import tqdm
import json
import logging
logging.basicConfig(filename='logo.log', level=logging.DEBUG, filemode='w')
logging.debug('debug message')
logging.info('info message')

# from pprint import pprint
id_vk = input('введите id пользователя вк: ')
token_vk = input('введите токен вк: ')
url = 'https://api.vk.com/method/photos.get'
params = {'user_id': id_vk, 'access_token': token_vk, 'v': '5.131','album_id': 'profile', 'extended': '1', 'photo_sizes': '1'}
res = requests.get(url, params=params)
# pprint(res.json())

token_ya = input('введите токен Yandex: ')

def ya_headers():
  return {'Content-type': 'application/json', 'Authorization': 'OAuth {}'.format(token_ya)}


def put_folder(path):
  url = 'https://cloud-api.yandex.net/v1/disk/resources/'
  headers = ya_headers()
  params = {'path': path, 'url': url}
  response = requests.put(url,headers = headers, params = params)
  
  if response.status_code == 201:
    print('папка создана')
  elif response.status_code == 409:
    print('Папка уже существует. Файлы будут помещены в неё.')  

  return path


def post_file(file_url, file_name):
  upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
  headers = ya_headers()
  params = {'path': f'/{file_name}', 'url': file_url}
  response = requests.post(upload_url, headers = headers, params = params)
  return response.json()


    
folder_name = put_folder(input("введите имя папки для загрузки фотографий: "))
name_list = []
data = []
size_list = []

for photos in tqdm(res.json()['response']['items']):
  
  sizes = photos['sizes']


  for picture in sizes:
    size_list.append(picture['type'])
    size_list.sort(reverse=True)
    
  for picture1 in sizes:
    data_dict = {}    
    if picture1['type'] == size_list[0]:
      href = picture1['url']
      filename = photos['likes']['count']      
      if filename in name_list:
        filename = f"{photos['likes']['count']}+{datetime.datetime.fromtimestamp(photos['date']).isoformat().replace(':', '|')}"
        post_file(href, f"{folder_name}/{filename}")          
      else:
        post_file(href, f"{folder_name}/{filename}")

      data_dict['file_name'] = filename
      data_dict['size'] = picture1['type']
      data.append(data_dict)  
        
       
  name_list.append(filename)
  size_list.clear()     
      
  time.sleep(1)
with open ('foto.json', 'w') as f:
  json.dump(data, f, ensure_ascii=False, indent=2)     