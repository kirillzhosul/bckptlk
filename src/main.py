from config import read_config
from strategies import run_strategy

config = read_config()
for target in config.targets:
    if config.verbose:
        print(f"Backuping target {target.id} with strategy: {target.strategy}")
    run_strategy(target, config)
    if config.verbose:
        print("OK!")
