from source.easysystems import create_app
import os

app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG')
    app.run(debug=debug)

