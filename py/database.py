import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234567890123wQ",
        database="smarthome",
        port=3307
    )
