import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.analysis.scanner import scanner_instance
from src.analysis.analyzer import analyzer_instance
from src.utils.logger import logger
import uvicorn

app = FastAPI(title="PQC Analyzer API")

@app.on_event("startup")
async def startup_event():
    logger.info("Warming up the LLM...")
    try:
        analyzer_instance.llm.invoke("Hello!")
        logger.info("LLM is warmed up and ready.")
    except Exception as e:
        logger.error(f"Failed to warm up LLM. Error: {e}")

class CodeAnalysisRequest(BaseModel):
    file_path: str

@app.post("/analyze-code", tags=["Analysis"])
async def analyze_code_endpoint(request: CodeAnalysisRequest):
    logger.info(f"Received request for file: {request.file_path}")
    
    try:
        with open(request.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
        
    # 1. Scanner를 통해 코드에서 저수준 단서를 찾습니다.
    found_clues = scanner_instance.scan_code(code_content)
    
    # 2. Analyzer에 코드와 발견된 단서를 전달하여 심층 분석(추론)을 요청합니다.
    analysis_result = analyzer_instance.analyze_from_clues(code_content, found_clues)
    
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result)
        
    return analysis_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)