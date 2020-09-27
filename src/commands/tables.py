import sys

import click
from sqlalchemy.exc import IntegrityError
from flask import Blueprint

from utils import db
from models import Role, Status, Criticality

tables = Blueprint('tables', __name__)


@tables.cli.command('add-seed-data')
def add_seed_data():
    """Initializes the table with values provided in the initial values attribute"""

    tables_to_init = (Role, Status, Criticality,)

    for table in tables_to_init:

        if not hasattr(table, 'initial_values'):
            raise click.UsageError(f'Table: {table} has no attribute initial_values, cannot proceed')

        init_values = getattr(table, 'initial_values')

        if not isinstance(init_values, (list, tuple, set)):
            raise click.UsageError(f'{table.__name__}.initial_values attribute can only be of type list/tuple/set')

        for value in init_values:
            row = table(value=value)
            try:
                db.session.add(row)
                db.session.commit()
                click.echo(message=f'Added Value: {value} to Table: {table.__tablename__}')
            except IntegrityError:
                db.session.rollback()
                click.echo(message=f'Cannot add Value: {value} to Table: {table.__tablename__}, Already Exists')
                continue
    sys.exit(0)


@tables.cli.command('drop-all')
def drop_all():
    """Drops all table"""

    db.drop_all()
