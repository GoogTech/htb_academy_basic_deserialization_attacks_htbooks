# HTBooks GmbH & Co. KG
# 10.10.2022

from . import config
import sqlite3
import bcrypt
import pickle
import base64

class Session:
    def __init__(self, username):
        # Connect to the SQLite database using the configured database name
        con = sqlite3.connect(config.DB_NAME)
        cur = con.cursor()
        # Query the database for the username and role of the given user
        res = cur.execute("SELECT username, role FROM users WHERE username = ?", (username,))
        # Fetch the query result and assign username and role to the session instance
        self.username, self.role = res.fetchone()
        # Close the database connection
        con.close()

    def getUsername(self):
        # Return the username stored in this session
        return self.username

    def getRole(self):
        # Return the user role stored in this session
        return self.role

    def isAdmin(self):
        # Return True if the user's role is 'admin'
        return self.role == 'admin'


def sessionToCookie(session):
    # Serialize the session object using pickle
    p = pickle.dumps(session)
    # Encode the serialized data into base64 format to store safely in a cookie
    b = base64.b64encode(p)
    # Return the encoded byte string
    return b


def cookieToSession(cookie):
    # Decode the base64-encoded cookie back into bytes
    b = base64.b64decode(cookie)
    # Check for potentially dangerous substrings that could indicate command injection.
    # Note that the prefix b indicates that the value is a bytes literal, not a regular string (str),
    # and the result of base64.b64decode(cookie) is binary data (a bytes object), for example: b'\x80\x04...'
    for badword in [b"nc", b"ncat", b"/bash", b"/sh", b"subprocess", b"Popen"]:
        if badword in b:
            return None  # Reject the cookie if it contains suspicious content

    # Deserialize the byte stream back into a Python object (Session instance)
    # !!! Detailed: decode pickled byte stream `b` back to a Python object. !!!
    # !!! Note: pickle.loads will execute object constructors / __reduce__/__setstate__; only use on trusted, verified data (e.g., HMAC-checked). !!!
    # Ref: https://docs.python.org/3/library/pickle.html#object.__reduce__
    p = pickle.loads(b)
    return p


def checkLogin(username, password):
    # Connect to the SQLite database
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    # Retrieve the stored password hash for the given username
    res = cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    passwordHash, = res.fetchone()
    con.close()
    # Compare the provided password with the stored bcrypt hash
    return bcrypt.checkpw(password.encode(), passwordHash.encode())