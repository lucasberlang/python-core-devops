from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    from app.__main__ import main

    print("Running locally...")
    main()


if __name__ == "__main__":
    main()
