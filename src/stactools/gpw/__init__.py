import stactools.core
from stactools.cli import Registry

from stactools.gpw import commands
from stactools.gpw.stac import create_pop_collection, create_pop_item

__all__ = ["create_pop_collection", "create_pop_item"]

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    registry.register_subcommand(commands.create_gpw_command)


__version__ = "0.2.0"
