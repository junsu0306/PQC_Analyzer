import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# --- LLM Settings ---
LLM_MODEL = os.getenv("LLM_MODEL", "llama3:8b") # .env 파일이 없으면 기본값으로 llama3:8b 사용

# --- Graph Database (Neo4j) Settings ---
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password") # .env에 비밀번호를 설정하세요

# --- Data Path Settings ---
# 프로젝트 루트를 기준으로 상대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_CSV_PATH = os.path.join(BASE_DIR, 'data', 'initial_graph', 'nodes.csv')
EDGES_CSV_PATH = os.path.join(BASE_DIR, 'data', 'initial_graph', 'edges.csv')