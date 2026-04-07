"""Voice control service for hands-free development"""

import asyncio
from typing import Optional, Callable
import speech_recognition as sr
from backend.core.logger import get_logger

logger = get_logger(__name__)

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.callback: Optional[Callable] = None
    
    def _init_mic(self):
        if self.microphone is None:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)

    async def start_listening(self, callback: Callable):
        """Start listening for voice commands"""
        self._init_mic()
        self.is_listening = True
        self.callback = callback
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    logger.info("Listening for command...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                try:
                    text = self.recognizer.recognize_google(audio, language="hi-IN")
                    logger.info(f"Voice command: {text}")
                    
                    if self.callback:
                        await self.callback(text)
                        
                except sr.UnknownValueError:
                    pass  # Didn't understand
                except sr.RequestError as e:
                    logger.error(f"Speech recognition error: {e}")
                    
                await asyncio.sleep(0.1)
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logger.error(f"Voice service error: {e}")
                await asyncio.sleep(1)
    
    async def stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
        logger.info("Voice listening stopped")
    
    async def convert_text_to_command(self, text: str) -> dict:
        """Convert voice text to system command"""
        text = text.lower()
        
        if "build" in text or "create" in text or "make" in text:
            # Extract the app description
            keywords = ["build", "create", "make", "develop"]
            for kw in keywords:
                text = text.replace(kw, "")
            
            return {
                "action": "build",
                "prompt": text.strip()
            }
        
        elif "stop" in text or "cancel" in text:
            return {"action": "stop"}
        
        elif "status" in text:
            return {"action": "status"}
        
        else:
            return {"action": "unknown", "text": text}

voice_service = VoiceService()
