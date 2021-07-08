# Importing the required libraries
import pandas as pd
import yamli as y
import requests
import getopt
import sys
import os

def process_results(user_data):
    
    # Converting the response received into JSON. Then we extract the info we actually need, which is contained in the dictionary element 'list'.
    user_data_dict = user_data.json()
    time_since = user_data_dict['since']
    y.set_yaml_value('time_since', time_since)
    required_data = user_data_dict['list']

    # We now need to iterate through all the articles and fetch the title, link and word count for each article.
    # Once these values have been fetched, we save the values to a dataframe.
    # A CSV file titled 'pocket-data.csv' is then generated.
    cols = ['Link', 'Word Count']
    item_list = []
    for p_id, p_info in required_data.items():
        if p_info['status'] == '2':
            # Every item in a user's Pocket storage has a status indicator.
            # Status code 0 indicates the item is in their to-read list.
            # Status code 1 indicates the item is in their archive.
            # Status code 2 indicates the item has been deleted. So if an item has a status code set to 2, there is no useful metadata we
            # can get from it. In such cases, we simply continue with our loop.
            continue
        else:
            title = p_info['resolved_title']
            link = p_info['given_url']
            word_count = p_info['word_count']
            item_list.append([title, link, word_count])
    df = pd.DataFrame(item_list, columns=cols)
    pocket_csv_data = df.to_csv('pocket-data.csv', index = False)

def retrieve(consumer_key, access_token, item_state, item_count):

    # A helper method to retrieve 'item_count' articles since Day 1.
    print("Requesting {} of your articles from Pocket...\nThis might take a while, please be patient.".format(item_count))
    xload = {'consumer_key': consumer_key, 'access_token': access_token, 'state': item_state, 'contentType': 'article', 'detailType': 'complete', 'count':item_count}
    all_data = requests.post('https://getpocket.com/v3/get', data = xload)
    return all_data

def retrieve_since(consumer_key, access_token, item_state, item_count, time_since):

    # A helper method to retrieve 'item_count' articles added/modified since the time stamp provided.
    print("Requesting {} of your articles from Pocket...\nThis might take a while, please be patient.".format(item_count))
    xload = {'consumer_key': consumer_key, 'access_token': access_token, 'state': item_state, 'contentType': 'article', 'detailType': 'complete', 'count': item_count, 'since': time_since}
    all_data = requests.post('https://getpocket.com/v3/get', data = xload)
    return all_data   

if __name__ == '__main__':

    # Handling user-provided parameters to get values that will be needed for retrieving the results.
    argument_list = sys.argv[1:]
    options = "s:c:t"
    long_options = ["state =", "count =", "time"]
    item_state = "all"
    item_count = 10000
    get_time_since_last_search = False

    # Checking for the existance of user-provided parameters and performing some basic checks for argument values.
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-s", "--state"):
                item_state = currentValue
                if item_state not in ("all", "archive", "unread"):
                    print("Invalid value for argument --state OR -s: Allowed values are 'all', 'archive' or 'unread'.")
                    os._exit(0)
            elif currentArgument in ("-c", "--count"):
                item_count = int(currentValue)
                if item_count < 1 or item_count > 10000:
                    print("Invalid value for argument --count OR -c: Choose a number between 1 and 10000")
                    os._exit(0)
            elif currentArgument in ("-t", "--time"):
                get_time_since_last_search = True
    except getopt.error as runtime_error:
        print(str(runtime_error))
    
    # Getting the two values from config.yaml that will be needed for retrieving the results.
    consumer_key = y.get_yaml_value('consumer_key')
    access_token = y.get_yaml_value('access_token')

    if(get_time_since_last_search == True):
        time_since = str(y.get_yaml_value('time_since'))
        if len(time_since) < 5:
            all_data = retrieve(consumer_key, access_token, item_state, item_count)
        else:
            all_data = retrieve_since(consumer_key, access_token, item_state, item_count, time_since)
    else:
        all_data = retrieve(consumer_key, access_token, item_state, item_count)
    print("Response status code: %s" % all_data.status_code)

    # All the data has been received from Pocket. Now we need to process it to get what we actually want, which is the article title, its URL and the word count.
    # This processing produces a CSV file in the same directory.
    print("Data received. Processing it now...")
    process_results(all_data)
    print("All done! You'll find the results in the 'pocket-data.csv' file.")
    # The final data is now in the 'pocket-data.csv' file. What can you do with it? That's entirely up to you. Use this as a backup method of all the links you've
    # saved, or to calculate how many words you've read over the years. You get to choose what to do with your data.