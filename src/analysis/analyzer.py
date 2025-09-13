import json
from langchain_community.llms import Ollama
from config.settings import LLM_MODEL
from src.graph.graph_db import graph_db_instance
from src.utils.logger import logger

class GraphRAGAnalyzer:
    def __init__(self):
        self.llm = Ollama(model=LLM_MODEL, format="json")
        self.graph_db = graph_db_instance
        # ✅ 수정: 이제 정규표현식은 여기서 사용하지 않습니다.

    # ✅ 수정: 새로운 분석 함수. 코드와 '사전 분석된 단서'를 함께 받습니다.
    def analyze_from_pre_scan(self, code: str, found_clues: list[dict]) -> dict:
        """
        사전 스캔을 통해 발견된 단서(clues)를 기반으로 코드를 분석합니다.
        found_clues: e.g., [{'type': 'MagicNumber', 'id': 'aes_sbox_const'}]
        """
        logger.info("Starting analysis based on pre-scanned clues...")
        
        if not found_clues:
            logger.info("No pre-scanned clues provided.")
            return {"assessment": "Safe", "reasoning": "No known patterns or keywords were found by the pre-scanner."}

        logger.info(f"Received clues: {found_clues}")
        all_contexts = set()
        
        # 전달받은 단서의 id를 사용해 그래프를 검색합니다.
        for clue in found_clues:
            entity_id = clue.get("id")
            if entity_id:
                contexts = self.graph_db.find_related_subgraph(entity_name=entity_id)
                for context in contexts:
                    all_contexts.add(context)
        
        retrieved_context = "\n".join(all_contexts)
        if retrieved_context:
            logger.info(f"Retrieved context from graph:\n{retrieved_context}")
        else:
            logger.warning("Clues were found, but no context was retrieved from the graph.")

        prompt = self._build_prompt(code, retrieved_context, found_clues)
        
        try:
            response_str = self.llm.invoke(prompt)
            # ... (이하 LLM 호출 및 에러 처리 부분은 기존과 동일)
            logger.info(f"Received raw response from LLM: {response_str}")
            if response_str.strip().startswith("```json"):
                response_str = response_str.strip()[7:-3]
            return json.loads(response_str)
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            return {"error": "Unexpected error during LLM invocation."}

    # ✅ 수정: 프롬프트도 '사전 발견된 단서'를 명시하도록 변경
    def _build_prompt(self, code: str, context: str, clues: list[dict]) -> str:
        clue_summary = ", ".join([f"'{c.get('id')}' ({c.get('type')})" for c in clues])
        return f"""
You are a cybersecurity expert. A low-level pattern analysis detected the following clues in the source code: {clue_summary}.
Your task is to analyze the source code and determine if it contains a non-PQC algorithm, using the CONTEXT which explains what these clues mean.

CONTEXT from Knowledge Graph:
{context if context else "No specific relationships found for the detected clues."}

SOURCE CODE:
```c
{code}
```

Based on the detected clues and the context, provide a response STRICTLY in JSON format with keys:
- "assessment": "Confirmed Non-PQC", "Suspicious", or "Safe".
- "evidence": "The primary piece of evidence found (e.g., a specific magic number).",
- "reasoning": "Explain how the evidence proves the existence of a non-PQC algorithm, even with obfuscation."
"""

analyzer_instance = GraphRAGAnalyzer()

