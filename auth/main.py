from dotenv import load_dotenv

from app import create_app

def main() -> None:
    load_dotenv()
    app = create_app()
    app.run('0.0.0.0', 7001, debug=True)

main()