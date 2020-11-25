from source.easysystems import create_app
import os

application = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG')
    application.run(debug=debug)

