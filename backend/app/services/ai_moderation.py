import requests
from typing import Dict, Optional, Tuple
from app.core.config import settings
from app.models.notification import SeverityLevel as ContentSeverity

class AIModeration:
    def __init__(self):
        self.api_token = settings.HUGGING_FACE_API_TOKEN
        self.api_url = "https://api-inference.huggingface.co/models/facebook/roberta-hate-speech-dynabench-r4-target"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    async def analyze_content(self, content: str) -> Dict:
        """
        Analyze content using Hugging Face API for content moderation
        Returns a dict with moderation results
        """
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": content}
            )
            result = response.json()

            # Process the response and determine severity
            severity, reason = self._process_response(result)

            return {
                "is_negative": severity is not None,
                "severity": severity,
                "reason": reason
            }
        except Exception as e:
            print(f"Error in content moderation: {str(e)}")
            return {
                "is_negative": False,
                "severity": None,
                "reason": "Error in content moderation"
            }

    def _process_response(self, result: list) -> Tuple[Optional[ContentSeverity], Optional[str]]:
        """
        Process the Hugging Face API response and determine content severity
        """
        try:
            # Get the highest probability classification
            scores = result[0]
            hate_score = next((item['score'] for item in scores if item['label'] == 'hate'), 0)
            offensive_score = next((item['score'] for item in scores if item['label'] == 'offensive'), 0)

            if hate_score > 0.7:
                return ContentSeverity.HIGH, "Content contains hate speech"
            elif hate_score > 0.4 or offensive_score > 0.7:
                return ContentSeverity.MEDIUM, "Content may be offensive"
            elif offensive_score > 0.4:
                return ContentSeverity.LOW, "Content may be inappropriate"
            else:
                return None, None

        except Exception as e:
            print(f"Error processing moderation response: {str(e)}")
            return None, None

ai_moderator = AIModeration() 