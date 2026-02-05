from typing import List
import openai
import os
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class EmbeddingService:
    """Service for generating text embeddings using OpenAI"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Only initialize if we have a real API key
        if api_key and api_key != "api-key-here":
            self.client = openai.OpenAI(api_key=api_key)
            self.enabled = True
            logger.info("OpenAI client initialized")
        else:
            self.client = None
            self.enabled = False
            logger.warning("OpenAI client not initialized - no valid API key")
        
        self.model = "text-embedding-3-small"
        self.dimension = 1536
        self.cache_hit_count = 0
        self.total_requests = 0
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        if not self.enabled:
            logger.warning("OpenAI not configured, returning dummy embedding")
            # Return dummy embedding for testing
            return [0.0] * self.dimension
        
        try:
            self.total_requests += 1
            
            logger.info(f"Generating embedding for text (length: {len(text)})")
            
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            embedding = response.data[0].embedding
            
            logger.info(f"✅ Embedding generated (dimension: {len(embedding)})")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def get_cache_hit_rate(self) -> float:
        """Get cache hit rate"""
        if self.total_requests == 0:
            return 0.0
        return self.cache_hit_count / self.total_requests
