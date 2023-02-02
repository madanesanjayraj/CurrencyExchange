import requests
"""
Handles External API requests

"""
class APIHandler(object):
    
    @staticmethod
    def fetchCurrencyRates() -> list:
        """
        Fetch list of currencies and rates from server
        
        :return: list
        """
        api_url = "https://api-coding-challenge.neofinancial.com/currency-conversion?seed=19231"
        response = requests.get(api_url)
        return response.json()