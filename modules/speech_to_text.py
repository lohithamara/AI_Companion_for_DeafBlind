"""
Speech-to-Text Module for AI Companion
Converts spoken audio input into text for processing
"""

from typing import Optional, Tuple
import logging
import speech_recognition as sr

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechToText:
    """
    Handles speech recognition from microphone input
    """
    
    def __init__(self, language: str = "en-US"):
        """
        Initialize the speech recognition system
        
        Args:
            language: Language code (default: en-US)
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        
        # Reduce pause threshold for faster response (default is 0.8)
        self.recognizer.pause_threshold = 0.5
        
        # Adjust for ambient noise on initialization
        logger.info("Calibrating microphone for ambient noise...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone ready!")
        except Exception as e:
            logger.error(f"Microphone initialization failed: {e}")
            self.recognizer = None
            self.microphone = None
    
    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 5) -> Tuple[bool, str]:
        """
        Listen for a single speech input
        
        Args:
            timeout: Maximum seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            Tuple of (success: bool, text: str or error_message: str)
        """
        if not self.recognizer or not self.microphone:
            return False, "Microphone not available"
            
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
            logger.info("Processing speech...")
            
            # Try Google Speech Recognition (free)
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"Recognized: {text}")
                return True, text
            
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return False, "Could not understand audio"
            
            except sr.RequestError as e:
                logger.error(f"API error: {e}")
                return False, f"Speech recognition service error: {e}"
        
        except sr.WaitTimeoutError:
            logger.warning("No speech detected")
            return False, "No speech detected - timeout"
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False, f"Error: {str(e)}"
    
    def listen_continuous(self, callback, stop_phrases: list = ["stop listening", "exit"]):
        """
        Continuously listen for speech input until a stop phrase is detected
        
        Args:
            callback: Function to call with recognized text
            stop_phrases: List of phrases that will stop listening
        """
        logger.info("Starting continuous listening mode...")
        logger.info(f"Say '{stop_phrases[0]}' to stop")
        
        with self.microphone as source:
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
                    
                    try:
                        text = self.recognizer.recognize_google(audio, language=self.language)
                        logger.info(f"Recognized: {text}")
                        
                        # Check for stop phrases
                        if any(phrase.lower() in text.lower() for phrase in stop_phrases):
                            logger.info("Stop phrase detected. Exiting...")
                            break
                        
                        # Call the callback with recognized text
                        callback(text)
                    
                    except sr.UnknownValueError:
                        logger.debug("Could not understand audio")
                        continue
                    
                    except sr.RequestError as e:
                        logger.error(f"API error: {e}")
                        break
                
                except sr.WaitTimeoutError:
                    continue
                
                except KeyboardInterrupt:
                    logger.info("Interrupted by user")
                    break
    
    def test_microphone(self) -> bool:
        """
        Test if the microphone is working
        
        Returns:
            True if microphone is accessible, False otherwise
        """
        try:
            with self.microphone as source:
                logger.info("Microphone test successful")
                return True
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False


def demo():
    """
    Demo function to test speech-to-text functionality
    """
    print("=" * 50)
    print("Speech-to-Text Demo")
    print("=" * 50)
    
    # Initialize speech recognizer
    stt = SpeechToText()
    
    # Test microphone
    if not stt.test_microphone():
        print("❌ Microphone not accessible!")
        return
    
    print("\n✅ Microphone ready!")
    print("\nOptions:")
    print("1. Single input test")
    print("2. Continuous listening")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n🎤 Speak now...")
        success, result = stt.listen_once(timeout=10)
        
        if success:
            print(f"\n✅ You said: {result}")
        else:
            print(f"\n❌ Error: {result}")
    
    elif choice == "2":
        print("\n🎤 Continuous listening active...")
        print("Say 'stop listening' to exit\n")
        
        def handle_speech(text):
            print(f"📝 Captured: {text}")
        
        stt.listen_continuous(callback=handle_speech)
        print("\n✅ Listening stopped")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    demo()
