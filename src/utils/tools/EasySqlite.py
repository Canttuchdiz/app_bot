from src.utils import *
from sqlite3 import *
import asyncio

class EasySqlite():

    def __init__(self, cursor : Cursor):
        self.cursor = cursor


    async def initialize(self):
        self.sql = await UtilMethods.json_retriever("jsons/sql.json")

    def create_table(self, table_name : str, *args : str):
        """
        Creates table with given arguments.
        :param table_name:
        :param args:
        :return:
        """
        separator = ', '
        try:
            self.cursor.execute(self.sql["table"].format(table_name, separator.join(*args)))
        except Exception as e:
            print(e)




