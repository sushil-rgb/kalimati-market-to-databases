from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from tools import KalimatiMarket


app = FastAPI()
date = KalimatiMarket().daily_date()
kalimati = KalimatiMarket().scrape()


@app.get("/")
def main_page():
    return {'api-endpoints':[
                            "/kalimati_market",                            
                            "/kalimati_market/commodity",
                            "/kalimati_market/unit",
                            "/kalimati_market/minimum",
                            "/kalimati_market/maximum",
                            "/kalimati_market/average",
                            
        ]
        }


@app.get("/kalimati_market")
def market_today():
    try:
        return {date: {
            "वस्तु": kalimati[0],
            "एकाइ": kalimati[1],
            "न्यूनतम": kalimati[2],
            "अधिकतम": kalimati[3],
            "औसत": kalimati[4]

        }
        
    
    }
    except IndexError:
        return "No data available try again tomorrow!"


@app.get("/kalimati_market/commodity")
def commodity():
    return {date:{
            "वस्तु": kalimati[0]}}
         
        


@app.get("/kalimati_market/unit")
def unit():
    return {date:{
            "एकाइ": kalimati[1]}}     
        


@app.get("/kalimati_market/minimum")
def minimum():
    return {date:{
            "न्यूनतम": kalimati[2]}}    
        


@app.get("/kalimati_market/maximum")
def maximum():
    return {date:{
            "अधिकतम": kalimati[3]}}    
        


@app.get("/kalimati_market/average")
def average():
    return {date:{
            "औसत": kalimati[4]}}
    
        