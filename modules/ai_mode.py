"""
AI Mode Module for AI Companion
Handles AI question-answering with smart semantic compression
"""

import os
from groq import Groq
from dotenv import load_dotenv
import logging
from typing import Optional, Tuple

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIMode:
    """
    AI Mode - Provides quick answers with smart compression
    Extracts key concepts while maintaining meaning
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Mode with Groq
        
        Args:
            api_key: Groq API key (defaults to .env)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Fast Groq model
        logger.info("AI Mode initialized")
    
    def process_question(self, question: str) -> Tuple[bool, str]:
        """
        Process a question and return compressed answer
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (success: bool, answer: str)
        """
        try:
            logger.info(f"Processing question: {question}")
            
            # Create aggressive compression prompt
            system_prompt = """You are an AI assistant for deafblind users who read Braille very slowly.

CRITICAL COMPRESSION RULES:
1. Answer accurately with MINIMAL words
2. Remove articles (the, a, an)
3. Remove obvious prepositions and "to be" verbs
4. Keep key nouns, numbers, verbs, and essential details
5. Maximum 100 characters
6. Answer must be complete and accurate
7. Use telegraphic style but maintain clarity

Examples:

Q: "What is gravity?"
Bad: "Gravity is a force that pulls objects toward Earth"
Good: "Force pulling objects to Earth"

Q: "Who invented the telephone?"
Good: "Alexander Graham Bell 1876"

Q: "What is machine learning?"
Good: "AI system learning from data patterns"

Q: "How does photosynthesis work?"
Good: "Plants convert sunlight to energy using chlorophyll"

Q: "What is the capital of France?"
Good: "Paris"

Q: "When did World War 2 end?"
Good: "1945"
"""
            
            # Get response from Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                model=self.model,
                temperature=0.2,
                max_tokens=75,
            )
            
            answer = chat_completion.choices[0].message.content.strip()
            logger.info(f"Generated answer: {answer}")
            
            # Ensure answer is within character limit
            if len(answer) > 100:
                answer = answer[:97] + "..."
            
            return True, answer
        
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return False, f"Error: {str(e)}"
    
    def get_quick_fact(self, topic: str) -> Tuple[bool, str]:
        """
        Get a quick fact about a topic
        
        Args:
            topic: Topic to get fact about
            
        Returns:
            Tuple of (success: bool, fact: str)
        """
        question = f"Give me one interesting fact about {topic}"
        return self.process_question(question)


def demo():
    """
    Demo function to test AI Mode
    """
    print("=" * 50)
    print("AI Mode Demo")
    print("=" * 50)
    
    try:
        ai = AIMode()
        
        # Test questions
        test_questions = [
            "What is gravity?",
            "Who invented the telephone?",
            "What is machine learning?",
            "How does photosynthesis work?",
        ]
        
        for question in test_questions:
            print(f"\n❓ Q: {question}")
            success, answer = ai.process_question(question)
            
            if success:
                print(f"✅ A: {answer}")
                print(f"   (Length: {len(answer)} chars)")
            else:
                print(f"❌ Error: {answer}")
        
        # Interactive mode
        print("\n" + "=" * 50)
        print("Interactive Mode (type 'exit' to quit)")
        print("=" * 50)
        
        while True:
            question = input("\n❓ Your question: ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            if not question:
                continue
            
            success, answer = ai.process_question(question)
            
            if success:
                print(f"✅ {answer}")
            else:
                print(f"❌ {answer}")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please set GROQ_API_KEY in your .env file")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    demo()
