import os

from config import read_config
from strategies import run_strategy

for target in read_config().targets:
    print(f"Backuping target {target.id} with strategy: {target.strategy}")
    run_strategy(target)
    print("OK!")
