"""
    `bckptlk` - Backup Toolkit
    
    Author: @kirillzhosul
"""

from config import read_config
from runner import run_strategy

if __name__ == "__main__":
    config = read_config()

    for target in config.targets:
        if config.verbose:
            print(f"Backuping target {target.id} with strategy: {target.strategy}")
        run_strategy(target, config)
        if config.verbose:
            print("OK!")
