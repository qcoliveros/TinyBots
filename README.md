# About TinyBots
A Telegram chatbot that can send and receive email messages using a Gmail account.

## Setup in Local Workspace
1. Install Python 3.

```
sudo apt install python3
```
2. Install the following Python modules:
    - argparse
    - configparser
    - imaplib2
    - lxml
    - pyTelegramBotAPI

 ```
 pip install <module>
 ```
3. Clone the repository locally.

```
git clone https://github.com/mcoliveros/TinyBots.git TinyBots
cd TinyBots
```
4. Setup the configuration file.
    1. Create the application.conf file by copying from application.conf.example.
    2. Update the content of application.conf file.
        - Refer to *[Setup Telegram Bot](#setup-the-telegram-bot)* for the information needed to provide under *Telegram* section.
        - The authentication method is set to OAuth2 by default. Refer to *[Setup OAuth2 Authentication for Gmail account](#setup-oauth2-authentication-for-gmail-account)* for the information needed to provide under *Mail* - *OAuth2* section. However, the authentication method can be changed to app password by setting "AuthenticationMethod" to "AppPassword". Refer to *[Setup App Password in Gmail account](#setup-app-password-in-gmail-account)* for the information needed to provide under *Mail* - *AppPassword* section.

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
2. Under *Signing in to Google*, select *App Passwords*.<br/>
    Note: If the App Password option is not showing, it might be because:<br/>
    (a) 2-Step Verification is not set up for the Google account;<br/>
    (b) 2-Step Verification is only set up for security keys;<br/>
    (c) the Google account is associated with work, school, or other organization;<br/>
    (d) Advanced Protection is turned on. Modify the existing setup accordingly and then complete Step 2 onwards.<br/>
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

## Setup the EC2 Instance in AWS LMS

1. Go to AWS Learners Lab: https://www.awsacademy.com/LMS_Login

2. Click on "Student Login" and enter your student email address and password to login.

3. On your dashboard, click on the "AWS Academy Learner Lab" icon.

4. On the left just beside the side panel, click on "Modules". This will lead you to the Learner lab options.

5. Click on "Learner Lab". This will open the leaner lab terminal console.

6. In order for you to be able to access the AWS console, click on "Start Lab" from the upper right options in the screen.

7. Wait for the AWS button to turn green and click the same "AWS" letters to get directed to the AWS Management console.

8. In the AWS console page. Navigate to EC2.

9.	Create a new EC2 instance with the following specifications:

    Name: TinyBots
    
    Application and OS Images:  Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
    
    Instance Type: t2.micro
    
    Key pair name: vockey
    
    Network settings: Allow SSH traffic from > Anywhere 0.0.0.0/0
    
10.	Launch the EC2 instance

11.	Create an Elastic IP
    
    a.	Go to Network and Security > Elastic Ips
    
    b.	Click Allocate Elastic IP address
    
    c.	Click the Elastic IP that you have created
    
    d.	Click Associate Elastic IP Address
    
    e.	Select the TinyBots instance
    
12.	Open PuTTY
    
    a.	Session > Host Name (Elastic IP)
    
    b.	SSH > Auth (PEM / PPK file)

13.	Login as: ubuntu

14.	In the terminal
    
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

