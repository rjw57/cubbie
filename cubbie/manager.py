"""
Command-line manager utility for cubbie.

"""
import logging

from flask import current_app
from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager, Command

from cubbie.webapp import create_app
from cubbie.model import db
from cubbie.model import User, Production, Performance, SalesDatum, Capability

def create_manager_app(config=None):
    app = create_app()
    if config is not None:
        app.config.from_pyfile(config)
    migrate = Migrate(app, db)

    return app

class GenFakeData(Command):
    "generates fake data in the database"

    def run(self):
        if current_app.config.get('DEVELOPMENT') is None:
            logging.error(
                'genfake command is only available in development. '
                'Ensure that DEVELOPMENT is True in app config.'
            )
            return

        db.create_all()

        from mixer.backend.flask import mixer
        from datetime import datetime, timedelta
        from random import seed, randint, choice
        from faker import Faker

        mixer.init_app(current_app)
        fake = Faker()

        mixer.cycle(10).blend(User, displayname=fake.name)
        mixer.cycle(5).blend(Production, name=fake.sentence, slug=fake.slug)

        def sa(c):
            return datetime.utcnow() + timedelta(minutes=10+5*c)

        def ea(c):
            return datetime.utcnow() + timedelta(minutes=20+15*c)

        mixer.cycle(50).blend(Performance,
            starts_at=mixer.sequence(sa),
            ends_at=mixer.sequence(ea),
            production=mixer.SELECT,
            is_cancelled=mixer.RANDOM,
            is_deleted=mixer.RANDOM,
        )

        def ma(c):
            return datetime.utcnow() + timedelta(days=randint(1,100))
        def sold(c):
            seed(c)
            return randint(0, 65)
        def avail(c):
            seed(c)
            s = randint(0, 65)
            return s + randint(0, 30)

        mixer.cycle(1000).blend(SalesDatum,
            measured_at=mixer.sequence(ma),
            performance=mixer.SELECT,
            is_valid=mixer.RANDOM,
            sold=mixer.sequence(sold),
            available=mixer.sequence(avail),
        )

        mixer.cycle(100).blend(Capability,
            user=mixer.SELECT,
            production=mixer.SELECT,
        )

manager = Manager(create_manager_app)
manager.add_command('db', MigrateCommand)
manager.add_command('genfake', GenFakeData)
manager.add_option('-c', '--config', dest='config', required=False)

def main():
    """Utility entry point."""
    manager.run()

if __name__ == '__main__':
    main()

