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
    * lxml
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

```
cp application.conf.example application.conf
```
* Refer to *[Setup OAuth2 Authentication for Gmail account](#setup-oauth2-authentication-for-gmail-account)* for the information needed to provide under *Mail* section.
* Refer to *[Setup Telegram Bot](#setup-the-telegram-bot)* for the information needed to provide under *Telegram* section.


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
    2. On the *OAuth consent screen*, click *Create*.
    3. Provide the following information:
        * App name
        * User support email: *[Provide the same email address]*
        * Email addresses: *[Provide the same email address]*
    4. Click *Save and Continue*.
    5. On the *Scopes*, click *Save and Continue* again.
    6. On the *Test users*, click *Add Users*.
    7. Specify the test user. *[Provide the same email address]*
    8. Click *Save and Continue*.
4. Create credentials.
    1. Click *Credentials*.
    2. Click *Create Credentials* then click *OAuth client ID*.
    3. Provide the following information:
        * Application type: Desktop app
        * Name
    4. Click *Create*.
    5. Download the OAuth client JSON file.
5. Based on the OAuth client information, generate the refresh token using the *oauth2.py* tool.

```
python3 OAuth2.py -c application.conf [--generate_permission_url/--generate_refresh_token]
```

6. Publish the application.
    1. Click *OAuth consent screen*.
    2. Click *Publish App*.
    3. Click *Confirm* to push to production.


## Setup the Telegram Bot
1. Start a new conversation with the BotFather.
2. Send /newbot to create a new Telegram bot.
3. Enter the name for the bot.
4. Give the Telegram bot a unique username.
5. Copy and save the Telegram bot's access token.
6. Send /setprivacy to disable the privacy mode.
7. Specify the bot's username created in step 4.
8. Select disable for the bot to receive all messages send to the group.
9. Add the Telegram bot to the chat group.
10. Get the list of updates for your Telegram bot:

```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```
11. Look for the "chat" object of the group to get the chat id.
