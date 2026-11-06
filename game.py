from gamer import Supervisor
from gamer import Participant
import sys
import time
import os
import glob

# List of model names - easy to modify here
MODEL_NAMES = ["Doubao-1.5-pro-32k", "Doubao-1.5-pro-32k", "Doubao-1.5-pro-32k"]

# List of decode files - easy to modify here
DECODE_FILES = ["decode1.txt", "decode2.txt", "decode3.txt"]

SUPERVISOR_MODEL_NAME = "deepseek-reasoner"
SUPERVISOR_DECODE_FILE = "total_decode.txt"

SUPERVISOR = None
PARTICIPANTS = []

def init():
    global SUPERVISOR, PARTICIPANTS

    SUPERVISOR = Supervisor(SUPERVISOR_DECODE_FILE, SUPERVISOR_MODEL_NAME)
    
    # Create participants with different decode files and models from the lists
    # zip() pairs them together: (decode_file, model)
    PARTICIPANTS = [Participant(decode_file, model) for decode_file, model in zip(DECODE_FILES, MODEL_NAMES)]


def game():
    global SUPERVISOR, PARTICIPANTS

    Message = "Game start"

    while not Message.endswith("爱你老妈，明天见。还有你，老爸。"):
        Message = SUPERVISOR.Boardcast(PARTICIPANTS, SUPERVISOR.Chat(Message))

    
if __name__ == "__main__":
    T = 5
    # Find the next available log file number
    record_dir = "/home/truthg/werewolf/record"
    existing_logs = glob.glob(os.path.join(record_dir, "game_log_*.txt"))
    if existing_logs:
        # Extract numbers from existing log files and find the max
        numbers = []
        for log_file in existing_logs:
            try:
                # Extract number from filename like "game_log_1.txt"
                base_name = os.path.basename(log_file)
                number = int(base_name.replace("game_log_", "").replace(".txt", ""))
                numbers.append(number)
            except ValueError:
                continue
        next_number = max(numbers) + 1 if numbers else 1
    else:
        next_number = 1
    
    log_path = os.path.join(record_dir, f"game_log_{next_number}.txt")
    with open(log_path, "a", encoding="utf-8") as log:
        original_stdout = sys.stdout
        sys.stdout = log
        try:
            for i in range(T):
                start_time = time.perf_counter()
                init()
                elapsed = time.perf_counter() - start_time
                print(f"Initialization time: {elapsed:.3f} seconds")
                start_time = time.perf_counter()
                game()
                elapsed = time.perf_counter() - start_time
                print(f"Game time: {elapsed:.3f} seconds")

                print("-" * 40)
        