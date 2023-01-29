import mysql.connector


def _connect_db():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='code',
        password='xIE_/InK@s(E8.(f',
        database='pass-gen'
    )
    return connection
