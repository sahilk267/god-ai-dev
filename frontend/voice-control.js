// Voice Control Module for AI Developer System

class VoiceControl {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.onCommand = null;
        this.supported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

        if (this.supported) {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'hi-IN';

            this.recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');

                if (event.results[0].isFinal) {
                    this.handleCommand(transcript);
                }
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateUI(false);
            };
        }
    }

    start(callback) {
        if (!this.supported) {
            alert('Voice control not supported in this browser');
            return false;
        }

        this.onCommand = callback;
        this.recognition.start();
        this.isListening = true;
        this.updateUI(true);
        return true;
    }

    stop() {
        if (this.recognition) {
            this.recognition.stop();
            this.isListening = false;
            this.updateUI(false);
        }
    }

    handleCommand(text) {
        console.log('Voice command:', text);
        text = text.toLowerCase();

        let command = null;

        if (text.includes('build') || text.includes('create')) {
            let prompt = text.replace(/build|create|make|develop/g, '').trim();
            command = { type: 'build', prompt: prompt };
        }
        else if (text.includes('save')) {
            command = { type: 'save' };
        }
        else if (text.includes('run') || text.includes('execute')) {
            command = { type: 'run' };
        }
        else if (text.includes('deploy')) {
            command = { type: 'deploy' };
        }
        else if (text.includes('stop')) {
            command = { type: 'stop' };
        }
        else if (text.includes('status')) {
            command = { type: 'status' };
        }

        if (command && this.onCommand) {
            this.onCommand(command);
            this.speak(`Executing ${command.type} command`);
        }
    }

    speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'hi-IN';
            window.speechSynthesis.speak(utterance);
        }
    }

    updateUI(isListening) {
        const btn = document.getElementById('voiceBtn');
        if (btn) {
            btn.style.background = isListening ? '#e74c3c' : '#2ecc71';
            btn.innerHTML = isListening ? '🎤 Listening...' : '🎤 Start Voice';
        }
    }
}

// Initialize voice control
const voiceControl = new VoiceControl();

// Add voice button to UI
function addVoiceButton() {
    const button = document.createElement('button');
    button.id = 'voiceBtn';
    button.innerHTML = '🎤 Start Voice';
    button.style.position = 'fixed';
    button.style.bottom = '20px';
    button.style.right = '20px';
    button.style.padding = '15px 30px';
    button.style.fontSize = '16px';
    button.style.background = '#2ecc71';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.borderRadius = '50px';
    button.style.cursor = 'pointer';
    button.style.zIndex = '9999';
    button.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';

    button.onclick = () => {
        if (voiceControl.isListening) {
            voiceControl.stop();
        } else {
            voiceControl.start((command) => {
                if (command.type === 'build') {
                    document.getElementById('prompt').value = command.prompt;
                    if (typeof startBuild === 'function') startBuild();
                } else if (command.type === 'save') {
                    if (typeof saveFile === 'function') saveFile();
                } else if (command.type === 'run') {
                    if (typeof runCode === 'function') runCode();
                } else if (command.type === 'deploy') {
                    if (typeof deploy === 'function') deploy();
                }
            });
        }
    };

    document.body.appendChild(button);
}

// Add voice button when DOM loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addVoiceButton);
} else {
    addVoiceButton();
}
