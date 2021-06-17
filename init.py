# Importing the required libraries
import os
import requests
import webbrowser
import time
import yamli as y

if __name__ == '__main__':
    
    # Collecting the request token from Pocket's v3 API. We are passing the secret Consumer Key
    # and a redirect URI to the v3 oAuth URL.
    consumer_key = y.get_yaml_value('consumer_key')
    redirect_uri = y.get_yaml_value('redirect_uri')
    print("Getting request token from Pocket...")
    params = {'consumer_key': consumer_key, 'redirect_uri': redirect_uri}
    r = requests.post('https://getpocket.com/v3/oauth/request', data = params)
    print("Response status code: %s" % r.status_code)

    # Let us now save the request token that arrived with the response.
    request_token = r.text[5:]
    print("Request token: %s" % request_token)
    y.set_yaml_value('request_token', request_token)

    # Now the user needs to authorize the application.
    # We open up the authorization page on Pocket, passing the request toekn and redirect URI
    # along with it.
    print("Setting up authorization page...")
    url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}'.format(request_token, redirect_uri)
    webbrowser.open_new_tab(url)

    # Waiting till the user has a chance to authorize the app before sending the next request.
    time.sleep(5)
    print("Waiting 5 more seconds...")
    time.sleep(5)
    print("Done...")

    # Once the user has (hopefully) granted permission, we request an access token from Pocket.
    newParams = {'consumer_key': consumer_key, 'code': request_token}
    x = requests.post('https://getpocket.com/v3/oauth/authorize', data = newParams)
    print("Requesting access token...")
    print("Response status code: %s" % x.status_code)

    # Next we save the access token and username in the config.yaml file for future use.
    access_token = x.text[13:43]
    y.set_yaml_value('access_token', access_token)
    print("Access token: %s" % access_token)
    username = x.text[53:]
    y.set_yaml_value('username', username)
    print("Username: %s" % username)
    print("Initial set-up done! Now run pull.py with the required parameters.")
    os._exit(0)