# Importing the required libraries
import requests
import pandas as pd
import webbrowser
import config
import time

# Requesting the request token from Pocket's v3 API. We are passing the secret Consumer Key
# and a redirect URI the v3 OAuth URL.
print("Getting code...")
params = {'consumer_key': config.consumer_key, 'redirect_uri': config.redirect_uri}
r = requests.post('https://getpocket.com/v3/oauth/request', data=params)
print("Response code: %s" % r.status_code)

# Let us now save the request token that arrived as a response.
code = r.text[5:]
print("Code: %s" % code)

# Now the user needs to authorize the application.
# We open up the authorization page on Pocket, passing the request token and redirect URI
# along with it.
print("Setting up authorization page...")
url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}'.format(code, config.redirect_uri)
print(url)
webbrowser.open_new_tab(url)

# Waiting till the user has a chance to authorize before sending the next request.
time.sleep(5)
print("5 more seconds...")
time.sleep(5)
print("Done...")

# Once the user has (hopefully) granted permission, we request an access token from Pokcet.
newParams = {'consumer_key': config.consumer_key, 'code': code}
x = requests.post('https://getpocket.com/v3/oauth/authorize', data=newParams)
print("Requesting access token...")
print("Response code: %s" % x.status_code)

# Store the access token and the username for future use (and printing it, just because).
access_token = x.text[13:43]
username = x.text[53:]
print("Access token: %s" % access_token)
print("Username: %s" % username)

# Using the secret Consumer Key and access token, we request 10,000 articles from the user's account.
# The articles may be read or unread.
# The '10,000' is an arbitrary number. It might be more than enough if you have <10,000 articles.
# This value of 10,000 can be modified if there are more than 10,000 articles in the user's archive.
xload = {'consumer_key': config.consumer_key, 'access_token' : access_token, 'state': 'all', 'contentType': 'article', 'detailType':'complete', 'count': 10000}
print("Requesting ALL of your saved items from Pocket...")
allData = requests.post('https://getpocket.com/v3/get', data= xload)
print("Response code: %s" % allData.status_code)
print("Data received. Processing it now...")

# Converting the response to JSON, and then extracting only the required list data into the
# variable requiredData.
allData_dictionary= allData.json()
requiredData = allData_dictionary['list']

# We now need to iterate through all the articles and fetch the title, links and word-counts for the articles.
# Once these values have been fetched, we save the values to a dataframe.
# A CSV file titled 'Pocket-Data.csv' is then generated.
cols = ['Title', 'Link']
lst = []
for p_id, p_info in requiredData.items():
    title= p_info['given_title']
    link= p_info['given_url']
    lst.append([title, link])
df = pd.DataFrame(lst,columns=cols)
pocket_csv_data = df.to_csv('Pocket-Data.csv', index = True)
print("All done! You'll find the Pocket-Data.csv file in the directory.")