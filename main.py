from app import create_app
from app.helpers import branding


app = create_app()


if __name__ == "__main__":
    branding.print_server_start_header()
    app.run()