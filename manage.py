import os
import unittest

from flask.cli import FlaskGroup
from flask_sqlalchemy import SQLAlchemy

from app.main import create_app, db
from app import blueprint

app = create_app('dev')
app.register_blueprint(blueprint)
app.app_context().push()

cli = FlaskGroup(app)

@cli.command('run')
def run():
    app.run()

@cli.command('test')
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()