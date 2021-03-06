import httplib
import urllib
import json

# Bitcoin24 API for Python
# Author: Carlos Esteban Lopez Rivas (github.com/celr)
# Last update: 02/26/2013
# Donate: 1Cw95xdqcPYyHKHr2TcXC1n7FBcdZDNsNV
class Bitcoin24:
    # Constructor
    def __init__(self, apiKey=None, username=None):
        self.username = username
        self.apiKey = apiKey
        self.apiHost = 'bitcoin-24.com'
        self.apiUri = '/api/user_api.php'
        self.__connected = False
        self.__connect()
        
    # Gets HTTPS connection
    def __connect(self):
        if (not self.__connected):
            self.__connection = httplib.HTTPSConnection(self.apiHost)
            self.__connected = True
    
    # Makes HTTPS request
    def __makeRequest(self, params, public=False, uri=None):
        if (uri == None):
            uri = self.apiUri
            
        if (public == False):
            params['user'] = self.username
            params['key'] = self.apiKey
            
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        urlParams = urllib.urlencode(params)
        self.__connection.request('POST', uri, urlParams, headers)
        return self.__connection.getresponse()
        
    # Makes request to the API
    def __makeApiRequest(self, apiRequest, params={}):
        self.__connect();
        params['api'] = apiRequest
        response = self.__makeRequest(params)
        return json.load(response)
        
    # Public methods for the API return a dictionary representing a JSON object.
    # API Documentation: https://bitcoin-24.com/user_api
    def getBalance(self):
        return self.__makeApiRequest('get_balance')
        
    def getBitcoinAddress(self):
        return self.__makeApiRequest('get_addr')
        
    def getOpenOrders(self):
        return self.__makeApiRequest('open_orders')
        
    def cancelOrder(self, orderId):
        return self.__makeApiRequest('cancel_order', {'id': orderId})
        
    def buyBitcoin(self, amount, price, currency):
        return self.__makeApiRequest('buy_btc', {'amount': amount, 'price': price, 'cur': currency })
        
    def sellBitcoin(self, amount, price, currency):
        return self.__makeApiRequest('sell_btc', {'amount': amount, 'price': price, 'cur': currency })     
     
    def withdrawBitcoin(self, amount, address):
        return self.__makeApiRequest('sell_btc', {'amount': amount, 'address': address })

    # Trades and orderbook
    def getTrades(self, currency='EUR', sinceId=0):
        self.__connect()
        requestUri = '/api/' + currency + '/trades.json' 
        response = self.__makeRequest({'since': sinceId}, True, requestUri)
        return json.load(response)
        
    def getOrderbook(self, currency='EUR'):
        self.__connect()
        requestUri = '/api/' + currency + '/orderbook.json' 
        response = self.__makeRequest({}, True, requestUri)
        return json.load(response)