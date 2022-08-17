from tools import UserAgent, KalimatiMarket
import mysql.connector
import logging



# This will log our each requests and record the time and error whenever the script fails so it would be easy to debug later:
logging.basicConfig(filename='kMarket.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(message)s', datefmt=f"%d-%b-%y %H:%M:%S")


# Making a MYSQL connection:
mydb = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = '',
                database = 'kalimati_daily_market' # first create a datbase in MYSQL then run the script.
    )
cursor = mydb.cursor()

# First create a database name by using below queries:
# cursor.execute("CREATE DATABASE kalimati_daily_market")

print(f"--------------------------------------------------------------------------------\nWelcome to Kalimati market data scraper. | The scraper is powered by Playwright.")


kalimati_market = KalimatiMarket()

today_date = kalimati_market.daily_date()


try:
  table_name = f"CREATE TABLE `{today_date}` (Date VARCHAR(50), Commodity VARCHAR(50), Units VARCHAR(50), Minimum VARCHAR(50), Maximum VARCHAR(50), Average VARCHAR(50))"
  cursor.execute(table_name)

  s = f"INSERT INTO `{today_date}` VALUES(%s, %s, %s, %s, %s, %s)"
  cursor.executemany(s, kalimati_market.scrape())
  mydb.commit()
  mydb.close()
  print(f"Database is saved!")
except mysql.connector.errors.ProgrammingError:
    print("No new data available. Try again tomorrow.")







