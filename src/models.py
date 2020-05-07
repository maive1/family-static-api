from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

class Family:
    """We are storing the Doe family members, 
    with their lucky numbers"""

    def __init__(self, last_name):
        self.last_name = last_name #Doe
        
        self._members = [{
            "id": 1,
            "first_name": "John",
            "age": 33,
            "gender": "Male",
            "lucky_numbers": [7,13,22]
        },
        {   
            "id": 2,
            "first_name": "Jane",
            "age": 35,
            "gender": "Female",
            "lucky_numbers": [10,14,3]
        },
        {
            "id": 3,
            "first_name": "Jimmy",
            "age": 5,
            "gender": "Male",
            "lucky_numbers": [1]
        }]

    def _generateId(self):
        return random.randint(0, 99999999)

    def add_member(self, member):
        id = self._generateId()
        member['id'] = id
        self._members.append(member)
        return member

    def delete_member(self, id):
        self._members = [member for member in self._members if member['id'] != id]
        return self._members

    def update_member(self, id, member):
        self._members = [member for member in self._members if member['id'] != id]

    def get_member(self, id):
        member = next(filter(lambda member: member.get('id') == id, self._members), None)
        return  member

    def get_all_members(self):
        return self._members
