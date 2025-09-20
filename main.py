
from src.orchestrator import Orchestrator

if __name__ == "__main__":
    print("space to start/stop listening, enter to exit")
    orchestrator = Orchestrator()
    orchestrator.start()