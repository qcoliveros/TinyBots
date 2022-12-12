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
* Refer to *[Setup Telegram Bot](#setup-the-telegram-bot)* for the information needed to provide under *Telegram* section.
* The authentication method is set to OAuth2 by default. Refer to *[Setup OAuth2 Authentication for Gmail account](#setup-oauth2-authentication-for-gmail-account)* for the information needed to provide under *Mail* - *OAuth2* section. However, the authentication method can be changed to app password by setting "AuthenticationMethod" to "AppPassword". Refer to *[Setup App Password in Gmail account](#setup-app-password-in-gmail-account)* for the information needed to provide under *Mail* - *AppPassword* section.


## Execute the Forwarder
1. To run the Gmail to Telegram forwarder:

```
python3 MailToTelegramForwarder.py -c application.conf 
```

2. To run the Telegram to Gmail forwarder:

```
python3 TelegramToMailForwarder.py -c application.conf 
```

## Setup the Telegram Bot
1. Start a new conversation with the BotFather.
2. Send the following message to create a new Telegram bot:

```
/newbot
```
3. Enter the name for the bot.
4. Give the Telegram bot a unique username.
5. Update the *BotToken* in application.conf based on the obtained Telegram bot's access token.
6. Send the following message to disable the privacy mode:

```
/setprivacy
```
7. Specify the bot's username created in step 4.
8. Select disable for the bot to receive all messages sent to the group.
9. Add the Telegram bot to the chat group.
10. Get the list of updates for your Telegram bot:

```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```
11. Look for the "chat" object of the group to get the chat id.
12. Update the *ChatId* in application.conf based on the obtained chat id.


## Setup App Password in Gmail account
1. Sign in to Google account.
2. Under *Signing in to Google*, select *App Passwords*.
(Note: If the App Password option is not showing, it might be because: a) 2-Step Verification is not set up for the Google account; b) 2-Step Verification is only set up for security keys; c) the Google account is associated with work, school, or other organization; d) Advanced Protection is turned on. Modify the existing setup accordingly and then complete Step 2 onwards.)
3. Choose *Select app*. 
4. Choose *Other (Custom name)* 
5. Provide the application name.
6. Click *Generate*.
7. Update the *AppPassword* in application.conf based on the obtained password.

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
5. Based on the OAuth client information, generate the refresh token using the *OAuth2.py* tool.
    1. Generate the permission URL. 
    2. Authorize the application then update the *AuthorizeCode* in application.conf based on the obtained authorization code.
    3. Generate the refresh token.
    4. Update the *RefreshToken* in application.conf based on the obtained refresh token.

```
python3 OAuth2.py -c application.conf [--generate_permission_url/--generate_refresh_token]
```
     
6. Publish the application.
    1. Click *OAuth consent screen*.
    2. Click *Publish App*.
    3. Click *Confirm* to push to production.

## Setup the EC2 Instance
1.	Create a new EC2 instance with the following specifications:
    Name: TinyBots
    Application and OS Images:  Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
    Instance Type: t2.micro
    Key pair name: vockey
    Network settings: Allow SSH traffic from > Anywhere 0.0.0.0/0
    
2.	Launch the EC2 instance

3.	Create an Elastic IP
    a.	Go to Network and Security > Elastic Ips
    b.	Click Allocate Elastic IP address
    c.	Click the Elastic IP that you have created
    d.	Click Associate Elastic IP Address
    e.	Select the TinyBots instance
    
4.	Open PuTTY
    a.	Session > Host Name (Elastic IP)
    b.	SSH > Auth (PEM / PPK file)

5.	Login as: ubuntu

6.	In the terminal
    
    a. Install Python 3

```
sudo apt install python3
```

   b.	Install the needed modules:
argparse
configparser
imaplib2
lxml
pyTelegramBotAPI

```
pip install <module>
```
   
   c.	Clone the repository
```
git clone https://github.com/mcoliveros/TinyBots.git TinyBots
```
   
   d.	Enter your github email address/username
   
   e.	Enter your Personal Access Token
         > To generate token > Go to github > Settings > Developer Settings > Tokens (Classic) > Generate New Token
   
   f.	Access directory
```
cd TinyBots
```
   g.	Update application.config
```
sudo nano application.conf
```
   Use the following values:
[Mail]
ImapServer=imap.googlemail.com
SmtpServer=smtp.gmail.com

User=tinybots238@gmail.com

# Authentication method is defaulted to OAuth2. Possible values are 'AppPassword' and 'OAuth2'.
AuthenticationMethod=AppPassword

# If authentication method is set to 'AppPassword'.
AppPassword=ylndodbelzdawbfe

# If authentication method is set to 'OAuth2'.
#ClientId=423123225629-din3a359pudvp8ujijs4a4gbcrh7h7nb.apps.googleusercontent.com
#ClientSecret=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
#AuthUri=https://accounts.google.com/o/oauth2/auth
#TokenUri=https://oauth2.googleapis.com/token
#AuthorizeCode=4/1AfgeXvtqVwAVvW2sQWs942v9vft5T674EnoWDlwEKcroJZkOM0hfUqyLux8
#RefreshToken=1//099UWRgozvvFYCgYIARAAGAkSNwF-L9IrhkqrdbEw9WIVCaCUcdvnwa-PA-oB2RxPIlMeOI6mCROQgzg6pm-QUF7T15HCBlcPAcw

[Telegram]
BotToken=5621037330:AAHJxOqo8jUAkcVHpn1Ne8SQ208j6pzh2o0
ChatId=-845399329

[Database]
File=tinybots.db

# tinybots238@gmail.com / T1nyB0ts!
   
