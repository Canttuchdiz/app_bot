from EasySqlite import *
import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()

instance = EasySqlite(cur)
instance.create_table("trees", "items", "things", "sports")
