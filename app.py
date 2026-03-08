"""
Main Application for AI Companion
Integrates all modules with Flask backend
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

from modules import SpeechToText, AIMode, CommunicationMode, StoryMode

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)

# Initialize modules
try:
    stt = SpeechToText()
    ai_mode = AIMode()
    comm_mode = CommunicationMode()
    story_mode = StoryMode()
    logger.info("All modules initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize modules: {e}")
    stt = ai_mode = comm_mode = story_mode = None

# Current mode state
current_mode = "ai"  # ai, communication, story


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """
    Endpoint for speech recognition
    """
    try:
        if not stt:
            return jsonify({"success": False, "error": "Speech module not initialized"}), 500
        
        # Listen for speech (reduced timeout for faster response)
        success, result = stt.listen_once(timeout=5, phrase_time_limit=5)
        
        return jsonify({
            "success": success,
            "text": result if success else "",
            "error": result if not success else None
        })
    
    except Exception as e:
        logger.error(f"Speech recognition error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_input():
    """
    Process input based on current mode
    """
    try:
        data = request.json
        mode = data.get('mode', current_mode)
        text = data.get('text', '')
        
        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400
        
        logger.info(f"Processing in {mode} mode: {text}")
        
        if mode == "ai":
            if not ai_mode:
                return jsonify({"success": False, "error": "AI mode not initialized"}), 500
            success, response = ai_mode.process_question(text)
        
        elif mode == "communication":
            if not comm_mode:
                return jsonify({"success": False, "error": "Communication mode not initialized"}), 500
            success, response = comm_mode.compress_speech(text)
        
        elif mode == "story":
            if not story_mode:
                return jsonify({"success": False, "error": "Story mode not initialized"}), 500
            success, response = story_mode.generate_story(text)
            
            if success:
                story_mode.load_content(response)
                page_num, total, page_content = story_mode.get_current_page()
                return jsonify({
                    "success": True,
                    "response": page_content,
                    "page": page_num,
                    "totalPages": total
                })
        
        else:
            return jsonify({"success": False, "error": "Invalid mode"}), 400
        
        return jsonify({
            "success": success,
            "response": response if success else "",
            "error": response if not success else None
        })
    
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/story/next', methods=['POST'])
def story_next():
    """Navigate to next story page"""
    try:
        if not story_mode:
            return jsonify({"success": False, "error": "Story mode not initialized"}), 500
        
        has_next, content = story_mode.next_page()
        page_num, total, _ = story_mode.get_current_page()
        
        return jsonify({
            "success": has_next,
            "content": content if has_next else "",
            "page": page_num,
            "totalPages": total,
            "message": content if not has_next else ""
        })
    
    except Exception as e:
        logger.error(f"Story navigation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/story/previous', methods=['POST'])
def story_previous():
    """Navigate to previous story page"""
    try:
        if not story_mode:
            return jsonify({"success": False, "error": "Story mode not initialized"}), 500
        
        has_prev, content = story_mode.previous_page()
        page_num, total, _ = story_mode.get_current_page()
        
        return jsonify({
            "success": has_prev,
            "content": content if has_prev else "",
            "page": page_num,
            "totalPages": total,
            "message": content if not has_prev else ""
        })
    
    except Exception as e:
        logger.error(f"Story navigation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mode', methods=['POST'])
def change_mode():
    """Change current mode"""
    global current_mode
    
    try:
        data = request.json
        new_mode = data.get('mode', '')
        
        if new_mode not in ['ai', 'communication', 'story']:
            return jsonify({"success": False, "error": "Invalid mode"}), 400
        
        current_mode = new_mode
        logger.info(f"Mode changed to: {current_mode}")
        
        mode_names = {
            'ai': 'AI Mode',
            'communication': 'Communication Mode',
            'story': 'Story Mode'
        }
        
        return jsonify({
            "success": True,
            "mode": current_mode,
            "modeName": mode_names[current_mode]
        })
    
    except Exception as e:
        logger.error(f"Mode change error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "modules": {
            "speech": stt is not None,
            "ai": ai_mode is not None,
            "communication": comm_mode is not None,
            "story": story_mode is not None
        }
    })


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting AI Companion server on localhost:{port}")
    app.run(host='127.0.0.1', port=port, debug=debug)
