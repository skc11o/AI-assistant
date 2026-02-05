import re
from typing import List

class PromptInjectionDetector:
    """Detects potential prompt injection attempts"""
    
    # Patterns that indicate prompt injection
    INJECTION_PATTERNS = [
        r'ignore (previous|above|all) (instructions|prompts|rules)',
        r'disregard (previous|above|all) (instructions|prompts|rules)',
        r'you are now',
        r'new instructions',
        r'system prompt',
        r'forget (everything|all|previous)',
        r'<\|im_start\|>',
        r'### instruction',
        r'assistant:',
        r'human:',
    ]
    
    def __init__(self):
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.INJECTION_PATTERNS]
    
    def is_malicious(self, text: str) -> bool:
        """
        Check if text contains potential prompt injection
        
        Args:
            text: Input text to check
            
        Returns:
            True if potentially malicious, False otherwise
        """
        text_lower = text.lower()
        
        # Check against known patterns
        for pattern in self.patterns:
            if pattern.search(text_lower):
                return True
        
        # Check for excessive special characters (might be encoding tricks)
        special_char_count = len(re.findall(r'[^a-zA-Z0-9\s.,!?-]', text))
        if len(text) > 0 and special_char_count / len(text) > 0.3:
            return True
        
        # Check for very long repeated characters (encoding attack)
        if re.search(r'(.)\1{20,}', text):
            return True
        
        return False
