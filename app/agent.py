import json
import logging
from typing import List, Dict

logger = logging.getLogger("vagabond_agent")

class VagabondAgent:
    def __init__(self, system_instruction: str, max_history_len: int = 5):
        self.system_instruction = system_instruction
        self.history: List[Dict] = []
        self.max_history_len = max_history_len

    def add_message(self, role: str, content: str):
        """Adds a message and implements context compaction (memory management)."""
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history_len:
            self.compact_memory()

    def compact_memory(self):
        """Summarizes and compacts older context to save memory tokens."""
        logger.info("Compacting session memory...")
        summary = "[System Compaction: User is planning a 3-week Munich EV loop to Austria/Italy]"
        self.history = [{"role": "system", "content": summary}] + self.history[-2:]

    def process_driving_log(self, hours: float) -> Dict:
        """Enforces driving guardrails and triggers Human-In-The-Loop hooks if exceeded."""
        if hours > 4.0:
            logger.warning("Driving limit alert triggered!")
            return {
                "status": "PAUSED_HITL",
                "message": f"Daily driving limit exceeded ({hours} hours). Human approval required to proceed."
            }
        return {"status": "SUCCESS", "message": "Route is within safe parameters."}
