import logging
import os
import re
from datetime import datetime
from typing import Optional

import pystac
import pytz
import rasterio
import shapely
from dateutil.relativedelta import relativedelta
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from stactools.core.io import ReadHrefModifier

from stactools.gpw.assets import (
    ITEM_ASSETS,
    POP_COUNT_ADJ_KEY,
    POP_COUNT_KEY,
    POP_DENSITY_ADJ_KEY,
    POP_DENSITY_KEY,
)
from stactools.gpw.constants import (
    DESCRIPTION,
    GPW_BOUNDING_BOX,
    GPW_END_YEAR,
    GPW_EPSG,
    GPW_ID,
    GPW_PROVIDER,
    GPW_START_YEAR,
    GPW_TITLE,
    LICENSE,
    LICENSE_LINK,
)

logger = logging.getLogger(__name__)


def create_item(
    pop_count: str,
    pop_count_adj: str,
    pop_density: str,
    pop_density_adj: str,
    cog_href_modifier: Optional[ReadHrefModifier] = None,
) -> pystac.Item:
    """Creates a STAC item for Gridded Population of the World,
    Version 4 (GPWv4): Population Count dataset.

    Args:
        pop_count (str): Path to tiled population count COG
        pop_count_adj (str): Path to tiled adjusted population count COG
        pop_density (str): Path to tiled population density COG
        pop_density_adj (str): Path to adjusted tiled population density COG

    Returns:
        pystac.Item: STAC Item object.
    """

    # construct an item id like: gpw_v4_rev11_2005_30_sec_1_1
    split_basename = os.path.basename(pop_count).split("_")
    item_id = "_".join([*split_basename[0:2], *split_basename[4:10]])

    match = re.search(r"\d{4}", item_id)
    assert match
    year = match.group()

    utc = pytz.utc

    dataset_datetime = utc.localize(datetime.strptime(year, "%Y"))

    end_datetime = dataset_datetime + relativedelta(years=5)

    start_datetime = dataset_datetime
    end_datetime = end_datetime

    polygon = shapely.geometry.box(*GPW_BOUNDING_BOX, ccw=True)
    coordinates = [list(i) for i in list(polygon.exterior.coords)]

    geometry = {"type": "Polygon", "coordinates": [coordinates]}

    properties = {
        "description": DESCRIPTION,
    }

    # Create item
    item = pystac.Item(
        id=item_id,
        geometry=geometry,
        bbox=GPW_BOUNDING_BOX,
        datetime=dataset_datetime,
        properties=properties,
    )

    item.common_metadata.start_datetime = start_datetime
    item.common_metadata.end_datetime = end_datetime

    item_projection = ProjectionExtension.ext(item, add_if_missing=True)
    item_projection.epsg = GPW_EPSG
    item_projection.bbox = GPW_BOUNDING_BOX

    src = rasterio.open(pop_count)

    item_projection.transform = list(src.transform)
    item_projection.shape = [src.height, src.width]

    for key, href in [
        (POP_COUNT_KEY, pop_count),
        (POP_COUNT_ADJ_KEY, pop_count_adj),
        (POP_DENSITY_KEY, pop_density),
        (POP_DENSITY_ADJ_KEY, pop_density_adj),
    ]:
        item.add_asset(key, ITEM_ASSETS[key].create_asset(href))

    return item


def create_collection(output_url: str) -> pystac.Collection:
    """Create a STAC Collection for Gridded Population of
    #the World, Version 4 (GPWv4): Population Count dataset

    Args:
        output (str): Location to save the output STAC Collection json

    Returns:
        pystac.Collection: pystac collection object
    """
    utc = pytz.utc

    start_datetime = utc.localize(datetime.strptime(GPW_START_YEAR, "%Y"))
    end_datetime = utc.localize(datetime.strptime(GPW_END_YEAR, "%Y"))

    collection = pystac.Collection(
        id=GPW_ID,
        title=GPW_TITLE,
        description=DESCRIPTION,
        providers=[GPW_PROVIDER],
        license=LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent(GPW_BOUNDING_BOX),
            # `or None` fixes mypy issue with the DateTime being non-Optional
            pystac.TemporalExtent([[start_datetime or None, end_datetime]]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )
    collection.add_link(LICENSE_LINK)
    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = ITEM_ASSETS

    collection.set_self_href(output_url)
    collection.save_object()

    return collection
