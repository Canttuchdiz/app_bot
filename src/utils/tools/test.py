from EasySqlite import *
import sqlite3
from functools import cached_property


con = sqlite3.connect("test.db")
cur = con.cursor()
@cached_property
def data():
    print("ya")

instance = EasySqlite(cur)
instance.create_table("trees", "items", "things", "sports")


