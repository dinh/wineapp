from typing import List
from app.models.message_db import MessageDB
from app.models.review import ReviewBaseDB, ReviewFullDB
from app.repository.review import get_review
from app.repository.review import save_review
from app.repository.review import update_review
from app.repository.review import get_all_review
from app.repository.review import delete_review


class reviewCore:
    @staticmethod
    def get_all(limit: int, offset: int) -> List[ReviewFullDB]:
        return list(get_all_review(limit, offset))

    @staticmethod
    def get_one(pid: str) -> ReviewFullDB:
        return get_review(pid)

    @staticmethod
    def save_one(data: ReviewBaseDB) -> MessageDB:
        ret = save_review(data.dict())
        return MessageDB(id=str(ret.inserted_id))
    
    @staticmethod
    def update_one(pid:str, data: ReviewFullDB) -> MessageDB:
        """
        > Update a review in the database

        :param pid: The id of the review to update
        :type pid: str
        :param data: ReviewFullDB
        :type data: ReviewFullDB
        :return: A MessageDB object with the modified count.
        """
        ret = update_review(pid, data.dict())
        return MessageDB(modified_count=str(ret.modified_count))

    @staticmethod
    def delete_one(pid: str) -> MessageDB:
        """
        > Delete a review from the database

        :param pid: str
        :type pid: str
        :return: A MessageDB object with the deleted_count attribute set to the number of documents deleted.
        """
        ret = delete_review(pid)
        return MessageDB(deleted_count=str(ret.deleted_count))