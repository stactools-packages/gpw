import logging
import os
import re
from datetime import datetime
from typing import Optional

import fsspec
import pystac
import pytz
import rasterio
import shapely
from dateutil.relativedelta import relativedelta
from pystac.extensions.file import FileExtension
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterBand, RasterExtension
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.version import ItemVersionExtension
from stactools.core.io import ReadHrefModifier

from stactools.gpw.assets import (
    ANC_BDC_BT_COUNT,
    ANC_BDC_BT_DENSITY,
    ANC_BDC_FT_COUNT,
    ANC_BDC_FT_DENSITY,
    ANC_BDC_MT_COUNT,
    ANC_BDC_MT_DENSITY,
    ANC_DQI_ADMIN_KEY,
    ANC_DQI_CONTEXT_KEY,
    ANC_DQI_WATERMASK_KEY,
    ANC_ITEM_ASSETS,
    ANC_LAND_AREA_KEY,
    ANC_NAT_ID_GRID_KEY,
    ANC_WATER_AREA_KEY,
    POP_COUNT_ADJ_KEY,
    POP_COUNT_KEY,
    POP_DENSITY_ADJ_KEY,
    POP_DENSITY_KEY,
    POP_ITEM_ASSETS,
)
from stactools.gpw.constants import (
    GPW_ANC_DESCRIPTION,
    GPW_ANC_END_YEAR,
    GPW_ANC_ID,
    GPW_ANC_START_YEAR,
    GPW_ANC_TITLE,
    GPW_BOUNDING_BOX,
    GPW_EPSG,
    GPW_LICENSE,
    GPW_LICENSE_LINK,
    GPW_POP_DESCRIPTION,
    GPW_POP_END_YEAR,
    GPW_POP_ID,
    GPW_POP_START_YEAR,
    GPW_POP_TITLE,
    GPW_PROVIDER,
    GPW_VERSION,
)

logger = logging.getLogger(__name__)


def create_pop_item(
    pop_count: str,
    pop_count_adj: str,
    pop_density: str,
    pop_density_adj: str,
    cog_href_modifier: Optional[ReadHrefModifier] = None,
) -> pystac.Item:
    """Creates a STAC item for Gridded Population of the World,
    Version 4 (GPWv4): Population datasets.

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
        "description": GPW_POP_DESCRIPTION,
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

    signed_cog_href = cog_href_modifier(
        pop_count) if cog_href_modifier else pop_count

    src = rasterio.open(signed_cog_href)

    item_projection.transform = list(src.transform)
    item_projection.shape = [src.height, src.width]

    item_version = ItemVersionExtension.ext(item, add_if_missing=True)
    item_version.version = GPW_VERSION

    for key, href in [
        (POP_COUNT_KEY, pop_count),
        (POP_COUNT_ADJ_KEY, pop_count_adj),
        (POP_DENSITY_KEY, pop_density),
        (POP_DENSITY_ADJ_KEY, pop_density_adj),
    ]:
        cog_asset = POP_ITEM_ASSETS[key].create_asset(href)
        item.add_asset(key, cog_asset)

        signed_cog_href = cog_href_modifier(
            href) if cog_href_modifier else href

        asset_file = FileExtension.ext(cog_asset, add_if_missing=True)
        with fsspec.open(signed_cog_href) as file:
            size = file.size
            if size is not None:
                asset_file.size = size

        with rasterio.open(signed_cog_href) as src:
            asset_raster = RasterExtension.ext(cog_asset, add_if_missing=True)
            asset_raster.bands = [
                RasterBand.create(
                    data_type=src.dtypes[0],
                    sampling=src.tags().get("AREA_OR_POINT").lower(),
                )
            ]

    return item


def create_anc_item(
    dqi_context: str,
    dqi_admin: str,
    dqi_watermask: str,
    bdc_bt_count: str,
    bdc_bt_density: str,
    bdc_ft_count: str,
    bdc_ft_density: str,
    bdc_mt_count: str,
    bdc_mt_density: str,
    land_area: str,
    water_area: str,
    nat_id_grid: str,
    cog_href_modifier: Optional[ReadHrefModifier] = None,
) -> pystac.Item:
    """Creates a STAC item for Gridded Population of the World,
    Version 4 (GPWv4): Ancillary datasets.

    Args:
        dqi_context (str): Path to tiled Data Quality Indicators - Data Context COG
        dqi_admin (str): Path to tiled Data Quality Indicators - Mean Administrative Unit Area COG
        dqi_watermask (str): Path to tiled Data Quality Indicators - Water Mask COG
        bdc_bt_count (str): Path to the tiled Basic Demographic Characteristics - Ttl Pop Count
        bdc_bt_density (str): Path to the tiled Basic Demographic Characteristics - Ttl Pop Density
        bdc_ft_count (str): Path to the tiled Basic Demographic Characteristics - Female Count
        bdc_ft_density (str): Path to the tiled Basic Demographic Characteristics - Female Density
        bdc_mt_count (str): Path to the tiled Basic Demographic Characteristics - Male Count
        bdc_mt_density (str): Path to the tiled Basic Demographic Characteristics - Male Density
        land_area (str): Path to tiled Land Area COG
        water_area (str): Path to tiled Water Area COG
        nat_id_grid (str): Path to tiled National Identifier Grid COG
        cog_href_modifier (Optional[ReadHrefModifier], optional): [description]. Defaults to None.

    Returns:
        pystac.Item: STAC Item object.
    """

    # construct an item id like: gpw_v4_rev11_30_sec_1_1
    split_basename = os.path.basename(dqi_context).split("_")
    item_id = "_".join(
        [*split_basename[0:2], split_basename[5], *split_basename[7:11]])

    utc = pytz.utc

    dataset_datetime = utc.localize(datetime.strptime("2010-07-01",
                                                      "%Y-%m-%d"))

    polygon = shapely.geometry.box(*GPW_BOUNDING_BOX, ccw=True)
    coordinates = [list(i) for i in list(polygon.exterior.coords)]

    geometry = {"type": "Polygon", "coordinates": [coordinates]}

    properties = {
        "description": GPW_ANC_DESCRIPTION,
    }

    # Create item
    item = pystac.Item(
        id=item_id,
        geometry=geometry,
        bbox=GPW_BOUNDING_BOX,
        datetime=dataset_datetime,
        properties=properties,
    )

    item_projection = ProjectionExtension.ext(item, add_if_missing=True)
    item_projection.epsg = GPW_EPSG
    item_projection.bbox = GPW_BOUNDING_BOX

    signed_cog_href = (cog_href_modifier(dqi_context)
                       if cog_href_modifier else dqi_context)

    src = rasterio.open(signed_cog_href)

    item_projection.transform = list(src.transform)
    item_projection.shape = [src.height, src.width]

    item_version = ItemVersionExtension.ext(item, add_if_missing=True)
    item_version.version = GPW_VERSION

    for key, href in [
        (ANC_DQI_CONTEXT_KEY, dqi_context),
        (ANC_DQI_ADMIN_KEY, dqi_admin),
        (ANC_DQI_WATERMASK_KEY, dqi_watermask),
        (ANC_BDC_BT_COUNT, bdc_bt_count),
        (ANC_BDC_BT_DENSITY, bdc_bt_density),
        (ANC_BDC_FT_COUNT, bdc_ft_count),
        (ANC_BDC_FT_DENSITY, bdc_ft_density),
        (ANC_BDC_MT_COUNT, bdc_mt_count),
        (ANC_BDC_MT_DENSITY, bdc_mt_density),
        (ANC_LAND_AREA_KEY, land_area),
        (ANC_WATER_AREA_KEY, water_area),
        (ANC_NAT_ID_GRID_KEY, nat_id_grid),
    ]:
        cog_asset = ANC_ITEM_ASSETS[key].create_asset(href)
        item.add_asset(key, cog_asset)

        signed_cog_href = cog_href_modifier(
            href) if cog_href_modifier else href

        asset_file = FileExtension.ext(cog_asset, add_if_missing=True)
        with fsspec.open(signed_cog_href) as file:
            size = file.size
            if size is not None:
                asset_file.size = size

        with rasterio.open(signed_cog_href) as src:
            asset_raster = RasterExtension.ext(cog_asset, add_if_missing=True)
            asset_raster.bands = [
                RasterBand.create(
                    data_type=src.dtypes[0],
                    sampling=src.tags().get("AREA_OR_POINT").lower(),
                )
            ]

    return item


def create_pop_collection(output_url: str) -> pystac.Collection:
    """Create a STAC Collection for Gridded Population of
    the World, Version 4 (GPWv4): Population datasets

    Args:
        output (str): Location to save the output STAC Collection json

    Returns:
        pystac.Collection: pystac collection object
    """
    utc = pytz.utc

    start_datetime = utc.localize(datetime.strptime(GPW_POP_START_YEAR, "%Y"))
    end_datetime = utc.localize(datetime.strptime(GPW_POP_END_YEAR, "%Y"))

    collection = pystac.Collection(
        id=GPW_POP_ID,
        title=GPW_POP_TITLE,
        description=GPW_POP_DESCRIPTION,
        providers=[GPW_PROVIDER],
        license=GPW_LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent(GPW_BOUNDING_BOX),
            # `or None` fixes mypy issue with the DateTime being non-Optional
            pystac.TemporalExtent([[start_datetime or None, end_datetime]]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )
    collection.add_link(GPW_LICENSE_LINK)
    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = POP_ITEM_ASSETS

    ScientificExtension.ext(collection, add_if_missing=True)

    collection.set_self_href(output_url)
    collection.save_object()

    return collection


def create_anc_collection(output_url: str) -> pystac.Collection:
    """Create a STAC Collection for Gridded Population of
    the World, Version 4 (GPWv4): Ancillary datasets

    Args:
        output (str): Location to save the output STAC Collection json

    Returns:
        pystac.Collection: pystac collection object
    """
    utc = pytz.utc

    start_datetime = utc.localize(datetime.strptime(GPW_ANC_START_YEAR, "%Y"))
    end_datetime = utc.localize(datetime.strptime(GPW_ANC_END_YEAR, "%Y"))

    collection = pystac.Collection(
        id=GPW_ANC_ID,
        title=GPW_ANC_TITLE,
        description=GPW_ANC_DESCRIPTION,
        providers=[GPW_PROVIDER],
        license=GPW_LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent(GPW_BOUNDING_BOX),
            # `or None` fixes mypy issue with the DateTime being non-Optional
            pystac.TemporalExtent([[start_datetime or None, end_datetime]]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )
    collection.add_link(GPW_LICENSE_LINK)
    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = ANC_ITEM_ASSETS

    ScientificExtension.ext(collection, add_if_missing=True)

    collection.set_self_href(output_url)
    collection.save_object()

    return collection
