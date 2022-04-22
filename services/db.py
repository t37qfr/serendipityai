from neo4j import GraphDatabase, basic_auth


class Neo4jConnection:
    def __init__(self):
        try:
            # Note: for production, credentials should be set via environment variable
            self._driver = GraphDatabase.driver("bolt://44.202.164.164:7687",
                                               auth=basic_auth("neo4j", "steamer-panels-words"))
        except Exception as e:
            print('Driver creation error:', e)

    def query(self, query):
        assert self._driver is not None, "Driver not initialized"

        session = None
        response = None

        try:
            session = self._driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()

        return response