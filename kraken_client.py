import os
import krakenex

api = krakenex.API()
api.key = os.getenv("YpgC+Ex67q5//tZ/APb47rzG8CJ0DDYjADU7JWE7KuLPZaF+5oZmN8SO")
api.secret = os.getenv("6i90kZkp9usvDZRiiuozeLSxn2ETVn3h1iC6XofjNedrsG9f6YL0JW4SCOopbIYsUsEQgsVCtA2cPiSNRETEkA==")
api key = api_key
api.secret = api_secret


def get_price(pair="XXBTZUSD"):
    return api.query_public('Ticker', {'pair': pair})

