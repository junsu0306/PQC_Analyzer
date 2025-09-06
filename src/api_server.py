import sys
import os

# --- 경로 문제 해결을 위한 코드 ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.analysis.analyzer import analyzer_instance
from src.utils.logger import logger
import uvicorn

app = FastAPI(
    title="PQC Analyzer API",
    description="API for analyzing source code for non-PQC vulnerabilities using GraphRAG.",
    version="1.0.0"
)

# --- ✅ 수정된 부분 시작 ---
@app.on_event("startup")
async def startup_event():
    """
    API 서버가 시작될 때 LLM을 예열(warm-up)하여 첫 요청에 바로 응답할 수 있도록 준비합니다.
    """
    logger.info("API server is starting up. Warming up the LLM...")
    try:
        # 모델을 메모리에 로드하기 위해 간단한 요청을 보냅니다.
        analyzer_instance.llm.invoke("Hello!")
        logger.info("LLM is warmed up and ready to receive requests.")
    except Exception as e:
        logger.error(f"Failed to warm up LLM. Please check if Ollama is running correctly. Error: {e}")
# --- ✅ 수정된 부분 끝 ---


class CodeAnalysisRequest(BaseModel):
    file_path: str

@app.post("/analyze-code", tags=["Analysis"])
async def analyze_code_endpoint(request: CodeAnalysisRequest):
    logger.info(f"Received analysis request for file: {request.file_path}")
    
    if not os.path.exists(request.file_path):
        logger.error(f"File not found: {request.file_path}")
        raise HTTPException(status_code=404, detail="File not found")
        
    try:
        with open(request.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()
    except Exception as e:
        logger.error(f"Error reading file {request.file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Could not read file: {e}")

    analysis_result = analyzer_instance.analyze_code(code_content)
    
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result)
        
    return analysis_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

