from neo4j import GraphDatabase
from src.utils.logger import logger
from config.settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class GraphDB:
    def __init__(self, uri, user, password):
        try:
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.info("Successfully connected to Neo4j.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()
            logger.info("Neo4j connection closed.")

    def run_query(self, query, parameters=None):
        if self._driver is None:
            logger.error("Driver not initialized. Cannot run query.")
            return None
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

    def find_related_subgraph(self, entity_name: str, depth: int = 2) -> list:
        # APOC 플러그인이 없을 때를 대비한 기본 쿼리
        fallback_query = f"""
        MATCH path = (n)-[*1..{depth}]-(m)
        WHERE n.name = $entity_name OR n.id = $entity_name
        RETURN path
        """
        
        result = self.run_query(fallback_query, parameters={'entity_name': entity_name})
        contexts = []
        if result:
            for record in result:
                path = record.get('path')
                if path:
                    nodes = path.nodes
                    for i in range(len(nodes) - 1):
                        start_node, end_node = nodes[i], nodes[i+1]
                        rel = path.relationships[i]
                        context = f"'{start_node['name']}' -[{rel.type}]-> '{end_node['name']}'"
                        if context not in contexts:
                            contexts.append(context)
        return contexts

graph_db_instance = GraphDB(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)