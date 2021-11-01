import logging
import os
from typing import List, Tuple, Union

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
    @click.option(
        "-e",
        "--expanded_bbox",
        nargs=4,
        required=False,
        help="Expand retiled bbox to: xmin ymin xmax ymax",
    )
    def create_cog_command(
        destination: str,
        source: str,
        tile: bool,
        expanded_bbox: Tuple[Union[float, int, str]],
    ) -> None:
        """Generate a COG from a GeoTiff. The COG will be saved in the destination
        with `_cog.tif` appended to the name.

        Args:
            destination (str): Local directory to save output COGs
            source (str, optional): An input GPW GeoTiff
            tile (bool): Tile the tiff into many smaller files
        """
        if not os.path.isdir(destination):
            raise IOError(f'Destination folder "{destination}" not found')

        expanded_bbox_list: List[Union[float, int, str]] = list(expanded_bbox)
        cog.create_cog(source,
                       destination,
                       tile=tile,
                       expanded_bbox=expanded_bbox_list)

    @gpw.command(
        "create-pop-collection",
        short_help="Creates a STAC collection from GPW population metadata",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection json",
    )
    def create_pop_collection_command(destination: str) -> None:
        """Creates a STAC Collection from GPW population metadata

        Args:
            destination (str): Directory used to store the collection json
        Returns:
            Callable
        """
        stac.create_pop_collection(destination)

    @gpw.command(
        "create-anc-collection",
        short_help="Creates a STAC collection from GPW ancillary metadata",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection json",
    )
    def create_anc_collection_command(destination: str) -> None:
        """Creates a STAC Collection from GPW ancillary metadata

        Args:
            destination (str): Directory used to store the collection json
        Returns:
            Callable
        """
        stac.create_anc_collection(destination)

    @gpw.command(
        "create-pop-item",
        short_help="Create a STAC item for population datasets",
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
    def create_pop_item_command(destination: str, cogs: Tuple[str]) -> None:
        """Generate a population STAC item using the metadata.

        Args:
            destination (str): Local directory to save the STAC Item json
            cog (str): location of COG assets for the item
        """

        (pop_count, pop_count_adj, pop_density,
         pop_density_adj) = (i for i in cogs)

        item = stac.create_pop_item(pop_count, pop_count_adj, pop_density,
                                    pop_density_adj)

        output_path = os.path.join(destination, item.id + ".json")

        item.set_self_href(output_path)
        item.make_asset_hrefs_relative()
        item.save_object()
        item.validate()

    @gpw.command(
        "create-anc-item",
        short_help="Create a STAC item for ancillary datasets",
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
        nargs=12,
        required=True,
        help="""
        \b
        COG hrefs for:
            Data Quality Indicators - Data Context,
            Data Quality Indicators - Mean Administrative Unit Area,
            Data Quality Indicators - Water Mask,
            Basic Demographic Characteristics - Total Population Count,
            Basic Demographic Characteristics - Total Population Density,
            Basic Demographic Characteristics - Female Count,
            Basic Demographic Characteristics - Female Density,
            Basic Demographic Characteristics - Male Count,
            Basic Demographic Characteristics - Male Density,
            Land Area,
            Water Area,
            National Identifier Grid
        """,
    )
    def create_anc_item_command(destination: str, cogs: Tuple[str]) -> None:
        """Generate a population STAC item using the metadata.

        Args:
            destination (str): Local directory to save the STAC Item json
            cog (str): location of COG assets for the item
        """

        (
            dqi_context,
            dqi_admin,
            dqi_watermask,
            bdc_bt_count,
            bdc_bt_density,
            bdc_ft_count,
            bdc_ft_density,
            bdc_mt_count,
            bdc_mt_density,
            land_area,
            water_area,
            nat_id_grid,
        ) = (i for i in cogs)

        item = stac.create_anc_item(
            dqi_context,
            dqi_admin,
            dqi_watermask,
            bdc_bt_count,
            bdc_bt_density,
            bdc_ft_count,
            bdc_ft_density,
            bdc_mt_count,
            bdc_mt_density,
            land_area,
            water_area,
            nat_id_grid,
        )

        output_path = os.path.join(destination, item.id + ".json")

        item.set_self_href(output_path)
        item.make_asset_hrefs_relative()
        item.save_object()
        item.validate()

    return gpw
