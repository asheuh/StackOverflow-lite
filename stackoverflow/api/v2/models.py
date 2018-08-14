from flask import json
from stackoverflow.api.v1.models import (
    MainModel,
    User
)
from datetime import datetime
from stackoverflow import v2_db

class DatabaseCollector(MainModel):
    """This is the base model"""
    __table__ = ""

    @classmethod
    def to_json_object(cls, item):
        """Creates a model object"""
        return json.loads(json.dumps(item, indent=4, sort_keys=True, default=str))

    @classmethod
    def get_all(cls):
        """Get all the items in the database"""
        v2_db.cursor.execute("SELECT * FROM {}".format(cls.__table__))
        items = v2_db.cursor.fetchall()
        return [cls.to_json_object(item) for item in items]

    @classmethod
    def get_by_field(cls, field, value):
        """
        Get an item from the database by its key or field
        if cls.get_all() is None:
            return {}
        for item in cls.get_all():
            if item[field] == value:
                return item
        """
        v2_db.cursor.execute("SELECT * FROM {0} WHERE {1} = %s".format(cls.__table__, field), (value,))
        items = v2_db.cursor.fetchall()
        return [cls.to_json_object(item) for item in items]

    @classmethod
    def get_one_by_field(cls, field, value):
        items = cls.get_by_field(field, value)
        if len(items) == 0:
            return None
        return items[0]

    @classmethod
    def get_item_by_id(cls, _id):
        """Retrieves an item by the id provided"""
        v2_db.cursor.execute("SELECT * FROM {} WHERE id = %s".format(cls.__table__), (_id,))
        item = v2_db.cursor.fetchone()
        if item is None:
            return None
        return cls.to_json_object(item)

    @classmethod
    def rollback(cls):
        """Deletes all the data from the tables"""
        v2_db.cursor.execute("DELETE FROM {}".format(cls.__table__))
        v2_db.connection.commit()

    def insert(self):
        """Inserts a new item in the database"""
        result = v2_db.cursor.fetchone()
        if result is not None:
            self.id = result['id']
        v2_db.connection.commit()

    @classmethod
    def delete(cls):
        """deletes an item from the database"""
        v2_db.cursor.execute("SELECT * FROM {} WHERE id = %s".format(cls.__table__), (cls.id))
        v2_db.connection.commit()

class User(User, DatabaseCollector):
    __table__ = "users"

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                name VARCHAR,
                username VARCHAR,
                email VARCHAR,
                password_hash VARCHAR,
                registered_on timestamp
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO users(name, username, email,"
            "password_hash, registered_on) VALUES(%s, %s, %s, %s, %s) RETURNING id", (
                self.name,
                self.username,
                self.email,
                self.password_hash,
                self.registered_on
            )
        )
        super().insert()

class BlackList(DatabaseCollector):
    __table__ = "blacklist"

    def __init__(self, jti, blacklisted_on=datetime.now()):
        self.jti = jti
        self.blacklisted_on = blacklisted_on

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS blacklist(
                id serial PRIMARY KEY,
                jti VARCHAR,
                blacklisted_on timestamp
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO blacklist(jti, blacklisted_on) VALUES(%s, %s) RETURNING id", (
                self.jti,
                self.blacklisted_on
            )
        )
        v2_db.connection.commit()
