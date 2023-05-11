import subprocess
import time

while True:
    subprocess.run(["python", "../orders_generator.py"])
    time.sleep(3600)  # 60min