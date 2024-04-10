import pandas as pd
import pymongo
from pymongo.errors import BulkWriteError
class CSVToJsonConverter:
    def __init__(self, csv_file):
        """
        初始化CSVToJsonConverter

        Parameters:
            csv_file (str): CSV文件的路徑

        Returns:
            None
        """
        self.csv_file = csv_file

    def convert_to_json(self):
        """
        將CSV文件轉換為JSON格式

        Returns:
            list: 包含JSON格式數據的列表
        """
        data = []
        df = pd.read_csv(self.csv_file)
        # 藉由member_id分組
        grouped = df.groupby('member_id')
        for member_id, group in grouped:
            entry = {
                "_id": member_id,
                "member_id": member_id,
                "tags": self.create_tags(group)
            }
            data.append(entry)
        return data

    def create_tags(self, group):
        """
        創建標籤List

        Parameters:
            group (pandas.DataFrame): 分組後的DataFrame

        Returns:
            list: 包含標籤字典的列表
        """
        tags = []
        for _, row in group.iterrows():
            tag = {
                "tag_name": row['tag_name'],
                "detail": [{
                    "detail_name": row['detail_name'],
                    "detail_value": row['detail_value']
                }]
            }
            tags.append(tag)
        return tags
    
class MongoWriter:
    """
    將數據寫入MongoDB的類別。

    Attributes:
        client (pymongo.MongoClient): MongoDB客戶端。
        db_name (str): 要寫入的資料庫名稱。
        collection_name (str): 要寫入的集合名稱。
    """

    def __init__(self, host: str, port: int, username: str, password: str, db_name: str, collection_name: str) -> None:
        """
        初始化MongoWriter。

        Parameters:
            host (str): MongoDB 主機名。
            port (int): MongoDB 連接埠號。
            username (str): MongoDB 用戶名。
            password (str): MongoDB 密碼。
            db_name (str): 資料庫名稱。
            collection_name (str): 集合名稱。
        """
        # 連接 MongoDB
        self.client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
        self.db_name = db_name
        self.collection_name = collection_name
         # 如果資料庫不存在，則創建新的資料庫
        if db_name not in self.client.list_database_names():
            self.client[db_name]

        # 如果集合不存在，則創建新的集合
        db = self.client[db_name]
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
    def write_to_mongodb(self, data: list) -> None:
        """
        將數據寫入MongoDB。

        Parameters:
            data (list): 包含要寫入的數據的列表。
        """
        try:
            db = self.client[self.db_name]
            collection = db[self.collection_name]
            print(f"開始寫入資料至 db: {self.db_name}, collection: {self.collection_name}")
            collection.insert_many(data)
            print("寫入完畢")
        except BulkWriteError:
            print("_id已存在，不進行寫入。")
        finally:
            self.client.close()

if __name__ =="__main__":
    csv_file = 'CSV2JSON.csv'
    converter = CSVToJsonConverter(csv_file)
    json_data = converter.convert_to_json()
    print(json_data)
    dbwriter = MongoWriter(host="localhost",username="admin",password="admin",port=27018,db_name="test3",collection_name="member_info")
    dbwriter.write_to_mongodb(json_data)
    