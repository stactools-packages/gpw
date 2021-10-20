from typing import Dict

import pystac
from pystac.extensions.item_assets import AssetDefinition

ARC30S_KEY = "30s1km"
ARC2M30S_KEY = "2min30s5km"
ARC15M_KEY = "15min30km"
ARC30M_KEY = "30min55km"
ARC60M_KEY = "60min110km"

ITEM_ASSETS: Dict[str, AssetDefinition] = {
    ARC30S_KEY:
    AssetDefinition({
        "title":
        "30 arc-seconds, 1km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Population Count, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
    ARC2M30S_KEY:
    AssetDefinition({
        "title":
        "2.5 arc-minutes, 5km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Population Count, 5km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
    ARC15M_KEY:
    AssetDefinition({
        "title":
        "15 arc-minutes, 30km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Population Count, 30km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
    ARC30M_KEY:
    AssetDefinition({
        "title":
        "30 arc-minutes, 55km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Population Count, 55km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
    ARC60M_KEY:
    AssetDefinition({
        "title":
        "60 arc-minutes, 110km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Population Count, 110km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
}
