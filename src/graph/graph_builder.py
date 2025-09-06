import pandas as pd
from src.graph.graph_db import graph_db_instance
from src.utils.logger import logger
from config.settings import NODES_CSV_PATH, EDGES_CSV_PATH

class GraphBuilder:
    def __init__(self, db_instance):
        self.db = db_instance

    def clear_database(self):
        logger.info("Clearing old data from the graph...")
        query = "MATCH (n) DETACH DELETE n"
        self.db.run_query(query)
        logger.info("Database cleared.")

    def build_graph(self, nodes_path, edges_path):
        self.clear_database()
        logger.info("Starting to build the graph...")
        
        try:
            nodes_df = pd.read_csv(nodes_path)
            edges_df = pd.read_csv(edges_path)
        except FileNotFoundError as e:
            logger.error(f"CSV file not found: {e}")
            return

        # 노드 생성
        for _, row in nodes_df.iterrows():
            # 라벨에 공백이나 특수문자가 있을 수 있으므로 백틱(`)으로 감싸줍니다.
            query = f"CREATE (n:`{row['label']}` {{id: $id, name: $name}})"
            self.db.run_query(query, parameters={'id': row['id'], 'name': row['name']})

        # 관계(엣지) 생성
        for _, row in edges_df.iterrows():
            # ✅ 여기가 수정된 부분입니다.
            query = f"""
            MATCH (a), (b)
            WHERE a.id = $source AND b.id = $target
            CREATE (a)-[r:`{row['relationship']}`]->(b)
            """
            self.db.run_query(query, parameters={'source': row['source'], 'target': row['target']})
        
        logger.info("Graph built successfully.")

if __name__ == "__main__":
    builder = GraphBuilder(graph_db_instance)
    builder.build_graph(nodes_path=NODES_CSV_PATH, edges_path=EDGES_CSV_PATH)
    graph_db_instance.close()