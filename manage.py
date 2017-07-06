import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from raven.contrib.flask import Sentry

from app import create_app, db
from app.models import User, Task

if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
sentry = Sentry(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Task=Task)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
