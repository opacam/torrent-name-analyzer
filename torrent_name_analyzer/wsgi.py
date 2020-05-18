import os
from torrent_name_analyzer.app import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

if __name__ == '__main__':
    app.run()
