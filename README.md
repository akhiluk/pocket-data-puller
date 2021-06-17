# Pocket Data Puller

## For lack of a better name.

### About

A simple Python program that connects to the read-it-later/bookmarking service [Pocket](https://getpocket.com). Upon authentication, it can fetch article titles, URLs and word counts for the items you've saved.

You can specify the state of the articles to retrieve (unread, archived, or both) and the number of articles to fetch.

All of this data is dumped into a CSV file titled `pocket-data.csv`

### Quickstart

1. Sign up at the [Pocket Developers website](https://getpocket.com/developer/docs/overview) and get yourself a `consumer key` for a web app.
2. Clone this repo and paste the `consumer key` into the `config-example.yaml` file.
3. Rename `config-example.yaml` to `config.yaml`.
4. Run `init.py`. This program consists of a one-time setup that lets you authorize the program to **retrieve** items from your Pocket list and archive.
5. Run `pull.py` to collect the data from your Pocket account using the Pocket v3 API. Use command-line arguments to specify article state and count.

### Command line usage

`pull.py [Options]`

#### Options

| Option | Description |
| :---   | :---        |
| -s, --state| Set the state of articles to be retrieved.<br>Allowed values include:<br>`all` (fetches items in your to-read list **and** the archive),<br>`unread` (fetches only the items in your to-read list) or<br>`archive` (fetches items in your achive).<br>Default value is `all`.|
| -c, --count| Specify the number of articles to fetch. Provide any value between `1` and `10,000`.<br>The default value is `10,000`. It is overkill but enough to reliably <br>fetch **all** the articles from a typical user's archive.|
| -t, --time| Include this parameter to fetch articles that have been added/modified since<br> the last execution of this program. Especially useful if you're running the<br> program after a while and don't want to download your whole archive again.|

#### Examples

`$ python pull.py -s all -c 500`<br>
`$ python pull.py --state all --count 500`

Fetches the 500 most-recent articles from both your to-read list and your archive.

`$ python pull.py -s unread -c 10`<br>
`$ python pull.py --state unread --count 10`

Fetches the 10 most-recent articles from your to-read list.

`$ python pull.py -s unread -c 10 -t`<br>
`$ python pull.py --state unread --count 10 --time`

Gets you the 10 most-recent unread articles that have been added since the last time the program was executed. Very useful when fetching new items after a week or month.

### Closing words

A very simple program with some avenues for improvement. The whole thing was written in an afternoon in 2020 for personal use, and re-written in 2021. If you have suggestions or critiques, I'd love to hear them.