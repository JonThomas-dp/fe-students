import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)


    def __init__(self, name):
        self.name = name


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name']

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)