from typing import Dict

import pystac
from pystac.extensions.item_assets import AssetDefinition

POP_COUNT_KEY = "pop_count"
POP_COUNT_ADJ_KEY = "pop_count_adj"
POP_DENSITY_KEY = "pop_density"
POP_DENSITY_ADJ_KEY = "pop_density_adj"

ITEM_ASSETS: Dict[str, AssetDefinition] = {
    POP_COUNT_KEY:
    AssetDefinition({
        "title":
        "Population Count, 1km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Population Count, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
    POP_COUNT_ADJ_KEY:
    AssetDefinition({
        "title":
        "UN WPP-Adjusted Population Count, 1km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): UN WPP-Adjusted Population Count, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
    POP_DENSITY_KEY:
    AssetDefinition({
        "title":
        "Population Density, 1km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Population Density, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
    POP_DENSITY_ADJ_KEY:
    AssetDefinition({
        "title":
        "UN WPP-Adjusted Population Density, 1km",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): UN WPP-Adjusted Population Density, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
    }),
}
