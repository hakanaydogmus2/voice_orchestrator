import json
import os
from datetime import datetime
from config import settings
from pydantic import BaseModel


class LogEntry(BaseModel):
    ts: str
    turn_id: int
    user_text: str
    assistant_text: str


class JSONLogger:
    def __init__(self, log_dir=settings.log_dir):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "conversation.jsonl")
        self.turn_id = 0

    def log_turn(self, user_text: str, assistant_text: str):
        
        self.turn_id += 1
        entry = LogEntry(
            ts=datetime.utcnow().isoformat() + "Z",
            turn_id=self.turn_id,
            user_text=user_text,
            assistant_text=assistant_text,
        )
        # JSON satırı olarak kaydet
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry.model_dump_json(exclude_unset=True) + "\n")
