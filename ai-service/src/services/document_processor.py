from typing import List, Dict, Any
import PyPDF2
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class DocumentChunk:
    """Simple document chunk"""
    def __init__(self, content: str, chunk_index: int, token_count: int):
        self.content = content
        self.chunk_index = chunk_index
        self.token_count = token_count

class DocumentProcessor:
    """Process documents for RAG pipeline"""
    
    def __init__(self):
        self.document_count = 0
        self.chunk_count = 0
    
    async def extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text from document
        
        Args:
            file_path: Path to file
            file_type: Type of file (application/pdf, etc.)
            
        Returns:
            Extracted text
        """
        try:
            if file_type == "application/pdf" or file_path.endswith('.pdf'):
                return self._extract_from_pdf(file_path)
            elif file_type == "text/plain" or file_path.endswith('.txt'):
                return self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def chunk_text(
        self, 
        text: str, 
        chunk_size: int = 400, 
        chunk_overlap: int = 50
    ) -> List[DocumentChunk]:
        """
        Chunk text into smaller pieces
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            # Rough token count (1 token ≈ 4 characters)
            token_count = len(chunk_text) // 4
            
            chunks.append(DocumentChunk(
                content=chunk_text.strip(),
                chunk_index=chunk_index,
                token_count=token_count
            ))
            
            start += (chunk_size - chunk_overlap)
            chunk_index += 1
        
        self.chunk_count += len(chunks)
        logger.info(f"Created {len(chunks)} chunks")
        
        return chunks
    
    async def store_chunk_metadata(
        self,
        document_id: str,
        chunks: List[Dict[str, Any]],
        vector_ids: List[str]
    ):
        """Store chunk metadata in database"""
        # In production, this would insert into PostgreSQL
        logger.info(f"Stored metadata for {len(chunks)} chunks")
    
    def get_document_count(self) -> int:
        """Get total documents processed"""
        return self.document_count
    
    def get_chunk_count(self) -> int:
        """Get total chunks created"""
        return self.chunk_count
