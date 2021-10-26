import logging
import os
from typing import Tuple

import click

from stactools.gpw import cog, stac

logger = logging.getLogger(__name__)


def create_gpw_command(cli: click.Group) -> click.Command:
    """Creates the gpw command line utility."""
    @cli.group(
        "gpw",
        short_help="Commands for working with GPW data",
    )
    def gpw() -> None:
        pass

    @gpw.command(
        "create-collection",
        short_help="Creates a STAC collection from GPW metadata",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection json",
    )
    def create_collection_command(destination: str) -> None:
        """Creates a STAC Collection from gpw metadata

        Args:
            destination (str): Directory used to store the collection json
        Returns:
            Callable
        """
        stac.create_collection(destination)

    @gpw.command(
        "create-cog",
        short_help="Transform Geotiff to Cloud-Optimized Geotiff.",
    )
    @click.option("-d",
                  "--destination",
                  required=True,
                  help="The output directory for the COG")
    @click.option("-s",
                  "--source",
                  required=True,
                  help="Path to an input GeoTiff")
    @click.option(
        "-t",
        "--tile",
        help="Tile the tiff into many smaller files.",
        is_flag=True,
        default=False,
    )
    def create_cog_command(destination: str, source: str, tile: bool) -> None:
        """Generate a COG from a GeoTiff. The COG will be saved in the destination
        with `_cog.tif` appended to the name.

        Args:
            destination (str): Local directory to save output COGs
            source (str): An input GPW GeoTiff
            tile (bool, optional): Tile the tiff into many smaller files
        """
        if not os.path.isdir(destination):
            raise IOError(f'Destination folder "{destination}" not found')

        cog.create_cog(source, destination, tile=tile)

    @gpw.command(
        "create-item",
        short_help="Create a STAC item",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC json",
    )
    @click.option(
        "-c",
        "--cogs",
        nargs=4,
        required=True,
        help="""
        \b
        COG hrefs for:
            Population Count,
            UN WPP-Adjusted Population Count,
            Population Density,
            UN WPP-Adjusted Population Density
        """,
    )
    def create_item_command(destination: str, cogs: Tuple[str]) -> None:
        """Generate a STAC item using the metadata, with an asset url as provided.

        Args:
            destination (str): Local directory to save the STAC Item json
            cog (str): location of a COG asset for the item
        """

        (pop_count, pop_count_adj, pop_density,
         pop_density_adj) = (i for i in cogs)

        item = stac.create_item(pop_count, pop_count_adj, pop_density,
                                pop_density_adj)

        output_path = os.path.join(destination, item.id + ".json")

        item.set_self_href(output_path)
        item.make_asset_hrefs_relative()
        item.save_object()
        item.validate()

    return gpw
