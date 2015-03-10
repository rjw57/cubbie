"""
Command-line manager utility for cubbie.

"""
import logging

from flask import current_app
from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager, Command
from mixer.backend.flask import mixer

from cubbie.webapp import create_app
from cubbie.model import db
from cubbie.model import User, Production, Performance, SalesDatum, Capability
from cubbie.fixture import (
    create_user_fixtures, create_production_fixtures,
    create_performance_fixtures, create_sales_fixtures, create_capability_fixtures
)

def create_manager_app(config=None):
    app = create_app()
    if config is not None:
        app.config.from_pyfile(config)
    migrate = Migrate(app, db)

    return app

class GenFakeData(Command):
    "generates fake data in the database"

    def run(self):
        if not current_app.debug:
            logging.error(
                'genfake command is only available in deebug modfe. '
                'Ensure that DEBUG is True in app config.'
            )
            return

        db.create_all()
        mixer.init_app(current_app)
        create_user_fixtures(10)
        create_production_fixtures(5)
        create_capability_fixtures(10)
        create_performance_fixtures(25)
        create_sales_fixtures(200)

manager = Manager(create_manager_app)
manager.add_command('db', MigrateCommand)
manager.add_command('genfake', GenFakeData)
manager.add_option('-c', '--config', dest='config', required=False)

def main():
    """Utility entry point."""
    manager.run()

if __name__ == '__main__':
    main()

