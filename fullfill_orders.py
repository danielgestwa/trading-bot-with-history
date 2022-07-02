#!/usr/bin/python

from datetime import datetime
from database import Database
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = ''
PASSWORD = ''
DOMAIN = 'ssl0.ovh.net'
PORT = 465

class Fullfill:
    def __init__(self, price, datetime):
        self.db = Database()
        self.price = price
        self.datetime = datetime

    def check_fullfill_order(self):
        self.db.db_open()
        orders = self.db.db_get_data("select * from orders order by cancel_time asc")

        for order in orders:
            if self.datetime > datetime.strptime(order[7], '%Y-%m-%d %H:%M:%S.%f'):
                print(f'{order[0]} - remove, Cancel -> date exceeded')
                self.db.db_execute_data("UPDATE orders SET state = -1 WHERE id = ?", [str(order[0])])
            
            elif (order[1] == 'LONG' and order[11] == 0 and self.price >= order[6]) or (order[1] == 'SHORT' and order[11] == 0 and self.price <= order[6]):
                print(f'{order[0]} - remove, Cancel -> price went oposite direction')
                self.db.db_execute_data("UPDATE orders SET state = -1 WHERE id = ?", [str(order[0])])
            
            elif (order[1] == 'LONG' and order[11] == 0 and self.price <= order[5]) or (order[1] == 'SHORT' and order[11] == 0 and self.price >= order[5]):
                print(f'{order[0]} - remove, Stop loose -> not accurate data')
                self.db.db_execute_data("UPDATE orders SET state = -1 WHERE id = ?", [str(order[0])])
            
            elif (order[1] == 'LONG' and order[11] == 0 and self.price <= order[3]) or (order[1] == 'SHORT' and order[11] == 0 and self.price >= order[3]):
                print(f'{order[0]} - buy {order[1]}')
                self.db.db_execute_data("UPDATE orders SET state = 1 WHERE id = ?", [str(order[0])])
                self.db.db_execute_data("INSERT INTO transactions VALUES(NULL, 'BUY', ?, ?, ?, ?)", [order[0], order[1], self.price, self.datetime])
                self.send_email(f'BUY, {order[0]}, {order[1]}, {self.price}, {self.datetime}')
            
            elif (order[1] == 'LONG' and order[11] == 1 and self.price <= order[5]) or (order[1] == 'SHORT' and order[11] == 1 and self.price >= order[5]):
                print(f'{order[0]} - sell {order[1]}, Stop loose -> price went oposite direction')
                self.db.db_execute_data("INSERT INTO transactions VALUES(NULL, 'SL SELL', ?, ?, ?, ?)", [order[0], order[1], self.price, self.datetime])
                self.db.db_execute_data("UPDATE orders SET state = -2 WHERE id = ?", [str(order[0])])
                self.send_email(f'SL SELL, {order[0]}, {order[1]}, {self.price}, {self.datetime}')
            
            elif (order[1] == 'LONG' and order[11] == 1 and self.price >= order[4]) or (order[1] == 'SHORT' and order[11] == 1 and self.price <= order[4]):
                print(f'{order[0]} - sell {order[1]}')
                self.db.db_execute_data("INSERT INTO transactions VALUES(NULL, 'SELL', ?, ?, ?, ?)", [order[0], order[1], self.price, self.datetime])
                self.db.db_execute_data("UPDATE orders SET state = 2 WHERE id = ?", [str(order[0])])
                self.send_email(f'SELL, {order[0]}, {order[1]}, {self.price}, {self.datetime}')

        self.db.db_close()

    def send_email(self, data):
        self.db.db_open()
        users = self.db.db_get_data("select email from users")
        self.db.db_close()

        sender_email = EMAIL
        password = PASSWORD

        for user in users:
            receiver_email = user[0]

            # Create the plain-text and HTML version of your message
            message = MIMEMultipart("alternative")
            message["From"] = sender_email
            message["To"] = receiver_email

            message["Subject"] = "NEW BUY/SELL REQUEST"
            text = data
            html = '<html><body><p>' + data + '</p></body></html>'

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(DOMAIN, PORT, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )