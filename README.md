# Telegram Bot - Traffic news for my commute

I have created a Telegram Bot to send me traffic news about my commute route. The news are scrapped from RTHK site based on specified location keywords.

## Getting Started

- Create a telegram account
- Create a bot and a chat group (See [Telegram Bot API](https://core.telegram.org/bots) to learn more)
- Clone this project and install the required libraries with:

```shell
    $ pip install -r requirements.txt
```
- Create `.env` in the project directory and assign value to below variables 
    - `<CHAT_IDS>`: Channel ID(s) where messages are sent to
    - `<TOEKN>`: Each bot is given a unique authentication token
```
    CHAT_IDS = <your CHAT_ID>, #separated by comma if you want more than one
    TOKEN = <your TOEKN>
```
- Open `tg_bot_traffic_news_scraper.py` and revise the value of `LOC_KWS` which fits your need
- Host it on your server