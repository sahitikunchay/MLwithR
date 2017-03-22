import json
import requests
import time
import urllib
from dbhelper import DBHelper

db = DBHelper()

TOKEN = "<Your Telegram Token Here>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def getUrl(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def getJSONfromUrl(url):
    content = getUrl(url)
    js = json.loads(content)
    return js

def getUpdates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = getJSONfromUrl(url)
    return js

def getLastUpdateId(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handleUpdates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            items = db.getItems(chat)
            if text == "/done":
                keyboard = buildKeyboard(items)
                sendMessage("Select an item to delete", chat, keyboard)
            elif text in items:
                db.deleteItem(text, chat)
                items = db.getItems(chat)
                keyboard = buildKeyboard(items)
                sendMessage("Select an item to delete", chat, keyboard)
            else:
                db.addItem(text, chat)
                items = db.getItems(chat)
            message = "\n".join(items)
            sendMessage(message, chat)
        except KeyError:
            pass

def getLastChatIdAndText(updates):
    numberOfUpdates = len(updates["result"])
    lastUpdate = numberOfUpdates - 1
    text = updates["result"][lastUpdate]["message"]["text"]
    chatID = updates["result"][lastUpdate]["message"]["chat"]["id"]
    return (text, chatID)

def buildKeyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
    
def sendMessage(text, chatID, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chatID)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    getUrl(url)

def main():
    db.setup()
    lastUpdateId = None
    while True:
        updates = getUpdates(lastUpdateId)
        if len(updates["result"]) > 0:
            lastUpdateId = getLastUpdateId(updates) + 1
            handleUpdates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
