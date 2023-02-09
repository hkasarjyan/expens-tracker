from PySide2.QtCore import QObject, QMetaObject
from ExpenseTracker.models.User import User
from ExpenseTracker.encoder import CustomJSONEncoder
import json
import requests
import requests


HOST = "http://localhost"
PORT = 5555

def getURL(endpoint):
    return "{}:{}/{}".format(HOST, PORT, endpoint)

class ResponseData:
    def __init__(self):
        self._status = False
        self._code = 500
        self._json = None

    @property
    def status(self)->bool:
        return self._status
    @status.setter
    def status(self, status: bool):
        self._status = status
        
    @property
    def json(self):
        return self._json
    @json.setter
    def json(self, json):
        self._json = json
        
    @property
    def code(self)->int:
        return self._code
    @code.setter
    def code(self, code: int):
        self._code = code

class Client(QObject):
    """API Client class"""

    def __init__(self, parent=None):
        super(Client,self).__init__(parent)
    
    def login(self, user: User):
        responseData = ResponseData()
        payload = json.dumps(user, cls=CustomJSONEncoder)
        headers = {
                    'Content-Type': "application/json"
                  }
        print(getURL('login'))
        
        response = None
        try:
            response = requests.request("POST", getURL('login'), data=payload, headers=headers)
            responseData.status = response.status_code == 200
            responseData.json = response.json()
            responseData.code = response.status_code
            return responseData
        except:
            responseData.json = {"msg":"Exception user is requested {}".format(response)}
            return responseData

    def signup(self, user: User)->ResponseData:
        responseData = ResponseData()
        payload = json.dumps(user, cls=CustomJSONEncoder)
        print("Payload={}".format(payload))
        headers = {
                    'Content-Type': "application/json"
                  }
        print(getURL('users'))
        
        response = None
        try:
            response = requests.request("POST", getURL('users'), data=payload, headers=headers)
            responseData.status = response.status_code == 201
            responseData.json = json.loads(response.text)
            responseData.code = response.status_code
        except:
            responseData.json = {"msg":"Exception user is requested {}".format(response)}
        return responseData


