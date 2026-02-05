from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import jwt
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from root .env file
env_path = Path(__file__).parent.parent.parent / '.env'
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Verify critical env vars
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key or openai_key == "api-key-here":
    print(" WARNING: OPENAI_API_KEY not set or using placeholder")
    print(" The service will start but queries won't work until you set a real API key")
else:
    print(f"OpenAI API key loaded (starts with: {openai_key[:10]}...)")

from src.models.schemas import QueryRequest, QueryResponse
from src.services.embedding_service import EmbeddingService
from src.services.document_processor import DocumentProcessor
from src.utils.prompt_injection_detector import PromptInjectionDetector
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Knowledge Assistant - AI Service",
    description="RAG-based knowledge retrieval service",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SERVICE_SECRET = os.getenv("SERVICE_SECRET", "your-service-secret")

# Initialize services
embedding_service = EmbeddingService()
document_processor = DocumentProcessor()
injection_detector = PromptInjectionDetector()


async def verify_service_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """Verify JWT token from API Gateway"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            SERVICE_SECRET,
            algorithms=["HS256"]
        )
        
        if payload.get("service") != "api-gateway":
            raise HTTPException(status_code=403, detail="Invalid service token")
        
        return payload.get("user_context", {})
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Service token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid service token")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-service",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "api-key-here")
    }


@app.post("/internal/query", response_model=QueryResponse)
async def execute_query(
    request: QueryRequest,
    user_context: Dict[str, Any] = Depends(verify_service_token)
):
    """
    Execute a knowledge base query using RAG pipeline
    
    THIS IS A SIMPLIFIED VERSION - Full RAG implementation in next step
    """
    try:
        logger.info(f"Query received from user {user_context.get('userId')}")
        
        # Validate input
        if len(request.query) < 3 or len(request.query) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Query must be between 3 and 1000 characters"
            )
        
        # Detect prompt injection
        if injection_detector.is_malicious(request.query):
            logger.warning(f"Prompt injection detected: {request.query[:50]}")
            raise HTTPException(
                status_code=400,
                detail="Query contains potentially malicious content"
            )
        

        logger.info("Query processed successfully")
        
        return QueryResponse(
            queryId="test-query-123",
            answer="This is a test response. Full RAG implementation coming next! Your query was: " + request.query,
            sources=[],
            confidence=0.85,
            tokensUsed=50,
            modelVersion="test-v1"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing query"
        )


@app.get("/metrics")
async def get_metrics():
    """Get service metrics"""
    return {
        "service": "ai-service",
        "metrics": {
            "total_documents_indexed": document_processor.get_document_count(),
            "total_chunks": document_processor.get_chunk_count(),
            "cache_hit_rate": embedding_service.get_cache_hit_rate(),
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
