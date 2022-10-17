"""REPOSITORIES
Methods to interact with the review collection
"""

from app.repository.dbmanager import db
from bson import ObjectId


def get_all_review(limit: int, offset: int, filters: dict):
    """
    > Get all documents from the `review` collection, skip `skips` documents, and limit the result to `limit` documents

    :param filters: mongodb filters format
    :type filters: dict
    :param limit: The number of documents to return
    :type limit: int
    :param offset: The page number
    :type offset: int
    :return: A list of documents
    """
    # Calculate the number of documents to skip
    skips = limit * (offset - 1)
    cursor = db['review'].find(filter=filters).skip(skips).limit(limit)

    #print(f"(filter={filters}).skip({skips}).limit({limit})")

    # Return documents
    return [document for document in cursor]


def save_review(data: dict):
    return db['review'].insert_one(data)


def update_review(pid: str, data: dict):
    """
    > Update the review with the given id with the given data

    :param pid: The id of the review you want to update
    :type pid: str
    :param data: dict
    :type data: dict
    :return: The result of the update operation.
    """
    value_to_set = {"$set": data}
    return db['review'].update_one({'_id': ObjectId(pid)}, value_to_set)


def delete_review(pid: str):
    return db['review'].delete_one({'_id': ObjectId(pid)})


def get_review(pid: str):
    return db['review'].find_one({'_id': ObjectId(pid)})


'''
async def get_user(conn: AsyncIOMotorClient, id: Optional[str] = None, username: Optional[str] = None,
                   email: Optional[str] = None, mobile: Optional[str] = None) -> UserInDB:
    if id:
        row = await conn[database_name][user_collection_name].find_one({"id": id})
        if row:
            return UserInDB(**row)
    if username:
        row = await conn[database_name][user_collection_name].find_one({"username": username})
        if row:
            return UserInDB(**row)
    if email:
        row = await conn[database_name][user_collection_name].find_one({"email": email})
        if row:
            return UserInDB(**row)
    if mobile:
        row = await conn[database_name][user_collection_name].find_one({"mobile": mobile})
        if row:
            return UserInDB(**row)
'''
