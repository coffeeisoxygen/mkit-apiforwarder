import json
from pathlib import Path

from src.config import Settings

pathtodevenv = Path(__file__).resolve().parent.parent / ".env.dev"
settings = Settings(_env_file=pathtodevenv, _env_file_encoding="utf-8")  # type: ignore


def main():
    print(
        json.dumps({
            "app_env": settings.app_env,
            "app_debug": settings.app_debug,
            "app_name": settings.app_name,
        })
    )


if __name__ == "__main__":
    main()
