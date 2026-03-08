"""
Communication Mode Module for AI Companion
Handles human-to-human conversation with smart compression
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


class CommunicationMode:
    """
    Communication Mode - Facilitates conversation between user and others
    Compresses responses for tactile reading
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Communication Mode with Groq
        
        Args:
            api_key: Groq API key (defaults to .env)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.conversation_history = []
        logger.info("Communication Mode initialized")
    
    def compress_speech(self, text: str) -> Tuple[bool, str]:
        """
        Compress human speech for Braille display
        
        Args:
            text: Text to compress
            
        Returns:
            Tuple of (success: bool, compressed_text: str)
        """
        try:
            logger.info(f"Compressing speech: {text}")
            
            # If text is already very short, return as-is
            if len(text) <= 30:
                return True, text
            
            # Create aggressive compression prompt
            system_prompt = """You are a text compression expert for deafblind Braille users who read slowly.

TASK: Compress text to ABSOLUTE MINIMUM words while preserving complete meaning.

COMPRESSION RULES:
1. Remove ALL articles (the, a, an, this, that)
2. Remove unnecessary prepositions (on, at, in, to) when meaning is clear
3. Remove "is", "are", "will be" when obvious
4. Keep ONLY essential words: nouns, numbers, key verbs, locations
5. Maximum 80 characters
6. Meaning must be 100% clear and accurate
7. Keep names, numbers, and critical details

Examples:

Input: "The train is on platform number 4."
Output: "Train platform 4"

Input: "The restroom is located next to the stairs on your left side."
Output: "Restroom next to stairs left"

Input: "Your appointment is scheduled for 3 PM tomorrow."
Output: "Appointment 3 PM tomorrow"

Input: "I'm sorry but I don't know where that is located."
Output: "Don't know location"

Input: "Please wait here while I check the information."
Output: "Wait here checking info"

Input: "The meeting will start in conference room B at 2 o'clock."
Output: "Meeting room B 2 o'clock"
"""
            
            # Get compressed response
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Compress: {text}"}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=50,
            )
            
            compressed = chat_completion.choices[0].message.content.strip()
            logger.info(f"Compressed: {compressed}")
            
            # Ensure within limit
            if len(compressed) > 80:
                compressed = compressed[:77] + "..."
            
            return True, compressed
        
        except Exception as e:
            logger.error(f"Error compressing speech: {e}")
            return False, f"Error: {str(e)}"
    
    def translate_to_speech(self, braille_input: str) -> Tuple[bool, str]:
        """
        Convert user's Braille input to natural speech for others
        
        Args:
            braille_input: User's input text
            
        Returns:
            Tuple of (success: bool, natural_text: str)
        """
        try:
            logger.info(f"Translating to speech: {braille_input}")
            
            system_prompt = """You are a speech enhancer for deafblind users.

TASK: Convert short/compressed input into natural, polite speech.

RULES:
1. Make it sound natural and conversational
2. Add polite phrases where appropriate
3. Keep it brief but friendly
4. Maximum 200 characters

Example:
Input: "where restroom"
Output: "Excuse me, could you tell me where the restroom is?"

Input: "need help"
Output: "Hi, I need some help please."
"""
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Enhance: {braille_input}"}
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=100,
            )
            
            natural = chat_completion.choices[0].message.content.strip()
            logger.info(f"Natural speech: {natural}")
            
            return True, natural
        
        except Exception as e:
            logger.error(f"Error translating to speech: {e}")
            return False, f"Error: {str(e)}"
    
    def process_conversation(self, incoming_speech: str) -> Tuple[bool, str]:
        """
        Process incoming conversation and return compressed version
        
        Args:
            incoming_speech: What someone said to the user
            
        Returns:
            Tuple of (success: bool, compressed_text: str)
        """
        # Store in conversation history
        self.conversation_history.append(incoming_speech)
        
        # Compress for display
        return self.compress_speech(incoming_speech)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")


def demo():
    """
    Demo function to test Communication Mode
    """
    print("=" * 50)
    print("Communication Mode Demo")
    print("=" * 50)
    
    try:
        comm = CommunicationMode()
        
        print("\n--- Test 1: Compress incoming speech ---")
        test_speeches = [
            "Hi there! The restroom is located right next to the stairs on your left.",
            "I'm sorry but I don't know where that is. Maybe ask at the front desk?",
            "Yes, the meeting will start at 3 PM in conference room B on the second floor.",
        ]
        
        for speech in test_speeches:
            print(f"\n📢 Original: {speech}")
            success, compressed = comm.compress_speech(speech)
            if success:
                print(f"✅ Compressed: {compressed}")
                print(f"   ({len(speech)} → {len(compressed)} chars)")
            else:
                print(f"❌ Error: {compressed}")
        
        print("\n\n--- Test 2: Enhance user input to speech ---")
        test_inputs = [
            "where restroom",
            "need help",
            "thank you",
        ]
        
        for user_input in test_inputs:
            print(f"\n💬 User types: {user_input}")
            success, natural = comm.translate_to_speech(user_input)
            if success:
                print(f"🔊 Says: {natural}")
            else:
                print(f"❌ Error: {natural}")
        
        # Interactive mode
        print("\n\n" + "=" * 50)
        print("Interactive Mode")
        print("1. Type speech to compress")
        print("2. Type 'exit' to quit")
        print("=" * 50)
        
        while True:
            text = input("\n📢 Enter text: ").strip()
            
            if text.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            if not text:
                continue
            
            success, result = comm.compress_speech(text)
            if success:
                print(f"✅ {result}")
            else:
                print(f"❌ {result}")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please set GROQ_API_KEY in your .env file")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    demo()
