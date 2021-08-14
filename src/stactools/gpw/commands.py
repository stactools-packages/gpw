import click
import logging
import os

from stactools.gpw import stac
from stactools.gpw import cog

logger = logging.getLogger(__name__)


def create_gpw_command(cli):
    """Creates the gpw command line utility."""
    @cli.group(
        "gpw",
        short_help="Commands for working with GPW data",
    )
    def gpw():
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
    def create_collection_command(destination: str):
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
    def create_cog_command(destination: str, source: str):
        """Generate a COG from a GeoTiff. The COG will be saved in the destination
        with `_cog.tif` appended to the name.

        Args:
            destination (str): Local directory to save output COGs
            source (str): An input GPW GeoTiff
        """
        if not os.path.isdir(destination):
            raise IOError(f'Destination folder "{destination}" not found')

        output_path = os.path.join(destination,
                                   os.path.basename(source)[:-4] + "_cog.tif")

        cog.create_cog(source, output_path)

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
    @click.option("-c",
                  "--cog",
                  nargs=5,
                  required=True,
                  help="COG hrefs for arc30s, arc2M30s, arc15m, arc30m, arc60m"
                  )
    def create_item_command(destination: str, cog: str):
        """Generate a STAC item using the metadata, with an asset url as provided.

        Args:
            destination (str): Local directory to save the STAC Item json
            cog (str): location of a COG asset for the item
        """

        arc30s, arc2M30s, arc15m, arc30m, arc60m = cog

        output_path = os.path.join(destination,
                                   os.path.basename(arc30s)[:-4] + ".json")

        stac.create_item(output_path, arc30s, arc2M30s, arc15m, arc30m, arc60m)

    return gpw
