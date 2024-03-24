# import secrets
from typing import Union
from unittest import result
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from .utils.noSQL import createClient
USERPROFILE_DOC_TYPE = "userprofile"

""" 
def get_bucket():
    cluster = Cluster(
        "couchbase://couchbasehost:8091?fetch_mutation_tokens=1&operation_timeout=30&n1ql_timeout=300"
    )
    authenticator = PasswordAuthenticator("username", "password")
    cluster.authenticate(authenticator)
    bucket: Bucket = cluster.open_bucket("bucket_name", lockmode=LOCKMODE_WAIT)
    bucket.timeout = 30
    bucket.n1ql_timeout = 300
    return bucket """
def createClient():
    # uriDemo = "mongodb+srv://root:<password>@demo.mysl5zj.mongodb.net/"
    uri = "mongodb+srv://root:lmsCAoHCBpDYxdgs@demo.mysl5zj.mongodb.net/?retryWrites=true&w=majority&appName=demo"
    secret = "lmsCAoHCBpDYxdgs"
# Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client

""" def get_user(bucket: Bucket, username: str):
    doc_id = f"userprofile::{username}"
    result = bucket.get(doc_id, quiet=True)
    if not result.value:
        return None
    user = UserInDB(**result.value)
    return user 
    """


# FastAPI specific code
""" app = FastAPI()


@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    bucket = get_bucket()
    user = get_user(bucket=bucket, username=username)
    return user
 """

client = createClient()

print(client.list_database_names())
db = client['fwwb']
print(db.list_collection_names())
collection = db['resume']


from bson.objectid import ObjectId

# 假设我们有一个 ObjectId
id_to_find = ObjectId('65ff92df8306e976ca9aa80b')

# 使用 _id 进行查询
doc = collection.find_one({"_id": id_to_find})
# result = collection.find_one({"_id":"65ff92df8306e976ca9aa80b"})
print(doc)
# result = collection.find({"user_id":3})
# for i in result:
#     print(i)

""" result2 = collection.find()
print(result2)
doc = {"name": "John", "age": 30, "city": "New York"}
collection.insert_one(doc)

stu2={'id':'002','name':'lisi','age':15}
stu3={'id':'003','name':'wangwu','age':20}
result = collection.insert_many([stu2,stu3])
print(result)
可以直接使用remove方法删除指定的数据 会报错，3.0版本已经废弃
result = collection.remove({'name': 'zhangsan'})
result2 = collection.delete_one({"name":"zhangsan"})
print(result2) """


""" #姓名为zhangsan的记录，age修改为22
condition = {'name': 'John'}
res = collection.find_one(condition)
res['age'] = 22
#update_one,第 2 个参数需要使用$类型操作符作为字典的键名
result = collection.update_one(condition, {'$set': res})
print(result) #返回结果是UpdateResult类型
print(result.matched_count,result.modified_count) #获得匹配的数据条数1、影响的数据条数1
 """
""" # update_many,所有年龄为15的name修改为xixi
condition = {'age': 15}
res = collection.find_one(condition)
res['age'] = 30
result = collection.update_many(condition, {'$set':{'name':'xixi'}})
print(result) #返回结果是UpdateResult类型
print(result.matched_count,result.modified_count) #获得匹配的数据条数3、影响的数据条数3
 """
# # 查询集合中的所有文档
""" docs = collection.find()

# 打印所有文档
for doc in docs:
    print(doc)
 """
