import os
from typing import Dict, Any
import requests
from fastapi import HTTPException

class ContentModerationService:
    def __init__(self):
        self.api_token = os.getenv("HUGGING_FACE_API_TOKEN")
        if not self.api_token:
            raise ValueError("HUGGING_FACE_API_TOKEN environment variable is not set")
        
        self.api_url = "https://api-inference.huggingface.co/models/facebook/roberta-hate-speech-dynabench-r4-target"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    async def check_content(self, text: str) -> Dict[str, Any]:
        """
        Check if content contains inappropriate material.
        Returns a dictionary with toxicity scores and classification.
        """
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": text}
            )
            response.raise_for_status()
            result = response.json()
            
            # Process the response
            # The model returns scores for different categories of toxicity
            scores = result[0]
            
            # Determine if content should be flagged
            is_toxic = any(score > 0.7 for score in scores.values())
            
            return {
                "is_toxic": is_toxic,
                "scores": scores,
                "text": text
            }
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling content moderation API: {str(e)}"
            )
        
    def is_content_allowed(self, moderation_result: Dict[str, Any]) -> bool:
        """
        Determine if content should be allowed based on moderation results.
        Returns True if content is safe, False if it should be blocked.
        """
        return not moderation_result["is_toxic"]

# Create a singleton instance
content_moderator = ContentModerationService() 