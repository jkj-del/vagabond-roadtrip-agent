import re
import json
import uuid
import logging

class TraceSpan:
    """Distributed tracing span class to monitor model pipelines."""
    def __init__(self, name: str, parent_span_id: str = None):
        self.name = name
        self.trace_id = str(uuid.uuid4())
        self.span_id = str(uuid.uuid4())
        self.parent_span_id = parent_span_id

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "span_name": self.name
        }

def redact_pii(text: str) -> str:
    """Filters sensitive PII like emails out of user-provided prompt streams."""
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.sub(email_pattern, "[REDACTED_EMAIL]", text)

def log_intent_outcome(span: TraceSpan, intent: str, outcome: str, success: bool):
    """Outputs structured intent vs outcome logs with distributed trace IDs."""
    log_record = {
        "trace_info": span.to_dict(),
        "intent": intent,
        "outcome": outcome,
        "status": "SUCCESS" if success else "FAILED"
    }
    print(f"[METRIC_LOG] {json.dumps(log_record)}")
