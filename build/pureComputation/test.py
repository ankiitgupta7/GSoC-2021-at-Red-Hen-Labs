import datetime
import os

from pathlib import Path

now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

Path("./data").mkdir(parents=True, exist_ok=True)

Path("./data/"+str(now)).mkdir(parents=True, exist_ok=True)

print(str(now))