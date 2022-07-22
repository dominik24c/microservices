from abc import ABC, abstractmethod
from typing import final

from .db import collection, db


class ContentType(ABC):
    """Chain of Responsibility pattern"""
    def __init__(self, nxt) -> None:
        self.__nxt = nxt

    @property
    def nxt(self):
        return self.__nxt

    @final
    def handle(self, content_type: str, body: dict) -> None:
        result = self.check(content_type, body)

        if result is None and self.nxt is not None:
            self.nxt.handle(content_type, body)
    
    @abstractmethod
    def check(self, content_type: str, body: dict) -> bool | None:
        pass


class CreateGameRatings(ContentType):
    def check(self, content_type: str, body: dict) -> bool | None:
        if content_type == 'create_game_ratings':
            # save data to database
            name = body['name'] # game name
            rating = body['rating']

            result = collection.find_one({'name': name})
            if not result:
                collection.insert_one({'name': name, 'total_ratings': rating, 'count_ratings': 1})
            else:
                collection.update_one({'name': name}, {"$inc": {'count_ratings': 1, 'total_ratings': rating }})

            return True

class DeleteGameRatings(ContentType):
    def check(self, content_type: str, body: dict) -> bool | None:
        if content_type == 'delete_game_ratings':
            # delete data in the db
            name = body['name'] # game name
            rating = body['rating']
            res = collection.update_one({'name': name}, {"$inc": {'count_ratings': -1, 'total_ratings': -rating }})
            
            # raise Exception("DELETE", body, res.modified_count, res.matched_count)
            return True
