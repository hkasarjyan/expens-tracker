"""
This script runs the ExpenseTracker application using a development server.
"""

from os import environ
from ExpenseTracker import app

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 5555
    app.run(HOST, PORT)

