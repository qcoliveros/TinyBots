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
Refer to *Setup OAuth2 Authentication for Gmail account* for the information needed to provide under *Mail* section.

## Setup OAuth2 Authentication for Gmail account
1. Sign in to **Google Cloud console** and create a *New Project* or continue with an existing project.
2. Go to *APIs and Services*.
3. Configure OAuth consent.
    3.1. Click *OAuth consent screen*.
    3.2. Provide the following information:
        * App name
        * User support email
        * Email addresses
    3.3. Click *Save and Continue*
4. Create credentials.
    4.1. Click *Credentials*.
    4.2. Click *Create Credentials* then click *OAuth client ID*.
    4.3. Provide the following information:
        * Application type: Desktop app
        * Name
    4.4. Click *Create*.
    4.5. Download the OAuth client JSON file.
