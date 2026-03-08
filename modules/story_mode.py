"""
Story Mode Module for AI Companion
Handles long-form content with pagination (NO compression)
"""

import os
from groq import Groq
from dotenv import load_dotenv
import logging
from typing import List, Tuple, Optional
import textwrap

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StoryMode:
    """
    Story Mode - Displays full text stories/articles with pagination
    NO compression - preserves complete content
    """
    
    def __init__(self, api_key: Optional[str] = None, chars_per_page: int = 200):
        """
        Initialize Story Mode with Groq
        
        Args:
            api_key: Groq API key (defaults to .env)
            chars_per_page: Maximum characters per page (default: 200)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.chars_per_page = chars_per_page
        self.current_story = None
        self.pages = []
        self.current_page = 0
        logger.info("Story Mode initialized")
    
    def generate_story(self, topic: str, length: str = "short") -> Tuple[bool, str]:
        """
        Generate a story about a topic
        
        Args:
            topic: Story topic
            length: "short" (300 words), "medium" (500 words), "long" (800 words)
            
        Returns:
            Tuple of (success: bool, story: str or error_message: str)
        """
        try:
            logger.info(f"Generating {length} story about: {topic}")
            
            word_limits = {
                "short": 300,
                "medium": 500,
                "long": 800
            }
            
            word_limit = word_limits.get(length, 300)
            
            system_prompt = f"""You are a creative storyteller.

Generate an engaging story about: {topic}

RULES:
1. Make it interesting and easy to understand
2. Use simple, clear language
3. Write approximately {word_limit} words
4. Include a beginning, middle, and end
5. Use complete sentences and proper grammar
6. NO compression - write full, natural text
"""
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Write a story about: {topic}"}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=word_limit * 2,  # Rough token estimate
            )
            
            story = chat_completion.choices[0].message.content.strip()
            logger.info(f"Generated story: {len(story)} characters")
            
            return True, story
        
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            return False, f"Error: {str(e)}"
    
    def fetch_article(self, topic: str) -> Tuple[bool, str]:
        """
        Fetch educational article about a topic
        
        Args:
            topic: Article topic
            
        Returns:
            Tuple of (success: bool, article: str)
        """
        try:
            logger.info(f"Fetching article about: {topic}")
            
            system_prompt = """You are an educational content writer.

Write a clear, informative article about the given topic.

RULES:
1. Use simple, accessible language
2. Explain concepts clearly
3. Include examples where helpful
4. Around 400-500 words
5. Complete sentences and proper structure
6. NO compression - full text
"""
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Write an article about: {topic}"}
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=1000,
            )
            
            article = chat_completion.choices[0].message.content.strip()
            logger.info(f"Generated article: {len(article)} characters")
            
            return True, article
        
        except Exception as e:
            logger.error(f"Error fetching article: {e}")
            return False, f"Error: {str(e)}"
    
    def load_content(self, content: str) -> bool:
        """
        Load content and split into pages
        
        Args:
            content: Full text content
            
        Returns:
            True if successful
        """
        try:
            self.current_story = content
            self.pages = self._split_into_pages(content)
            self.current_page = 0
            logger.info(f"Loaded content: {len(self.pages)} pages")
            return True
        
        except Exception as e:
            logger.error(f"Error loading content: {e}")
            return False
    
    def _split_into_pages(self, content: str) -> List[str]:
        """
        Split content into pages by character limit
        Tries to break at sentence boundaries
        """
        pages = []
        remaining = content
        
        while remaining:
            if len(remaining) <= self.chars_per_page:
                pages.append(remaining)
                break
            
            # Try to break at sentence end
            chunk = remaining[:self.chars_per_page]
            
            # Look for sentence ending punctuation
            last_period = max(chunk.rfind('. '), chunk.rfind('! '), chunk.rfind('? '))
            
            if last_period > self.chars_per_page * 0.6:  # At least 60% of page
                split_point = last_period + 2  # Include punctuation and space
            else:
                # Break at last space
                last_space = chunk.rfind(' ')
                split_point = last_space if last_space > 0 else self.chars_per_page
            
            pages.append(remaining[:split_point].strip())
            remaining = remaining[split_point:].strip()
        
        return pages
    
    def get_current_page(self) -> Tuple[int, int, str]:
        """
        Get current page content
        
        Returns:
            Tuple of (current_page_num, total_pages, page_content)
        """
        if not self.pages:
            return 0, 0, ""
        
        return self.current_page + 1, len(self.pages), self.pages[self.current_page]
    
    def next_page(self) -> Tuple[bool, str]:
        """
        Navigate to next page
        
        Returns:
            Tuple of (has_next: bool, page_content: str)
        """
        if not self.pages:
            return False, "No content loaded"
        
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            return True, self.pages[self.current_page]
        else:
            return False, "End of content"
    
    def previous_page(self) -> Tuple[bool, str]:
        """
        Navigate to previous page
        
        Returns:
            Tuple of (has_previous: bool, page_content: str)
        """
        if not self.pages:
            return False, "No content loaded"
        
        if self.current_page > 0:
            self.current_page -= 1
            return True, self.pages[self.current_page]
        else:
            return False, "Start of content"
    
    def goto_page(self, page_num: int) -> Tuple[bool, str]:
        """
        Go to specific page
        
        Args:
            page_num: Page number (1-indexed)
            
        Returns:
            Tuple of (success: bool, page_content: str)
        """
        if not self.pages:
            return False, "No content loaded"
        
        if 1 <= page_num <= len(self.pages):
            self.current_page = page_num - 1
            return True, self.pages[self.current_page]
        else:
            return False, f"Invalid page number (1-{len(self.pages)})"


def demo():
    """
    Demo function to test Story Mode
    """
    print("=" * 50)
    print("Story Mode Demo")
    print("=" * 50)
    
    try:
        story_mode = StoryMode(chars_per_page=200)
        
        print("\nOptions:")
        print("1. Generate story")
        print("2. Generate article")
        print("3. Load custom text")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        content = None
        
        if choice == "1":
            topic = input("Story topic: ").strip()
            print(f"\n📖 Generating story about '{topic}'...\n")
            success, content = story_mode.generate_story(topic, "short")
            
            if not success:
                print(f"❌ Error: {content}")
                return
        
        elif choice == "2":
            topic = input("Article topic: ").strip()
            print(f"\n📰 Generating article about '{topic}'...\n")
            success, content = story_mode.fetch_article(topic)
            
            if not success:
                print(f"❌ Error: {content}")
                return
        
        elif choice == "3":
            content = input("Enter text to display: ").strip()
        
        else:
            print("Invalid choice!")
            return
        
        # Load content
        if content:
            story_mode.load_content(content)
            
            # Display with pagination
            while True:
                page_num, total, page_content = story_mode.get_current_page()
                
                print("\n" + "=" * 50)
                print(f"Page {page_num}/{total}")
                print("=" * 50)
                print(page_content)
                print("\n" + "=" * 50)
                
                if page_num < total:
                    action = input("\n[N]ext | [P]revious | [G]oto | [Q]uit: ").strip().lower()
                else:
                    action = input("\n[P]revious | [G]oto | [Q]uit (End of content): ").strip().lower()
                
                if action == 'n':
                    has_next, msg = story_mode.next_page()
                    if not has_next:
                        print(f"ℹ️  {msg}")
                
                elif action == 'p':
                    has_prev, msg = story_mode.previous_page()
                    if not has_prev:
                        print(f"ℹ️  {msg}")
                
                elif action == 'g':
                    page = input(f"Go to page (1-{total}): ").strip()
                    try:
                        success, msg = story_mode.goto_page(int(page))
                        if not success:
                            print(f"❌ {msg}")
                    except ValueError:
                        print("❌ Invalid page number")
                
                elif action == 'q':
                    print("\nGoodbye!")
                    break
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please set GROQ_API_KEY in your .env file")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    demo()
