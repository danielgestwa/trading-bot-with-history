# trading-bot-with-history

## Configuration:
- fullfill_orders.py -> set SMTP SSL settings: EMAIL, PASSWORD, DOMAIN, PORT
- main_fullfill.py -> create account on CoinMarketCap and set API_KEY value
- main_order.py -> create account on CoinApi and set API_KEY value

## Database setup:
- run main_order.py
- conntect to created stock.db database using command: sqlite3 stock.db
- add emails that you want to send information: INSERT INTO users VALUES(NULL, "example@email.com");
- close database: exit

## Scheduler setup (e.g. CRON)
- add scheule for running main_order.py once a day
- add schedule for running main_fullfill.py every 10 min

That's all, wait for email info when to buy and sell.
You can check created orders and transactions by selecting 'transactions' and 'orders' tables from 'stock.db' database.