from tools import UserAgent, KalimatiMarket
import time
import sqlite3


print(f"--------------------------------------------------------------------------------\nWelcome to Kalimati market data scraper. | The scraper is powered by Playwright.")

kalimati_market = KalimatiMarket()

today_date = kalimati_market.daily_date()
daily_date = today_date.replace(",", "").split() # here we first replace the comma and split it to give a table name
table_name = '_'.join(daily_date)

# Make sqlite3 connection:
conn = sqlite3.connect("Kmarket daily database.db")
curr = conn.cursor()

try:    
    curr.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(कृषि_उपज TEXT, ईकाइ TEXT, न्यूनतम TEXT, अधिकतम TEXT, औसत TEXT)")
    curr.executemany(f"INSERT INTO {table_name} VALUES(?, ?, ?, ?, ?)", kalimati_market.scrape())
    conn.commit()
    conn.close()
    print(f"Today's date: {today_date}")
    time.sleep(2)
    print(f"Kalimati Market database is saved. Date | {today_date}\n-------------------------------------------------------------------------------")
except sqlite3.OperationalError:
    print(f"No data available. Please try again tomorrow.")

