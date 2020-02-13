import requests
import urllib
import time
import telegram
import re
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import logging

# settings
load_dotenv()
CHAT_IDS = [id for id in os.getenv('CHAT_IDS').split(',') if id]
TOKEN = os.getenv('TOKEN')

# logger config
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, handlers=[logging.FileHandler('file.log')])

# keywords
LOC_KWS = ['廣福邨', '吐露港', '大埔滘', ' 大埔公路', '科學園',
                '大老山', '彩虹', '啟業', '九龍灣', '觀塘', '牛頭角']

def init_bot(token):
    bot = telegram.Bot(token=token)
    logging.info('bot created')
    return bot


def send_message_to_ids(bot, chat_ids, message):
    if message:
        for id in chat_ids:
            bot.send_message(id, message)
        logging.info('News sent.')
    else:
        logging.info('No update.')
        return


def scrape_news(loc_kws):
    url = urllib.request.urlopen(
        'http://programme.rthk.hk/channel/radio/trafficnews/index.php')

    soup = BeautifulSoup(url, "lxml")

    # scrape updates
    updates = soup.findAll(class_='inner')
    refreshed_updates = {}
    for update in updates:
        date_time = update.contents[1].text
        content = update.contents[0].strip()

        # check if content contains LOC_KEYWORDS
        if any([True for kw in loc_kws if(kw in content)]):
            key = str(re.sub("[^\d+]", "", date_time)) + \
                '-' + str(content)
            refreshed_updates[key] = {
                'date_time': date_time, 'content': content}

    # get where is not in previous updates
    try:
        new_updates = {k: refreshed_updates[k] for k in sorted(
            refreshed_updates) if k not in previous_updates.keys()}
    except NameError:
        new_updates = {k: refreshed_updates[k]
                       for k in sorted(refreshed_updates)}

    # create previous updates
    global previous_updates
    previous_updates = refreshed_updates

    if new_updates:
        message = "=====交通消息====="
        for update in new_updates.values():
            message += "\n" + update['date_time']
            message += "\n" + update['content'] + '\n'
        logging.info('News updated!')
        return message.strip()


# init bot
bot = init_bot(TOKEN)

# loop
while True:
    try:
        message = scrape_news(LOC_KWS)
        send_message_to_ids(bot, CHAT_IDS, message)
        time.sleep(10)
    except Exception as e:
        logging.error(e)
        break
