import requests
import pandas as pd
import webbrowser
import config

params = {'consumer_key': config.consumer_key, 'redirect_uri': config.redirect_uri}
r = requests.post('https://getpocket.com/v3/oauth/request', data=params)
print(r.status_code)

config.code = r.text[5:]

url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}'.format(config.code, config.redirect_uri)
print(url)
webbrowser.open_new_tab(url)

newParams = {'consumer_key': config.consumer_key, 'code': config.code}
x = requests.post('https://getpocket.com/v3/oauth/authorize', data=newParams)
print(x.status_code)

config.access_token = x.text[13:43]
config.username = x.text[53:]

xload = {'consumer_key': config.consumer_key, 'access_token' : config.access_token, 'state': 'all', 'contentType': 'article', 'detailType':'complete', 'count': 10000}
print(xload)
allData = requests.post('https://getpocket.com/v3/get', data= xload)
print(allData.status_code)

allData_dictionary= allData.json()
requiredData = phi_dictionary['list']

i=1
cols = ['Article No.', 'Word Count']
lst = []
for p_id, p_info in requiredData.items():
    count= p_info['word_count']
    lst.append([i, count])
    i+=1
df = pd.DataFrame(lst,columns=cols)
pocket_csv_data = df.to_csv('Pocket-Data.csv', index = True)