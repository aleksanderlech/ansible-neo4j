from neo4j import GraphDatabase


class Neo4jExecutor:

    def __init__(self, host, port, user, password, encrypted):
        self.driver = GraphDatabase.driver(f"bolt://{host}:{port}", auth=(user, password), encrypted=encrypted)

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

    def index_exists(self, labels, properties, uniqueness, name=None, index_type="BTREE"):
        if name:
            name_match = "name = $name"
        else:
            name_match = "name IS NOT NULL"

        with self.driver.session() as session:
            for record in session.run(
                    "CALL db.indexes() YIELD name, type, labelsOrTypes, properties, uniqueness "
                    f"WHERE {name_match} "
                    "AND labelsOrTypes = $labels AND properties = $properties "
                    "AND uniqueness = $uniqueness AND type = $type "
                    "RETURN COUNT(name) AS matchingCount",
                    labels=labels, properties=properties, uniqueness=uniqueness, name=name, type=index_type):
                return record[0] == 1

    def close(self):
        self.driver.close()
