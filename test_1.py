from game import record_dir
from gamer import Supervisor
from gamer import Participant
import time
import sys
import os


T = 5
record_dir = "/home/truthg/werewolf/record"
existing_logs = glob.glob(os.path.join(record_dir, "test_log_*.txt"))
if existing_logs:
    numbers = []
    for log_file in existing_logs:
        try:
            number = int(log_file.replace("test_log_","").replace(".txt",""))
            numbers.append(number)
        except ValueError:
            continue
    next_number = max(numbers) + 1 if numbers else 1
else:
    next_number = 1
log_path = os.path.join(record_dir, f"test_log_{next_number}.txt")


with open(log_path, "a", encoding="utf-8") as log:
    original_stdout = sys.stdout
    sys.stdout = log
    try:
        for i in range(T):
            general_start_time = time.perf_counter()

            print(f"this is the {i}th loop")
            st = time.perf_counter()
            supervisor = Supervisor(decode_file = "total_decode.txt", model = "deepseek-reasoner")
            et = time.perf_counter()
            print(f"the deepseek-reasoner uses {(et - st):.3f}s to finish initalization")
            
            st = time.perf_counter()
            participant_1 = Participant(decode_file = "decode1.txt", model = "Doubao-1.5-pro-32k")
            et = time.perf_counter()
            print(f"the Doubao-1.5-pro-32k uses {(et - st):.3f}s to finish initalization")

            st = time.perf_counter()
            participant_2 = Participant(decode_file = "decode2.txt", model = "deepseek-chat")
            et = time.perf_counter()
            print(f"deepseek-chat uses {(et - st):.3f}s to finish initalization")

            st = time.perf_counter()
            participant_3 = Participant(decode_file = "decode3.txt", model = "qwen-mt-turbo")
            et = time.perf_counter()
            print(f"qwen-mt-turbo uses {(et - st):.3f}s to finish initalization")

            
            #test_message = "so transfer 'hello, you are the werewolf' to 'one' and 'hello, you are seer' to 'two' and 'hello, you are villeger' to 'three' in your following response, give me the result in three different lines."
            test_message = "so transfer 'hello, you are the werewolf' to 'one'"
            test_message += "just output the trasferred sentences, no other words."
            test_message += "Check you result three times before sending me the final result."
            
            start_time = time.perf_counter()
            test_response = supervisor.Chat(test_message)
            elapsed = time.perf_counter() - start_time
            print(f"it takes {elapsed:.3f}s for the surpervisor to deal with the rule and test_message")

            test_boardcast_response = supervisor.Boardcast([participant_1, participant_2, participant_3], test_response)

            print("The test_response is:")
            print(test_response)
            print("The test_boardcast_response is:")
            print(test_boardcast_response)
            
            general_elapsed = time.perf_counter() - general_start_time

            print(f"The time for the test_example perf_counteto run once is {general_elapsed}s")
            
            print("-" * 40)
    finally:
        sys.stdout = original_stdout