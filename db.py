import os
import json
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Secures a connection wiht the database and stores it into the
        instance variable "conn"
        """
        self.conn = sqlite3.connect(
            "todo.db", check_same_thread=False
        )
        self.delete_user_table()
        self.create_user_table()

    def create_user_table(self):
        """
        Using SQL, creates a user table
        """
        self.conn.execute("""
        CREATE TABLE user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            balance REAL
        );
        """)
    
    def delete_user_table(self):
        """
        Using SQL, deletes the user table.
        """
        self.conn.execute("DROP TABLE IF EXISTS user;")

    def get_all_users(self):
        """
        Using SQL, gets all users
        """
        cursor = self.conn.execute("SELECT id, name, username FROM user;")
        users = []
        for row in cursor:
            users.append({"id":row[0], "name":row[1], "username":row[2]})
        return users

    def insert_user_table(self, name, username, balance):
        """
        Using SQL, inserts a new user into the table
        """
        cursor = self.conn.execute("INSERT INTO user (name, username, balance) VALUES (?,?,?);", (name, username, balance))

        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, id):
        """
        Using SQL to get a specific user by ID
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?;",(id,))

        for row in cursor:
            return({"id":row[0], "name":row[1], "username":row[2], "balance":row[3]})

        return None

    def delete_user_by_id(self, id):
        """
        Using SQL, deletes a specific user by id
        """
        self.conn.execute("DELETE FROM user WHERE id = ?;", (id,))
        self.conn.commit()

    def update_user_by_id(self, id, balance):
        """
        Using SQL, updates the balance of a user by ID
        """
        self.conn.execute("UPDATE user SET balance = ? WHERE id = ?;", (balance,id))
        self.conn.commit()


    

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
