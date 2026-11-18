import re
import json
import uuid
import logging

# 1. Setup structured logger utilizing standard Python logging instead of print
logger = logging.getLogger("vagabond_observability")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class TraceSpan:
    """Distributed tracing span mimicking standard OpenTelemetry span attributes."""
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
    """Filters sensitive PII (Emails, IP addresses, and Phone Numbers) from user prompts."""
    # Email pattern
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, "[REDACTED_EMAIL]", text)
    
    # IPv4 address pattern
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    text = re.sub(ip_pattern, "[REDACTED_IP]", text)
    
    # Standard phone number pattern (international or simple format)
    phone_pattern = r'\+?\d{1,4}[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    text = re.sub(phone_pattern, "[REDACTED_PHONE]", text)
    
    return text

def log_intent(span: TraceSpan, intent: str):
    """Logs the intent PRIOR to execution."""
    log_record = {
        "event": "INTENT_START",
        "trace_info": span.to_dict(),
        "intent": intent
    }
    logger.info(f"[METRIC_LOG] {json.dumps(log_record)}")

def log_outcome(span: TraceSpan, intent: str, outcome: str, success: bool):
    """Logs the outcome POST execution."""
    log_record = {
        "event": "OUTCOME_COMPLETE",
        "trace_info": span.to_dict(),
        "intent": intent,
        "outcome": outcome,
        "status": "SUCCESS" if success else "FAILED"
    }
    logger.info(f"[METRIC_LOG] {json.dumps(log_record)}")
