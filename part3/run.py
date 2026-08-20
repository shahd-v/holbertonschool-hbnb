import os

from dotenv import find_dotenv, load_dotenv

from app import create_app

# Searchs for .env if it's in current dir or up
load_dotenv(find_dotenv())

app = create_app()

if __name__ == '__main__':

    # if APP_DEBUG in .env or defaults to true
    debug_mode = os.environ.get('APP_DEBUG', 'False').lower() == 'true'

    app.run(debug=True)
