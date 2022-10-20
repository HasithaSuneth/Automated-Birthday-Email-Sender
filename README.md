# Automated-Birthday-Email-Sender
This script generates automated birthday email messages using user data obtained from the OrangeHRM system database. 
The script requires running every day using Cronjob (Linux) or Task Scheduler (Windows).

- dbhost: Database host (Ex: localhost/127.0.0.1)
- dbusername: Database username
- dbpassword: Database user password
- database: Database name
- email_username: Email username (Ex: mail_address@domain.com)
- email_password: Email password
- email_server: Email server (Ex: smtp/imap)
- email_port: Email port (Ex: 587)
- email_from: Email sender email address
- email_Cc: Email cc email address

``python3 main.py -H dbhost -U dbusername -P dbpassword -D database -u email_username -p email_password -s email_server -o email_port -f email_from -c email_Cc``
