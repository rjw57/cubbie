"""
Command-line manager utility for cubbie.
"""

from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager

from cubbie.webapp import create_app, db

app = create_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

def main():
    """Utility entry point."""
    manager.run()

if __name__ == '__main__':
    main()

