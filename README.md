# About TinyBots
A Telegram chatbot that can send and receive email messages using a Gmail account.

## Setup in Local Workspace
1. Install Python 3 and pip.

```
sudo apt install python3
sudo apt install python3-pip
```
2. Install the following Python modules:
    - argparse
    - configparser
    - imaplib2
    - lxml
    - pyTelegramBotAPI

 ```
 sudo pip install <module>
 ```
3. Clone the repository locally.

```
git clone https://github.com/mcoliveros/TinyBots.git TinyBots
cd TinyBots
```
4. Create the configuration file.

```
cp application.conf.example application.conf
```
* Refer to *[Setup Telegram Bot](#setup-the-telegram-bot)* for the information needed to provide under *Telegram* section.
* The authentication method is set to OAuth2 by default. Refer to *[Setup OAuth2 Authentication for Gmail account](#setup-oauth2-authentication-for-gmail-account)* for the information needed to provide under *Mail* - *OAuth2* section. However, the authentication method can be changed to app password by setting "AuthenticationMethod" to "AppPassword". Refer to *[Setup App Password in Gmail account](#setup-app-password-in-gmail-account)* for the information needed to provide under *Mail* - *AppPassword* section.


5. Open a terminal and run the Gmail to Telegram forwarder.
    
```
python3 MailToTelegramForwarder.py -c application.conf 
```
6. Open another terminal and run the Telegram to Gmail forwarder.

```
python3 TelegramToMailForwarder.py -c application.conf 
```

## Setup in AWS LMS
1. Sign in to *[AWS Learners Lab](https://www.awsacademy.com/vforcesite/LMS_Login)*.
2. On the *Dashboard*, click *AWS Academy Learner Lab*.
3. Click *Modules*.
4. Click *Learner Lab*. This will launch the leaner laboratory terminal console.
5. Click *Start Lab* to access the AWS console.
6. Wait for the *AWS* button to turn green, then click the same *AWS* letters to get directed to the *AWS Management Console*.
7. Navigate to *EC2* page.
8. Create a new EC2 instance with the following specifications:
    - *Name:* IS238-Project-TinyBots
    - *Application and OS Images:* Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
    - *Instance type:* t2.micro
    - *Key pair name:* vockey
    - *Security group name:* IS238-Project-TinyBots-Security-Group
    - *Security group rule 1:* Allow SSH traffic from My IP
    - *Security group rule 2:* Allow Custom TCP 993 from Anywhere 0.0.0.0/0<br/>
       Note: For IMAP.
    - *Security group rule 3:* Allow Custom TCP 465 from Anywhere 0.0.0.0/0<br/>
       Note: For SMTP using implicit SSL/TLS.
    - *Security group rule 4:* Allow Custom TCP 587 from Anywhere 0.0.0.0/0<br/>
       Note: For SMTP using explicit SSL/TLS.
    - *Security group rule 5:* Allow HTTPS from Anywhere 0.0.0.0/0<br/>
       Note: For Telegram.
9. Click *Launch instance*.
10. Create an Elastic IP.
    1. Go to *Network & Security* > *Elastic IPs*.
    2. Click *Allocate Elastic IP address*.
    3. Click *Add new tag*.
    4. Provide the following:
        - *Key:* Name
        - *Value:* IS238-Project-TinyBots-Elastic-IP
    5. Click *Allocate*.
    6. Click *Actions* > *Associate Elastic IP address*.
    7. Select the *IS238-Project-TinyBots* instance.
    8. Click *Associate*.
    9. Click *Actions* > *Update reverse DNS*.
    10. Provide the following:
        - *Reverse DNS domain name:* [Provide the domain name]<br/>
            Note: Make sure to add DNS A record first based on Elastic IP address.
        - *To confirm update, type update in the field:* update
    11. Click *Update*.
11. Click *EC2 Dashboard*, then view *IS238-Project-TinyBots* instance details. Take note of its *Public IPv4 DNS*.
12. Go back to *Learner Lab*, then click *AWS Details*.
13. Download the SSH key.
14. Open a terminal and go to the SSH key location.
15. Execute the following to ensure that the SSH key is publicly viewable.

```
chmod 400 vockey.pem
```
16. Connect to *IS238-Project-TinyBots* instance via SSH using its *Public IPv4 DNS* from step 11.

```
ssh -i "vockey.pem" [Public IPv4 DNS]
```
17. Update the system package list.

```
sudo apt update && upgrade
```
18. Go to the root directory

```
sudo su
```

19. Install pip and venv.

```
sudo apt install python3-pip
sudo apt install python3-venv
```
20. Setup virtual environment.
    1. Create a folder for Python environments.
    2. Go to the created folder.
    3. Create an environment.
    4. Activate the environment to use it.

```
cd /
sudo mkdir environments
cd environments
sudo python3 -m venv tinybots-env
source tinybots-env/bin/activate
```
21. Install the following Python modules:
    - argparse
    - configparser
    - imaplib2
    - lxml
    - pyTelegramBotAPI

 ```
 pip install <module>
 ```
22. Clone the repository.

```
cd tinybots-env
mkdir source
cd source
git clone https://github.com/mcoliveros/TinyBots.git TinyBots
cd TinyBots
```
23. Create the configuration file.

```
cp application.conf.example application.conf
```
* Refer to *[Setup Telegram Bot](#setup-the-telegram-bot)* for the information needed to provide under *Telegram* section.
* The authentication method is set to OAuth2 by default. Refer to *[Setup OAuth2 Authentication for Gmail account](#setup-oauth2-authentication-for-gmail-account)* for the information needed to provide under *Mail* - *OAuth2* section. However, the authentication method can be changed to app password by setting "AuthenticationMethod" to "AppPassword". Refer to *[Setup App Password in Gmail account](#setup-app-password-in-gmail-account)* for the information needed to provide under *Mail* - *AppPassword* section.

24. Create a shell script file.
    
```
cd ..
mkdir scripts
cd scripts
nano TinyBots.sh
```
Provide the following:

```
cd /environments/tinybots-env/source/TinyBots
source /environments/tinybots-env/bin/activate
python3 MailToTelegramForwarder.py -c application.conf &
python3 TelegramToMailForwarder.py -c application.conf &
```

25. Edit the crontab.

```
crontab -e
```
Provide the following:

```
@reboot /environments/tinybots-env/scripts/TinyBots.sh
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
1. Sign in to *[Google account](https://myaccount.google.com/)*.
2. Click *Security*.
3. Under *Signing in to Google*, select *App Passwords*.<br/>
    Note: If the App Password option is not showing, it might be because:<br/>
    (a) 2-Step Verification is not set up for the Google account;<br/>
    (b) 2-Step Verification is only set up for security keys;<br/>
    (c) the Google account is associated with work, school, or other organization;<br/>
    (d) Advanced Protection is turned on. Modify the existing setup accordingly and then complete Step 2 onwards.<br/>
4. Choose *Select app*. 
5. Choose *Other (Custom name)* 
6. Provide the application name.
7. Click *Generate*.
8. Update the *AppPassword* in application.conf based on the obtained password.

## Setup OAuth2 Authentication for Gmail account
1. Sign in to *[Google Cloud console](https://console.cloud.google.com/)* and create a *New Project* or continue with an existing project.
2. Go to *APIs and Services*.
3. Configure OAuth consent.
    1. Click *OAuth consent screen*.
    2. On the *OAuth consent screen*, click *Create*.
    3. Provide the following information:
        - *App name*
        - *User support email:* [Provide the same email address]
        - *Email addresses:* [Provide the same email address]
    4. Click *Save and Continue*.
    5. On the *Scopes*, click *Save and Continue* again.
    6. On the *Test users*, click *Add Users*.
    7. Specify the test user. *[Provide the same email address]*
    8. Click *Save and Continue*.
4. Create credentials.
    1. Click *Credentials*.
    2. Click *Create Credentials* then click *OAuth client ID*.
    3. Provide the following information:
        - *Application type:* Desktop app
        - *Name*
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

