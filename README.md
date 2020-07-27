# Telegram-Fast-Food-Order-Bot-Demo
A Telegram bot written in Python3 that can be fully customized to your needs.

## Usage
Create a settings.py file on the root directory with the content:

```python
token="XXXXXXX"  #telegram bot api token
pickle_logs = "babis.log"
timeout = 900

# mongo config
mongo_host = 'localhost'
mongo_user = 'tgbot'
mongo_password = '12345678'
mongo_port = '27017'
mongo_collection = 'tgbot'

admin_list = []
CHATID = "anything" 

```
