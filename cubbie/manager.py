"""
Command-line manager utility for cubbie.

"""
from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager

from cubbie.webapp import create_app
from cubbie.model import db

def create_manager_app(config=None):
    app = create_app()
    if config is not None:
        app.config.from_pyfile(config)
    migrate = Migrate(app, db)

    return app

manager = Manager(create_manager_app)
manager.add_command('db', MigrateCommand)
manager.add_option('-c', '--config', dest='config', required=False)

def main():
    """Utility entry point."""
    manager.run()

if __name__ == '__main__':
    main()

