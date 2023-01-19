from neo4j import GraphDatabase


class Neo4jExecutor:

    def __init__(self, host, port, user, password, encrypted):
        self.driver = GraphDatabase.driver(f"bolt://{host}:{port}", auth=(user, password), encrypted=encrypted)

    def execute(self, query):
        with self.driver.session() as session:
            return query(session)

    def constraint_exists(self, labels, properties, name=None):
        if name:
            name_match = "name = $name"
        else:
            name_match = "name IS NOT NULL"

        with self.driver.session() as session:
            for record in session.run(
                    "SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties "
                    f"WHERE {name_match} "
                    "AND labelsOrTypes = $labels AND properties = $properties "
                    "AND type = 'UNIQUENESS' "
                    "RETURN COUNT(name) AS matchingCount",
                    labels=labels, properties=properties):
                return record[0] == 1

    def index_exists(self, labels, properties, name=None, index_type="RANGE"):
        if name:
            name_match = "name = $name"
        else:
            name_match = "name IS NOT NULL"

        with self.driver.session() as session:
            for record in session.run(
                    "SHOW INDEXES YIELD name, type, labelsOrTypes, properties "
                    f"WHERE {name_match} "
                    "AND labelsOrTypes = $labels AND properties = $properties "
                    "AND type = $type "
                    "RETURN COUNT(name) AS matchingCount",
                    labels=labels, properties=properties, name=name, type=index_type):
                return record[0] == 1

    def close(self):
        self.driver.close()
