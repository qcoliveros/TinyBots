# About TinyBots
A Telegram chatbot that can send and receive email messages using a Gmail account.

## Installation
1. Install Python 3.
```
sudo apt install python3
```
2. Install the following Python modules:
    * argparse
    * configparser
    * imaplib2
    * logging
    * python-telegram-bot
 ```
 pip install <module>
 ```
3. Clone the repository locally.
```
git clone https://github.com/mcoliveros/TinyBots.git TinyBots
cd TinyBots
```
4. Setup the configuration file.
```
cp application.conf.example application.conf
```