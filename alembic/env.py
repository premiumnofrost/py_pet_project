import os
import asyncio

from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from alembic.operations.ops import DropTableOp

from sqlalchemy.ext.asyncio import async_engine_from_config

from app.db.database import Base
from app.core.config import settings
import app.models

from pathlib import Path

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata



def assert_metadata_not_empty():
    if not Base.metadata.tables:
        raise Exception("❌ Base.metadata пустой — модели не загружены")


def block_drop_tables(context, revision, directives):
    script = directives[0]

    for op in script.upgrade_ops.ops:
        if isinstance(op, DropTableOp):
            raise Exception("❌ DROP TABLE запрещён. Сделай вручную.")

    return directives


async def run_migrations_online():

    assert_metadata_not_empty()

    
    config_section = config.get_section(config.config_ini_section, {})

    connectable = async_engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # 4. Запускаем миграции
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # 5. Очищаем соединение
    await connectable.dispose()

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        process_revision_directives=block_drop_tables,
    )

    with context.begin_transaction():
        context.run_migrations()



if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())