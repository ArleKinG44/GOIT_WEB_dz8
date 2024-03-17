from bson import json_util
from mongoengine import connect, Document, StringField, ListField, ReferenceField, BooleanField, CASCADE 


connect(db='hw', host = "mongodb://localhost:27017")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "autors"}


class Quote(Document):
    author = ReferenceField(Author revers_delete_rule = CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args: *args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
    

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)