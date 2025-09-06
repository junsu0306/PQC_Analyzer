import re
import json
from langchain_community.llms import Ollama
from config.settings import LLM_MODEL
from src.graph.graph_db import graph_db_instance
from src.utils.logger import logger

class GraphRAGAnalyzer:
    def __init__(self):
        self.llm = Ollama(model=LLM_MODEL, format="json")
        self.graph_db = graph_db_instance
        self.entity_patterns = re.compile(r'\b(EVP_aes_256_cbc|RSA_public_encrypt|AES|RSA|OpenSSL)\b', re.IGNORECASE)

    def analyze_code(self, code: str) -> dict:
        logger.info("Starting code analysis...")
        found_entities = set(self.entity_patterns.findall(code))
        if not found_entities:
            logger.info("No relevant entities found in the code.")
            return {"assessment": "Safe", "reasoning": "No known non-PQC keywords were found."}

        logger.info(f"Found entities: {list(found_entities)}")
        all_contexts = set()
        for entity in found_entities:
            contexts = self.graph_db.find_related_subgraph(entity_name=entity)
            for context in contexts:
                all_contexts.add(context)
        
        retrieved_context = "\n".join(all_contexts)
        if retrieved_context:
            logger.info(f"Retrieved context from graph:\n{retrieved_context}")
        else:
            logger.warning("Entities found, but no context retrieved from graph.")

        prompt = self._build_prompt(code, retrieved_context)
        
        try:
            response_str = self.llm.invoke(prompt)
            logger.info(f"Received raw response from LLM: {response_str}")
            if response_str.strip().startswith("```json"):
                response_str = response_str.strip()[7:-3]
            return json.loads(response_str)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from LLM: {response_str}")
            return {"error": "LLM returned non-JSON response.", "raw_response": response_str}
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            return {"error": "Unexpected error during LLM invocation."}

    def _build_prompt(self, code: str, context: str) -> str:
        return f"""
You are a cybersecurity expert specializing in Post-Quantum Cryptography (PQC).
Analyze the source code to find non-PQC algorithms. Use the CONTEXT from a knowledge graph to make an informed decision.

CONTEXT from Knowledge Graph:
{context if context else "No specific relationships found for the detected keywords."}

SOURCE CODE:
```c
{code}
```

Based on your analysis, provide a response STRICTLY in JSON format with these keys:
- "identified_vulnerabilities": list of dicts, each with "algorithm_name" and "entity_found_in_code".
- "assessment": "Confirmed Non-PQC", "Suspicious", or "Safe".
- "reasoning": A detailed explanation referencing both the code and the context.
"""

# --- ✅ 수정된 부분 시작 ---
# GraphRAGAnalyzer 클래스의 실제 인스턴스(객체)를 생성합니다.
# 이 인스턴스를 다른 파일에서 가져가서 사용하게 됩니다.
analyzer_instance = GraphRAGAnalyzer()
# --- ✅ 수정된 부분 끝 ---

