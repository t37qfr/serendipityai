import uuid

from services.db import Neo4jConnection
from .base import BaseQuery


class TopicQuery(BaseQuery):
    def __init__(self, user_id=None):
        super().__init__(user_id=user_id)

    def list(self, name):
        query = "MATCH (t:Topic) "

        if name:
            query += "WHERE t.name = '" + name + "' "

        query += "RETURN t.id, t.name, t.description"

        data = self.run(query)
        return data

    def get(self, id):
        query = "MATCH (n:Topic {id: '%s'}) RETURN n.id, n.name, n.description" % id
        data = self.run(query)

        if len(data) == 1:
            return data[0]

        return None

    def create(self, topic_dict):
        assert self.user_id, 'User not defined'

        id = uuid.uuid4()
        name = topic_dict.get('name')
        description = topic_dict.get('description')

        if not name or not description:
            raise ValueError('Name and description are mandatory!')

        # create the node
        query = "CREATE (n:Topic {id: '%s', name: '%s', description: '%s'}) RETURN n" % (id, name, description)
        data = self.run(query)

        # create connection with the user
        query = "MATCH (t:Topic {id: '%s'}) " \
                "MATCH (u:User {id: '%s'}) " \
                "CREATE (u)-[rel:OWNS] -> (t)" % (id, self.user_id)

        self.run(query)

        return data[0]

    def delete(self, id):
        self._connection_exist_with_the_user(id)

        query = "MATCH (n:Topic {id: '%s'}) DETACH DELETE n" % id
        self.run(query)

    def update(self, id, dt):
        self._connection_exist_with_the_user(id)

        query = "MATCH (t:Topic {id: '%s'}) " % id

        name = dt.get('name')
        description = dt.get('description')

        set_parts = []

        if name:
             set_parts.append("t.name='" + name + "'")

        if description:
            set_parts.append("t.description='" + description + "'")

        if set_parts:
            query += " SET " + ', '.join(set_parts)

        query += " RETURN t.id, t.name, t.description"

        data = self.run(query)

        return data[0]

    def _connection_exist_with_the_user(self, id):
        """Security check to ensure the user has the right to modify the topic"""
        assert self.user_id, 'User not defined'

        # check connection with the user
        query = "MATCH (t:Topic {id: '%s'}), (u:User {id: '%s'}) RETURN EXISTS( (t)-[:OWNS]-(u) )" % (id, self.user_id)

        is_related_to_user = self.run(query)

        if not is_related_to_user:
            raise ValueError('Access Denied')





