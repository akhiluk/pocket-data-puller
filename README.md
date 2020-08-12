# pocket-data-puller

A simple Python script that authenticates with the read-it-later service [Pocket](https://getpocket.com/) and fetches the user's data. The word counts for **all** the articles saved by the user are then dumped into a CSV file titled 'Pocket-Data.csv'.

*Variables such as the [Pocket API Consumer Key](https://getpocket.com/developer/docs/overview) and the redirect URI will have to be manually added to a* config.py *file.*