# Importing the required libraries
import requests
import pandas as pd
import webbrowser
import config

# Requesting the request token from Pocket's v3 API. We are passing the secret Consumer Key
# and a redirect URI the v3 OAuth URL.
params = {'consumer_key': config.consumer_key, 'redirect_uri': config.redirect_uri}
r = requests.post('https://getpocket.com/v3/oauth/request', data=params)
print(r.status_code)

# Let us now save the request token that arrived as a response.
config.code = r.text[5:]

# Now the user needs to authorize the application.
# We open up the authorization page on Pocket, passing the request token and redirect URI
# along with it.
url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}'.format(config.code, config.redirect_uri)
print(url)
webbrowser.open_new_tab(url)

# Once the user has (hopefully) granted permission, we request an access token from Pokcet.
newParams = {'consumer_key': config.consumer_key, 'code': config.code}
x = requests.post('https://getpocket.com/v3/oauth/authorize', data=newParams)
print(x.status_code)

# Store the access token and the username for future use.
config.access_token = x.text[13:43]
config.username = x.text[53:]

# Using the secret Consumer Key and access token, we request 10,000 articles from the user's account.
# The articles may be read or unread.
# The '10,000' is an arbitrary number. It might be more than enough if you have <10,000 articles.
# This value of 10,000 can be modified if there are more than 10,000 articles in the user's archive.
xload = {'consumer_key': config.consumer_key, 'access_token' : config.access_token, 'state': 'all', 'contentType': 'article', 'detailType':'complete', 'count': 10000}
print(xload)
allData = requests.post('https://getpocket.com/v3/get', data= xload)
print(allData.status_code)

# Converting the response to JSON, and then extracting only the required list data into the
# variable requiredData.
allData_dictionary= allData.json()
requiredData = phi_dictionary['list']

# We now need to iterate through all the articles and fetch the values for 'word_count'.
# Once the word counts for all the articles have been fetched, we save the values to a dataframe.
# A CSV file titled 'Pocket-Data.csv' is then generated.
i=1
cols = ['Article No.', 'Word Count']
lst = []
for p_id, p_info in requiredData.items():
    count= p_info['word_count']
    lst.append([i, count])
    i+=1
df = pd.DataFrame(lst,columns=cols)
pocket_csv_data = df.to_csv('Pocket-Data.csv', index = True)