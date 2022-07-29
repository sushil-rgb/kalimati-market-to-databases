from tools import UserAgent, KalimatiMarket
import time
import sqlite3


print(f"-------------------------------------------------------\nWelcome to Kalimati market data scraper:")

kalimati_market_url = "https://kalimatimarket.gov.np/price"
kalimati_market = KalimatiMarket(kalimati_market_url)

today_date = kalimati_market.daily_date()
daily_date = today_date.replace(",", "").split() # here we first replace the comma and split it to give a table name
table_name = '_'.join(daily_date)
print(f"Today's date: {today_date}")
time.sleep(1)

# Make sqlite3 connection:
conn = sqlite3.connect("Kmarket daily database.db")
curr = conn.cursor()

curr.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(कृषि_उपज TEXT, ईकाइ TEXT, न्यूनतम TEXT, अधिकतम TEXT, औसत TEXT)")

curr.executemany(f"INSERT INTO {table_name} VALUES(?, ?, ?, ?, ?)", kalimati_market.scrape())
conn.commit()
conn.close()

print(f"Kalimati Market database is saved. Date | {today_date}\n-------------------------------------------------------")


