from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from alembic.operations.ops import DropTableOp

from app.db.database import Base
import app.models


config = context.config

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


def run_migrations_online():
    assert_metadata_not_empty()

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
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
    run_migrations_online()