"""Database migration tasks using Alembic."""

import os

from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task

# Fixed name for the throwaway migration database.
_TEMP_DB = "xarizmi_migrate_temp"


def _get_database_url() -> str:
    """Return DB URL from DATABASE_URL env var, falling back to alembic.ini."""
    if "DATABASE_URL" in os.environ:
        return os.environ["DATABASE_URL"]
    import configparser

    cfg = configparser.RawConfigParser()
    cfg.read("alembic.ini")
    url = cfg.get("alembic", "sqlalchemy.url", fallback=None)
    if not url:
        raise RuntimeError(
            "No database URL found. Set DATABASE_URL or configure "
            "sqlalchemy.url in alembic.ini."
        )
    return url


def _pg_env(url: str) -> dict[str, str]:
    """Extract PG* environment variables from a SQLAlchemy URL.

    createdb / dropdb read connection settings from these standard
    PostgreSQL environment variables.
    """
    from sqlalchemy.engine import make_url

    u = make_url(url)
    return {
        "PGHOST": u.host or "localhost",
        "PGPORT": str(u.port or 5432),
        "PGUSER": u.username or "",
        "PGPASSWORD": u.password or "",
    }


@task(
    help={
        "message": (
            "Short description of the migration, e.g. 'add user table'. "
            "Used as the migration file name suffix."
        ),
    }
)
def generate_migration(c: Context, message: str) -> None:
    """Generate an Alembic autogenerate migration.

    Prerequisites
    -------------
    PostgreSQL must be running locally and the xarizmi_migrate_temp table
    should exist with postgres user as owner and password 1

    Example
    -------
        invoke database.generate-migration --message "add portfolio table"
    """
    original_url = _get_database_url()

    print(original_url)

    print("→ Applying all existing migrations...")
    c.run("alembic upgrade head", env={"DATABASE_URL": original_url})

    print(f"→ Generating migration: '{message}'")
    c.run(
        f"alembic revision --autogenerate -m '{message}'",
        env={"DATABASE_URL": original_url},
    )

    print(
        "✅ Done. Review the new file in "
        "xarizmi/db/alembic/versions/ before committing."
    )


@task(help={"revision": "Target revision or 'head' (default: head)"})
def upgrade(c: Context, revision: str = "head") -> None:
    """Upgrade the database to a revision (default: head)."""
    c.run(f"alembic upgrade {revision}", pty=True)


@task(help={"revision": "Revision or relative step, e.g. '-1' (default: -1)"})
def downgrade(c: Context, revision: str = "-1") -> None:
    """Downgrade the database by one revision or to a specific revision."""
    c.run(f"alembic downgrade {revision}", pty=True)


@task()
def history(c: Context) -> None:
    """Show the full migration history."""
    c.run("alembic history --verbose", pty=True)


@task()
def current(c: Context) -> None:
    """Show the current migration revision of the database."""
    c.run("alembic current --verbose", pty=True)


ns_database = Collection("database")
ns_database.add_task(generate_migration)
ns_database.add_task(upgrade)
ns_database.add_task(downgrade)
ns_database.add_task(history)
ns_database.add_task(current)

__all__ = ["ns_database"]
