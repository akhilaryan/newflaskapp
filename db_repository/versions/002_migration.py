from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('uid', Integer, primary_key=True, nullable=False),
    Column('firstname', String),
    Column('lastname', String),
    Column('email', String),
    Column('pwdhash', String),
)

post = Table('post', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('users_id', Integer),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstname', String(length=100)),
    Column('lastname', String(length=100)),
    Column('email', String(length=120)),
    Column('pwdhash', String(length=54)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    pre_meta.tables['post'].drop()
    post_meta.tables['posts'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    pre_meta.tables['post'].create()
    post_meta.tables['posts'].drop()
    post_meta.tables['users'].drop()
