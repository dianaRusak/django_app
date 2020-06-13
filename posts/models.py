from django.db import models
import os
import shutil
import sqlite3
from posts.logic import use_darknet as ud


def delete_from_db():
    sqliteConnection = False
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = """DELETE from posts_post"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def get_name_from_db():
    sqliteConnection = False
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        image_name = """SELECT cover from posts_post"""
        cursor.execute(image_name)
        sqliteConnection.commit()
        cursor.close()
        return image_name

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.cover:
            pass

        ud.dn.test()
        image_name = get_name_from_db()
        print(image_name)
        detect = ud.dn.detector_image()
        cover = detect.ImageField(upload_to='images/')
        shutil.rmtree('media/images/')
        delete_from_db()
        os.mkdir('media/images/')
        super(Post, self).save(*args, **kwargs)
