import glob
import os
import sys
from importlib import util
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import get_app_settings
from app.db.sqlalchemy_models import Base

SETTINGS = get_app_settings()
DATABASE_URL = SETTINGS.database_url

config = context.config

fileConfig(config.config_file_name)  # type: ignore

target_pattern = "/FastAPI_SQL_builder_based/app/db/sqlalchemy_models/*.py"

for module in glob.glob(target_pattern, recursive=True):
    if os.path.basename(module) not in {"__init__.py", "base.py"}:
        spec = util.spec_from_file_location("module.name", module)
        imported_module = util.module_from_spec(spec)
        sys.modules["module.name"] = imported_module
        spec.loader.exec_module(imported_module)

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", str(DATABASE_URL))


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
