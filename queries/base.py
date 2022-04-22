from services.db import Neo4jConnection


class BaseQuery:
    def __init__(self, user_id):
        self.conn = Neo4jConnection()
        self.user_id = user_id

    def run(self, query):
        return self.conn.query(query)