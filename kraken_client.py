import os
import krakenex

api = krakenex.API()
api.key = os.getenv("KRAKEN_API_KEY")
api.secret = os.getenv("KRAKEN_API_SECRET")

def get_price(pair="XXBTZUSD"):
    return api.query_public('Ticker', {'pair': pair})


 
