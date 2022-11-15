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
    * pyTelegramBotAPI

 ```
 pip install <module>
 ```
3. Clone the repository locally.

```
git clone https://github.com/mcoliveros/TinyBots.git TinyBots
cd TinyBots
```
4. Setup the configuration file.
    * Refer to *Setup OAuth2 Authentication for Gmail account* for the information needed to provide under *Mail* section.
    * Refer to *Setup Telegram Bot* for the information needed to provide under *Telegram* section.

```
cp application.conf.example application.conf
```


## Execute the Forwarder
1. To run the Gmail to Telegram forwarder:

```
python3 MailToTelegramForwarder.py -c application.conf 
```

2. To run the Telegram to Gmail forwarder:

```
python3 TelegramToMailForwarder.py -c application.conf 
```


## Setup OAuth2 Authentication for Gmail account
1. Sign in to **Google Cloud console** and create a *New Project* or continue with an existing project.
2. Go to *APIs and Services*.
3. Configure OAuth consent.
    1. Click *OAuth consent screen*.
    2. Provide the following information:
        * App name
        * User support email: <Provide the same email address>
        * Email addresses: <Provide the same email address>
    3. Click *Save and Continue*
4. Create credentials.
    1. Click *Credentials*.
    2. Click *Create Credentials* then click *OAuth client ID*.
    3. Provide the following information:
        * Application type: Desktop app
        * Name
    4. Click *Create*.
    5. Download the OAuth client JSON file.
5. Based on the OAuth client information, generate the refresh token using the Google Gmail tool: https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
6. Publish the application.
    1. Click *OAuth consent screen*.
    2. Click *Publish App*.
    3. Click *Confirm* to push to production.


## Setup the Telegram Bot
1. Start a new conversation with the BotFather.
2. Send /newbot to create a new Telegram bot.
3. When asked, enter a name for the bot.
4. Give the Telegram bot a unique username.
5. Copy and save the Telegram bot's access token.
6. Add the Telegram bot to the chat group.
7. Get the list of updates for your Telegram bot:

```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```
8. Look for the "chat" object to get the chat id.