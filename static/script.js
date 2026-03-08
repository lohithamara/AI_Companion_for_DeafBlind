// Configuration
const GRID_COLS = 25;
const GRID_ROWS = 10;
const TOTAL_CELLS = GRID_COLS * GRID_ROWS;

// Current state
let currentMode = 'AI Mode';
let displayedText = '';
let brailleCells = [];

// Modes
const MODES = ['AI Mode', 'Communication Mode', 'Story Mode'];
let currentModeIndex = 0;

// Initialize the application
function init() {
    createBrailleGrid();
    setupEventListeners();
    updateModeDisplay();
}

// Create the Braille grid (25x10 = 250 cells)
function createBrailleGrid() {
    const display = document.getElementById('brailleDisplay');
    display.innerHTML = '';
    brailleCells = [];
    
    for (let i = 0; i < TOTAL_CELLS; i++) {
        const cell = document.createElement('div');
        cell.className = 'braille-cell';
        cell.dataset.index = i;
        
        // Create 6 dots for each cell (2 columns x 3 rows)
        const dots = [];
        for (let j = 0; j < 6; j++) {
            const dot = document.createElement('div');
            dot.className = 'braille-dot';
            dot.dataset.dotIndex = j;
            cell.appendChild(dot);
            dots.push(dot);
        }
        
        display.appendChild(cell);
        brailleCells.push({ element: cell, dots: dots });
    }
}

// Display text on Braille board
function displayTextOnBraille(text) {
    clearBrailleDisplay();
    const patterns = textToBraille(text);
    
    // Display up to available cells
    const maxCells = Math.min(patterns.length, TOTAL_CELLS);
    
    for (let i = 0; i < maxCells; i++) {
        const pattern = patterns[i];
        const cell = brailleCells[i];
        
        // Activate dots based on pattern
        pattern.forEach((active, dotIndex) => {
            if (active === 1) {
                cell.dots[dotIndex].classList.add('active');
            }
        });
    }
    
    displayedText = text;
    document.getElementById('displayText').textContent = text;
}

// Clear all Braille dots
function clearBrailleDisplay() {
    brailleCells.forEach(cell => {
        cell.dots.forEach(dot => {
            dot.classList.remove('active');
        });
    });
    displayedText = '';
    document.getElementById('displayText').textContent = 'Ready...';
}

// Setup event listeners
function setupEventListeners() {
    // Mode button
    document.getElementById('modeBtn').addEventListener('click', async () => {
        currentModeIndex = (currentModeIndex + 1) % MODES.length;
        currentMode = MODES[currentModeIndex];
        updateModeDisplay();
        showModeMessage();
        
        // Update backend mode
        try {
            const modeMap = {
                'AI Mode': 'ai',
                'Communication Mode': 'communication',
                'Story Mode': 'story'
            };
            
            await fetch('/api/mode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mode: modeMap[currentMode]
                })
            });
        } catch (error) {
            console.error('Mode change error:', error);
        }
    });
    
    // Speak button (will be connected to speech recognition later)
    document.getElementById('speakBtn').addEventListener('click', () => {
        handleSpeakButton();
    });
    
    // Previous button
    document.getElementById('prevBtn').addEventListener('click', () => {
        handlePreviousButton();
    });
    
    // Next button
    document.getElementById('nextBtn').addEventListener('click', () => {
        handleNextButton();
    });
}

// Update mode display
function updateModeDisplay() {
    document.getElementById('currentMode').textContent = currentMode;
}

// Show mode change message
function showModeMessage() {
    let message = '';
    switch(currentMode) {
        case 'AI Mode':
            message = 'AI MODE ACTIVE';
            break;
        case 'Communication Mode':
            message = 'COMM MODE';
            break;
        case 'Story Mode':
            message = 'STORY MODE';
            break;
    }
    displayTextOnBraille(message);
    
    // Clear after 2 seconds
    setTimeout(() => {
        clearBrailleDisplay();
    }, 2000);
}

// Handle speak button
async function handleSpeakButton() {
    const speakBtn = document.getElementById('speakBtn');
    speakBtn.disabled = true;
    displayTextOnBraille('LISTENING');
    
    try {
        // Call backend speech-to-text API
        const response = await fetch('/api/speech-to-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const recognizedText = data.text.toUpperCase();
            displayTextOnBraille(recognizedText);
            
            // Process based on current mode
            await processInput(recognizedText);
        } else {
            displayTextOnBraille('ERROR: ' + (data.error || 'Speech recognition failed'));
        }
    } catch (error) {
        console.error('Speech recognition error:', error);
        displayTextOnBraille('ERROR: MICROPHONE ACCESS');
    } finally {
        speakBtn.disabled = false;
    }
}

// Process input based on current mode
async function processInput(text) {
    try {
        const modeMap = {
            'AI Mode': 'ai',
            'Communication Mode': 'communication',
            'Story Mode': 'story'
        };
        
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mode: modeMap[currentMode],
                text: text
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTextOnBraille(data.response.toUpperCase());
            
            // If story mode, handle pagination
            if (currentMode === 'Story Mode' && data.totalPages) {
                console.log(`Story loaded: Page ${data.page}/${data.totalPages}`);
            }
        } else {
            displayTextOnBraille('ERROR: ' + (data.error || 'Processing failed'));
        }
    } catch (error) {
        console.error('Processing error:', error);
        displayTextOnBraille('ERROR: SERVER CONNECTION');
    }
}

// Simulate speech input (placeholder - now deprecated, use handleSpeakButton)
function simulateSpeechInput() {
    const exampleQuestions = [
        'WHAT IS GRAVITY',
        'WHO INVENTED TELEPHONE',
        'WHAT IS AI',
        'WHERE IS RESTROOM'
    ];
    
    const question = exampleQuestions[Math.floor(Math.random() * exampleQuestions.length)];
    displayTextOnBraille(question);
    
    // Simulate AI response after 2 seconds
    setTimeout(() => {
        processAIResponse(question);
    }, 2000);
}

// Process AI response (with keyword extraction)
function processAIResponse(question) {
    // Example keyword-based responses
    const responses = {
        'WHAT IS GRAVITY': 'FORCE PULL EARTH OBJECTS',
        'WHO INVENTED TELEPHONE': 'ALEXANDER BELL INVENTOR 1876',
        'WHAT IS AI': 'ARTIFICIAL INTELLIGENCE MACHINE LEARNING',
        'WHERE IS RESTROOM': 'NEAR STAIRS LEFT'
    };
    
    const response = responses[question] || 'UNKNOWN QUERY';
    displayTextOnBraille(response);
}

// Handle next button
// Handle next button
// Handle previous button
async function handlePreviousButton() {
    if (currentMode === 'Story Mode') {
        try {
            const response = await fetch('/api/story/previous', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayTextOnBraille(data.content.toUpperCase());
                console.log(`Page ${data.page}/${data.totalPages}`);
            } else {
                displayTextOnBraille(data.message || 'START OF CONTENT');
            }
        } catch (error) {
            console.error('Navigation error:', error);
            displayTextOnBraille('ERROR: NAVIGATION FAILED');
        }
    } else {
        displayTextOnBraille('PREVIOUS');
        setTimeout(() => {
            clearBrailleDisplay();
        }, 1000);
    }
}

// Handle next button
async function handleNextButton() {
    if (currentMode === 'Story Mode') {
        try {
            const response = await fetch('/api/story/next', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayTextOnBraille(data.content.toUpperCase());
                console.log(`Page ${data.page}/${data.totalPages}`);
            } else {
                displayTextOnBraille(data.message || 'END OF CONTENT');
            }
        } catch (error) {
            console.error('Navigation error:', error);
            displayTextOnBraille('ERROR: NAVIGATION FAILED');
        }
    } else {
        displayTextOnBraille('NEXT');
        setTimeout(() => {
            clearBrailleDisplay();
        }, 1000);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Demo function - display welcome message
setTimeout(() => {
    displayTextOnBraille('WELCOME AI COMPANION');
}, 500);
