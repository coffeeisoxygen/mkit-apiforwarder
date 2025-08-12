import json

from src.config import get_settings

settings = get_settings()


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
