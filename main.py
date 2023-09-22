import csv
import requests
from environ import Env
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

env = Env()
env.read_env(env_file='.env')
api_key = env('API_KEY')

body = ''
query = {'country': 'in', 'category': 'general', 'apiKey': api_key}
response = requests.get(url='https://newsapi.org/v2/top-headlines', params=query)


lst = response.json()['articles']
for news in lst:
    title = news['title']
    description = news['description']
    body += f'NEWS :-  {title}\nDESCRIPTION :-  {description}\n\n'
response.close()


host = 'smtp.gmail.com'
port = 465
context = ssl.create_default_context()


username = env('USER')
password = env('PASS')
new_sub_or_not = input('Press Y to add a new subscriber, otherwise press N').upper()


if new_sub_or_not == 'Y':
    f = open('subscription.csv', 'a')
    writer = csv.writer(f, lineterminator='\n')
    mail = input('Enter Email - ')
    writer.writerow([mail])
    f.close()
    print('New Subscriber Added \U0001F603')

f = open('subscription.csv', 'r')
reader = csv.DictReader(f, fieldnames=['Emails'])

message = MIMEMultipart()
message['Subject'] = "Your Daily News Alerts are here... \U0001F601 \U0001F6A8"
message.attach(MIMEText(body))


try:
    conn = smtplib.SMTP_SSL(host=host, context=context, port=port)
    conn.login(user=username, password=password)
    for rdr in reader:
        conn.sendmail(from_addr='NewsAlert_Daily', to_addrs=rdr['Emails'], msg=message.as_string())
        print(f"Email Sent Successfully to {rdr['Emails']} \U0001F44D")
    f.close()
except Exception as e:
    print(e)
else:
    conn.quit()