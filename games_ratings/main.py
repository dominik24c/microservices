from dotenv import load_dotenv
from flask import Flask

from app import create_app


def main() -> Flask:
    load_dotenv()
    return create_app()


app = main()
