from neo4j import GraphDatabase


class Neo4jExecutor:

    def __init__(self, host, port, user, password):
        self.driver = GraphDatabase.driver(f"bolt://{host}:{port}", auth=(user, password))

    def execute(self, query):
        with self.driver.session() as session:
            return query(session)

    def execute_conditionally(self, check_query, query):
        changed = False

        with self.driver.session() as session:
            exists = check_query(session)

            if not exists:
                query(session)
                changed = True

        return changed

    def close(self): self.driver.close()
