"""REPOSITORIES
Methods to interact with the review collection
"""

from app.repository.dbmanager import db
from bson import ObjectId


def get_all_review():
    def id_limit(page_size=10, last_id=None):
        """Function returns `page_size` number of documents after last_id
        and the new last_id.
        """

        """
        filter = {
            '_id': {
                '$gt': ObjectId('6338ca7d2a28471c077dd97e')
            }
        }
        sort = list({
                        '_id': -1
                    }.items())
        limit = 20

        result = db['review'].find(
            filter=filter,
            sort=sort,
            limit=limit
        )
        """

        if last_id is None:
            # first page
            cursor = db['review'].find({}).limit(page_size)
        else:
            cursor = db['review'].find({'_id': {'$gt': ObjectId(last_id)}}).limit(page_size)

        # Get the data
        data = [document for document in cursor]

        if not data:
            # No documents left
            return None, None

        # Since documents are naturally ordered with _id, last document will
        # have max id.
        last_id = data[-1]['_id']

        return data, last_id

    def skip_limit(page_size=10, page_num=1):
        """returns a set of documents belonging to page number `page_num`
        where size of each page is `page_size`.
        """
        # Calculate number of documents to skip
        skips = page_size * (page_num - 1)
        print(skips)
        # Skip and limit
        cursor = db['review'].find().skip(skips).limit(page_size)

        # Return documents
        return [document for document in cursor]
        # return cursor

    # return db['review'].find({}).limit(10)
    # return skip_limit(10, 1)
    data, last_id = id_limit(10, "6338ca7d2a28471c077dd97e")
    print(last_id)

    return data


"""
filter={}
sort=list({
              '_id': -1
          }.items())
skip=20
limit=20

result = client['wine']['review'].find(
    filter=filter,
    sort=sort,
    skip=skip,
    limit=limit
)
"""

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
