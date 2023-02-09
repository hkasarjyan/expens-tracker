from PySide2.QtCore import QThread
from APIClient.client import Client
_client = Client()

worker_thread = QThread()

_client.moveToThread(worker_thread)
