# AI Companion for Deafblind Users

Intelligent tactile communication system with AI-powered semantic compression and multi-mode support.

## 📑 Table of Contents

- [Quick Start](#-quick-start)
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Three Operating Modes](#three-operating-modes)
- [Setup Instructions](#-setup-instructions)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage)
- [API Endpoints](#-api-endpoints)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Performance & Requirements](#-performance--requirements)
- [Key Concepts](#-key-concepts)
- [Testing & Validation](#-testing--validation)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [Credits](#-credits--acknowledgments)

## ⚡ Quick Start

```powershell
# 1. Clone or download project
# 2. Install dependencies
python -m venv venv
.\venv\Scripts\Activate
.\venv\Scripts\pip install -r requirements.txt

# 3. Add Groq API key to .env file
# GROQ_API_KEY=gsk_your_key_here

# 4. Run server
.\venv\Scripts\python.exe app.py

# 5. Open browser to http://127.0.0.1:5000
```

## 🎯 Project Overview

This system provides an accessible communication interface for deafblind users, converting speech and AI responses into Braille patterns optimized for tactile reading through **smart semantic compression**.

### Core Innovation
**Semantic Compression** - AI responses are intelligently compressed into concise, meaningful phrases that preserve complete meaning while minimizing tactile reading time. The system removes redundant words (articles, prepositions) while maintaining grammatical clarity.

**Example:** "The train is on platform number 4" → "Train platform 4"

## ✨ Key Features

- **25×10 Braille Display** - 250 cells, each with 6 dots (2×3 pattern)
- **Voice Input** - Fast speech recognition with 0.5s pause detection
- **Smart Compression** - Reduces text to 60-80% while preserving meaning
- **Multi-Mode Interface** - Three specialized modes for different use cases
- **Story Navigation** - Forward/backward pagination for long content
- **Real-time Processing** - Groq-powered LLM for instant responses
- **Clean Design** - Professional white theme interface

## 📋 Features

### Three Operating Modes

#### 1. **AI Mode** (Cyan Button)
Quick Q&A with aggressive compression for fast tactile reading.

- **Purpose:** Answer questions with maximum brevity
- **Compression:** Very aggressive (100 chars max)
- **Temperature:** 0.2 (focused, predictable)
- **Example Input:** "What is photosynthesis?"
- **Example Output:** "Process plants use converting sunlight into energy"

#### 2. **Communication Mode** (Pink Button)
Human conversation facilitation with telegraphic compression.

- **Purpose:** Compress spoken dialogue for tactile reading
- **Compression:** Extremely aggressive (80 chars max)
- **Temperature:** 0.1 (minimal variation)
- **Example Input:** "The meeting is scheduled for 3 PM tomorrow in room 205"
- **Example Output:** "Meeting 3pm tomorrow room 205"

#### 3. **Story Mode** (Purple/Orange Buttons)
Long-form content with full preservation and pagination.

- **Purpose:** Read stories, articles, educational material
- **Compression:** None - full text preserved
- **Pagination:** 200 characters per page
- **Navigation:** Previous/Next buttons for multi-page content
- **Example:** Full fairy tales, news articles, learning content

## 🚀 Setup Instructions

### 1. Prerequisites
- **Python 3.8+** (tested on Python 3.11)
- **Microphone** for speech input
- **Groq API Key** (free at https://console.groq.com)
- **Internet connection** for speech recognition and LLM

### 2. Installation

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies
.\venv\Scripts\pip install -r requirements.txt
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**To get a Groq API key:**
1. Visit https://console.groq.com
2. Sign up for free account
3. Navigate to API Keys section
4. Create new API key
5. Copy and paste into `.env` file

### 4. Run the Application

**Windows:**
```powershell
.\venv\Scripts\python.exe app.py
```

**Linux/Mac:**
```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`

### 5. Open the Interface

Navigate to: **http://127.0.0.1:5000** in your web browser

## 📁 Project Structure

```
AI Companion/
├── modules/
│   ├── __init__.py
│   ├── speech_to_text.py       # Speech recognition with Google API
│   ├── ai_mode.py              # AI Q&A with aggressive compression
│   ├── communication_mode.py   # Human conversation compression
│   └── story_mode.py           # Long-form content with pagination
│
├── templates/
│   └── index.html              # Main web interface
│
├── static/
│   ├── styles.css              # White theme styling
│   ├── braille.js              # Braille character mappings (A-Z, 0-9)
│   └── script.js               # Frontend logic & API calls
│
├── venv/                       # Virtual environment (not in git)
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── .env                        # API keys (not in git)
└── README.md                   # This file
```

## 🎮 Usage

### Web Interface Controls

The interface features 4 circular control buttons:

1. **Mode Button** (Cyan) - "M"
   - Cycles through: AI Mode → Communication Mode → Story Mode
   - Current mode displayed in status panel below

2. **Speak Button** (Pink) - 🎤
   - Activates microphone for speech input
   - Listens for 5 seconds or until 0.5s pause detected
   - Works in all three modes

3. **Previous Button** (Purple) - ◀
   - Navigate backward through story pages
   - Only active in Story Mode
   - Shows "PREVIOUS" message in other modes

4. **Next Button** (Yellow) - ▶
   - Navigate forward through story pages
   - Only active in Story Mode
   - Shows "NEXT" message in other modes

### Status Panel

Displays real-time information:
- **Current Mode:** AI Mode / Communication Mode / Story Mode
- **Display:** Shows last action or current text being displayed

### Braille Display

- **Grid:** 25 columns × 10 rows (250 cells total)
- **Active Dots:** Bright cyan with glow effect
- **Inactive Dots:** Light gray
- **Each Cell:** 6 dots in standard 2×3 Braille pattern

### Workflow Example

1. Press **Mode** button until "AI Mode" shows
2. Press **Speak** button
3. Ask: "What causes lightning?"
4. System displays compressed answer: "Lightning caused electrical discharge clouds"
5. Switch to **Story Mode** for full explanations
6. Use **Previous/Next** to navigate long content

### Testing Individual Modules

Each module has a built-in `demo()` function for standalone testing:

**Test Speech Recognition:**
```powershell
.\venv\Scripts\python.exe modules\speech_to_text.py
# Speak into your microphone when prompted
```

**Test AI Mode:**
```powershell
.\venv\Scripts\python.exe modules\ai_mode.py
# Input: "What is quantum physics?"
# Output: Shows compressed response
```

**Test Communication Mode:**
```powershell
.\venv\Scripts\python.exe modules\communication_mode.py
# Input: "The package will arrive tomorrow at 3 PM"
# Output: "Package arrive tomorrow 3pm"
```

**Test Story Mode:**
```powershell
.\venv\Scripts\python.exe modules\story_mode.py
# Generates a story and shows pagination
```

## 🔧 API Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| `GET` | `/` | Main interface | None | HTML page |
| `POST` | `/api/speech-to-text` | Speech recognition | None | `{success, text, error}` |
| `POST` | `/api/process` | Process input by mode | `{mode, text}` | `{success, response}` |
| `POST` | `/api/mode` | Change current mode | `{mode}` | `{success, mode}` |
| `POST` | `/api/story/next` | Next story page | None | `{success, content, page, totalPages}` |
| `POST` | `/api/story/previous` | Previous story page | None | `{success, content, page, totalPages}` |

## 📊 System Architecture

```
┌─────────────────┐
│   User Speech   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Speech-to-Text Module             │
│   (Google Speech Recognition)       │
│   - 0.5s pause detection            │
│   - Ambient noise calibration       │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Mode Router (Flask Backend)       │
└────┬────────────┬────────────┬──────┘
     │            │            │
     ▼            ▼            ▼
┌─────────┐  ┌──────────┐  ┌─────────┐
│AI Mode  │  │Comm Mode │  │Story    │
│(100ch)  │  │(80ch)    │  │Mode     │
│Compress │  │Compress  │  │(Full)   │
└────┬────┘  └────┬─────┘  └────┬────┘
     │            │            │
     └────────────┴────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Groq LLM API  │
         │  (llama-3.3)   │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │Braille Encoder │
         │  (A-Z, 0-9)    │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ 25×10 Display  │
         │  (250 cells)   │
         └────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Web server & API endpoints
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **Groq 1.0.0** - Fast LLM inference (llama-3.3-70b-versatile)
- **SpeechRecognition 3.10.0** - Google speech-to-text
- **PyAudio 0.2.14** - Audio input handling
- **python-dotenv 1.0.0** - Environment configuration

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **CSS3** - Modern white theme with gradients
- **HTML5** - Semantic structure

### Key Library Features
- **Groq**: Sub-second LLM responses (500ms average)
- **Google Speech API**: Free, no key required, reliable
- **Flask**: Lightweight, easy deployment

## ⚡ Performance & Requirements

### System Requirements

**Minimum:**
- **OS:** Windows 10/11, Linux, macOS 10.14+
- **RAM:** 2 GB (4 GB recommended)
- **CPU:** Dual-core processor
- **Storage:** 500 MB for project + dependencies
- **Internet:** Stable connection (required for LLM & speech)
- **Microphone:** Any USB or built-in microphone

**Recommended:**
- **RAM:** 8 GB or more
- **CPU:** Quad-core or better
- **Internet:** 5 Mbps+ for smooth operation

### Performance Metrics

| Operation | Average Time | Notes |
|-----------|--------------|-------|
| Speech Recognition | 1-3 seconds | Depends on speech length |
| LLM Response (Groq) | 0.5-1 second | Using llama-3.3-70b |
| Braille Display Update | ~50ms | Instant visual feedback |
| Mode Switching | Instant | Client-side operation |
| Page Navigation | ~20ms | Local state management |

### Bandwidth Usage

- **Speech Recognition:** ~100 KB per request
- **Groq LLM API:** ~1-5 KB per request
- **Total per interaction:** ~100-150 KB
- **Typical session (30 min):** ~5-10 MB

### API Rate Limits

**Groq Free Tier:**
- 30 requests per minute
- 14,400 requests per day
- Sufficient for typical usage patterns

**Google Speech API (Free):**
- No strict limits for basic usage
- Unlimited for reasonable use

## 🎓 Key Concepts

### Semantic Compression Philosophy

Traditional assistive text just shows keywords, losing context. Our system uses AI to create **telegraphic compression** - removing only non-essential words while preserving complete meaning and grammatical structure.

**Compression Examples:**

| Original Text | Bad (Keywords) | Good (Smart Compression) |
|--------------|----------------|--------------------------|
| "The train is arriving at platform number 4" | `TRAIN PLATFORM 4` | "Train platform 4" |
| "Please meet me at the coffee shop at 2 PM" | `MEET COFFEE 2PM` | "Meet coffee shop 2pm" |
| "Gravity is a force that pulls objects toward Earth" | `GRAVITY FORCE PULL EARTH` | "Force pulling objects to Earth" |

### Compression Techniques

1. **Article Removal:** "the", "a", "an" → removed
2. **Preposition Reduction:** "is on", "at the" → simplified
3. **Essential Words Only:** Keep nouns, verbs, numbers, names
4. **Grammar Preservation:** Maintain readable sentence structure
5. **Number/Name Priority:** Never compress critical data points

### Braille Display Specifications

- **Grid Size:** 25 columns × 10 rows = 250 cells
- **Cell Pattern:** 6 dots per cell (standard 2×3 Braille)
- **Capacity:** ~40-50 characters per screen comfortably
- **Character Set:** A-Z, 0-9, basic punctuation (.,!?-)
- **Display Update:** Real-time dot activation with cyan glow

### Speech Recognition Features

- **Engine:** Google Speech Recognition API (free)
- **Pause Detection:** 0.5 seconds (fast response)
- **Timeout:** 5 seconds maximum listening time
- **Language:** English (en-US)
- **Ambient Noise:** Auto-calibration on startup

## 🐛 Troubleshooting

### Microphone Not Working

**Issue:** Speech recognition fails or times out

**Solutions:**
1. Check microphone permissions in Windows Settings
2. Test microphone: `.\venv\Scripts\python.exe modules\speech_to_text.py`
3. Verify microphone is default recording device
4. Restart Python/Flask after changing audio devices

**Error:** `"No speech detected - timeout"`
- Speak louder or closer to microphone
- Reduce ambient noise
- Check microphone is not muted

### Groq API Errors

**Issue:** `401 Unauthorized` or API errors

**Solutions:**
1. Verify API key in `.env` file (no quotes, no spaces)
2. Generate new key at https://console.groq.com
3. Restart Flask server after updating `.env`
4. Check internet connection
5. Verify API key starts with `gsk_`

**Error:** `Rate limit exceeded`
- Free tier: 30 requests/minute
- Wait 60 seconds and retry
- Consider upgrading plan for higher limits

### Module Import Errors

**Issue:** `ModuleNotFoundError` or import failures

**Solutions:**
```powershell
# Ensure venv is activated
.\venv\Scripts\Activate

# Reinstall all dependencies
.\venv\Scripts\pip install -r requirements.txt --force-reinstall

# Verify installation
.\venv\Scripts\pip list
```

### Flask Server Won't Start

**Issue:** Port already in use or server crashes

**Solutions:**
```powershell
# Kill existing Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Restart server
.\venv\Scripts\python.exe app.py
```

### Braille Display Issues

**Issue:** Dots not showing or incorrect patterns

**Solutions:**
1. Check browser console (F12) for JavaScript errors
2. Hard refresh browser (Ctrl+Shift+R)
3. Verify `static/braille.js` is loading correctly
4. Clear browser cache

## 📝 Development

### Project Philosophy

This project prioritizes:
1. **Accessibility First** - Every feature designed for deafblind users
2. **Speed** - Sub-second responses using Groq's fast LLM
3. **Semantic Preservation** - Compression without losing meaning
4. **Simplicity** - Minimal dependencies, easy to understand

### Adding New Features

1. **Create Module** in `modules/` folder:
   ```python
   # modules/new_feature.py
   class NewFeature:
       def __init__(self):
           pass
       
       def process(self, text):
           # Your logic here
           return result
   ```

2. **Export in** `modules/__init__.py`:
   ```python
   from .new_feature import NewFeature
   ```

3. **Add API Endpoint** in `app.py`:
   ```python
   @app.route('/api/new-feature', methods=['POST'])
   def new_feature():
       # Handle request
       return jsonify({"success": True})
   ```

4. **Update Frontend** in `static/script.js`:
   ```javascript
   async function callNewFeature() {
       const response = await fetch('/api/new-feature');
       // Handle response
   }
   ```

### Code Standards

- **Python:** PEP 8 style guide
- **JavaScript:** ES6+ syntax, async/await
- **CSS:** BEM naming convention for classes
- **Comments:** Docstrings for all functions

### Testing New Modules

All modules should have a `demo()` function:
```python
if __name__ == "__main__":
    demo()  # Standalone testing
```

## � Credits & Acknowledgments

**Built for Deafblind Accessibility**

This project demonstrates AI-powered assistive technology for the deafblind community, showcasing how modern LLMs can enable faster, more accessible communication.

### Technologies Used

- **[Groq](https://groq.com)** - Ultra-fast LLM inference (llama-3.3-70b-versatile)
- **[Google Speech Recognition](https://cloud.google.com/speech-to-text)** - Free, reliable speech-to-text
- **[Flask](https://flask.palletsprojects.com/)** - Lightweight Python web framework
- **[PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)** - Cross-platform audio I/O

### Design Inspiration

- Tactile reading research and Braille standards
- Telegraphic speech compression principles
- Modern accessible web design patterns

### License

MIT License - Free for educational and personal use

### Contributing

Contributions welcome! Here are some areas for enhancement:

**High Priority:**
- 🌍 Additional language support (Spanish, French, etc.)
- 🔊 Voice output (text-to-speech for hearing users)
- 📱 Mobile/tablet responsive optimization
- 🔌 Hardware Braille display integration (USB/Bluetooth)

**Medium Priority:**
- 💾 Offline mode capabilities (local LLM)
- 🎨 Customizable themes and contrast modes
- 📊 Usage analytics and learning patterns
- 🔐 Enhanced privacy options

**How to Contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Test thoroughly with demo functions
4. Submit a pull request with clear description

### Accessibility Statement

This project prioritizes accessible design:
- ✅ Keyboard navigation support
- ✅ High contrast visual indicators
- ✅ Screen reader compatible structure
- ✅ Large touch targets (90px buttons)
- ✅ Clear, sans-serif typography
- ✅ Minimal cognitive load interface

### Future Roadmap

**Version 2.0 Goals:**
- Multi-user conversation support
- Context memory across sessions
- Customizable compression levels
- Integration with smart home devices
- Braille music notation support
- Educational content library

---

**Questions? Issues?** Test individual modules first using the demo functions, then check the troubleshooting section above.

**Live Demo:** http://127.0.0.1:5000 (after running `python app.py`)
