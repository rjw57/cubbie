"""
CLI tool for cubbie ui.

"""
from flask.ext.script import Manager

from cubbieui import app

def create_app(config=None):
    if config is not None:
        app.config.from_pyfile(config)
    return app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)

def main():
    """Utility entry point."""
    manager.run()

if __name__ == '__main__':
    main()

