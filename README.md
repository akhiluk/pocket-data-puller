# Pocket Data Puller

A simple Python script that authenticates with the read-it-later service [Pocket](https://getpocket.com/) and fetches the user's data. The titles, URLs and word-counts for **all** the articles saved by the user are then dumped into a CSV file titled 'Pocket-Data.csv'.

That's all the script does as of now. More features will be added as time permits.

*Variables such as the [Pocket API Consumer Key](https://getpocket.com/developer/docs/overview) and the redirect URI will have to be manually added to a* config.py *file.*