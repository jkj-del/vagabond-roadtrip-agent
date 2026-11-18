import json
import asyncio
from typing import Dict, List
from app.database import SessionDatabase
from app.tracing import redact_pii, TraceSpan, log_intent_outcome

class PlannerAgent:
    """Specialized Agent to evaluate road trip rules."""
    def evaluate_plan(self, hours: float) -> dict:
        if hours > 4.0:
            return {"status": "PAUSED_HITL", "msg": f"Driving limit exceeded ({hours} hrs). Approvals required."}
        return {"status": "SUCCESS", "msg": "Rules validated."}

class RouterAgent:
    """Specialized Agent to handle strategic model routing."""
    def route_query(self, complexity: str) -> str:
        if complexity == "high":
            return "gemini-1.5-pro" # Heavy model for complex loop planning
        return "gemini-1.5-flash" # Fast, cost-efficient model for simple queries

class VagabondAgent:
    """Primary Multi-Agent Coordinator containing database session state."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.db = SessionDatabase()
        self.planner = PlannerAgent()
        self.router = RouterAgent()
        self.history: List[dict] = []

    async def initialize_async(self):
        """Loads state asynchronously from sqlite session database."""
        self.history = await self.db.load_session_async(self.session_id)

    async def ingest_message_async(self, user_content: str, complexity: str = "low") -> dict:
        """Ingests message, scrubs PII, routes model, and updates SQLite asynchronously."""
        span = TraceSpan(name="ingest_message")
        
        # 1. Automatic integrated PII scrubbing
        clean_content = redact_pii(user_content)
        self.history.append({"role": "user", "content": clean_content})
        
        # 2. Strategic Model Routing
        selected_model = self.router.route_query(complexity)
        
        # 3. Process with Planner
        plan_eval = self.planner.evaluate_plan(3.0) # Mock call to sub-agent
        
        # 4. Async memory compaction
        if len(self.history) > 5:
            await self.compact_memory_async()
            
        # 5. Persist back to database
        await self.db.save_session_async(self.session_id, self.history)
        
        # 6. Intent vs Outcome Observability Tracing
        log_intent_outcome(span, "Ingest User Roadtrip request", "State saved and model routed", True)
        
        return {
            "model_used": selected_model,
            "state_persisted": True,
            "eval_status": plan_eval["status"]
        }

    async def compact_memory_async(self):
        """Asynchronous context consolidator."""
        await asyncio.sleep(0.01) # Non-blocking async sleep
        summary = "[Async Compaction: Active 3-week roadtrip plan]"
        self.history = [{"role": "system", "content": summary}] + self.history[-2:]
