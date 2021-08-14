import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import shapely
import rasterio
import pytz

import pystac
from pystac.extensions.item_assets import ItemAssetsExtension

from pystac.extensions.projection import ProjectionExtension

from stactools.gpw.constants import (GPW_ID, GPW_EPSG, GPW_TITLE, DESCRIPTION,
                                     GPW_PROVIDER, LICENSE, LICENSE_LINK,
                                     GPW_BOUNDING_BOX, GPW_START_YEAR,
                                     GPW_END_YEAR)

from stactools.gpw.assets import (ITEM_ASSETS, ARC30S_KEY, ARC2M30S_KEY,
                                  ARC15M_KEY, ARC30M_KEY, ARC60M_KEY)

logger = logging.getLogger(__name__)


def create_item(output_url: str, arc30s_href: str, arc2M30s_href: str,
                arc15m_href: str, arc30m_href: str,
                arc60m_href: str) -> pystac.Item:
    """Creates a STAC item for Gridded Population of the World,
    Version 4 (GPWv4): Population Count dataset.

    Args:
        output_url (str): Path to output STAC item.
        cog_href (str): Path to COG asset.

    Returns:
        pystac.Item: STAC Item object.
    """

    item_id = arc30s_href.split(".")[0].split("/")[-1]

    year = re.search("\d{4}", item_id).group()  # noqa

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
    item = pystac.Item(id=item_id,
                       geometry=geometry,
                       bbox=GPW_BOUNDING_BOX,
                       datetime=dataset_datetime,
                       properties=properties)

    item.common_metadata.start_datetime = start_datetime
    item.common_metadata.end_datetime = end_datetime

    item_projection = ProjectionExtension.ext(item, add_if_missing=True)
    item_projection.epsg = GPW_EPSG
    item_projection.bbox = GPW_BOUNDING_BOX

    src = rasterio.open(arc30s_href)

    item_projection.transform = list(src.transform)
    item_projection.shape = [src.height, src.width]

    for key, href in [(ARC30S_KEY, arc30s_href), (ARC2M30S_KEY, arc2M30s_href),
                      (ARC15M_KEY, arc15m_href), (ARC30M_KEY, arc30m_href),
                      (ARC60M_KEY, arc60m_href)]:
        item.add_asset(key, ITEM_ASSETS[key].create_asset(href))

    item.set_self_href(output_url)
    item.save_object()

    return item


def create_collection(output_url: str):
    """Create a STAC Collection for Gridded Population of
    #the World, Version 4 (GPWv4): Population Count dataset

    Args:
        output (str): Location to save the output STAC Collection json

    Returns:
        pystac.Collection: pystac collection object
    """
    utc = pytz.utc

    dataset_datetime = utc.localize(datetime.strptime(GPW_START_YEAR, "%Y"))
    end_datetime = utc.localize(datetime.strptime(GPW_END_YEAR, "%Y"))
    start_datetime = dataset_datetime

    collection = pystac.Collection(
        id=GPW_ID,
        title=GPW_TITLE,
        description=DESCRIPTION,
        providers=[GPW_PROVIDER],
        license=LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent(GPW_BOUNDING_BOX),
            pystac.TemporalExtent([start_datetime, end_datetime]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )
    collection.add_link(LICENSE_LINK)
    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = ITEM_ASSETS

    collection.set_self_href(output_url)
    collection.save_object()

    return collection
