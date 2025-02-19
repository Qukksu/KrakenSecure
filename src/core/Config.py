import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    def __init__(self, env_file='.env'):
        self.env_file = env_file
        self._create_env_file_if_not_exists()
        load_dotenv(self.env_file)
        # for key, value in os.environ.items():
        #     setattr(self, key, value) # WIP

    def _create_env_file_if_not_exists(self):
        if not Path(self.env_file).exists():
            with open(self.env_file, 'w') as f:
                f.write("# Configuration file\n")
            self.set_default()
                # f.write("KEY=value\n")

    def get(self, key, default=None):
        return os.getenv(key, default)

    def set(self, key, value):
        os.environ[key] = value
        self._update_env_file(key, value)

    def set_default(self):
        self.set("SQLITE_PATH", "")
        self.set("LOCALIZATION_FILE", "")

    def _update_env_file(self, key, value):
        with open(self.env_file, 'r') as f:
            lines = f.readlines()

        with open(self.env_file, 'w') as f:
            for line in lines:
                if line.startswith(f"{key}="):
                    continue
                f.write(line)
            f.write(f"{key}={value}\n")


# Пример использования
config = Config()

