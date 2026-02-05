from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserContext(BaseModel):
    """User context for permission filtering"""
    userId: str
    role: str
    department: Optional[str] = None
    permissions: List[str] = []

class QueryRequest(BaseModel):
    """Request model for knowledge base query"""
    query: str = Field(..., min_length=3, max_length=1000)
    userContext: Optional[UserContext] = None

class SourceDocument(BaseModel):
    """Source document citation"""
    documentId: str
    documentName: str
    page: Optional[int] = None
    relevanceScore: float
    excerpt: str

class QueryResponse(BaseModel):
    """Response model for knowledge base query"""
    queryId: str
    answer: str
    sources: List[SourceDocument]
    confidence: float
    tokensUsed: int
    modelVersion: str

class DocumentChunk(BaseModel):
    """Document chunk for RAG"""
    chunkId: str
    documentId: str
    content: str
    chunkIndex: int
    relevanceScore: float = 0.0
    metadata: Dict[str, Any] = {}

class DocumentUploadRequest(BaseModel):
    """Request model for document upload"""
    documentId: str
    filename: str
    filePath: str
    fileType: str
    classification: str = "internal"
    department: Optional[str] = None

class DocumentUploadResponse(BaseModel):
    """Response model for document upload"""
    documentId: str
    status: str
    chunksCreated: int
    message: str
