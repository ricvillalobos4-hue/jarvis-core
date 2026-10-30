
import json
from pathlib import Path
from datetime import datetime, timezone


class JarvisMemory:
    def __init__(self):
        root = Path(__file__).resolve().parent.parent
        self.memory_dir = root / "data"
        self.memory_file = self.memory_dir / "memory.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)

        if not self.memory_file.exists():
            self._save([])

        self.memories = self._load()

    def _load(self):
        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, data):
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def remember(self, information):
        if not isinstance(information, str) or not information.strip():
            return False

        memory = {
            "information": information.strip(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.memories.append(memory)
        self._save(self.memories)
        return True

    def recall(self):
        self.memories = self._load()
        return self.memories

    def forget_all(self):
        self.memories = []
        self._save(self.memories)
        return True
