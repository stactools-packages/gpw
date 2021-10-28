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
        "sci:doi":
        "10.7927/H4JW8BX5",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Population Count, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4JW8BX5. Accessed 22 October 2021.",  # noqa: E501
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
        "sci:doi":
        "10.7927/H4PN93PB",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Population Count Adjusted to Match 2015 Revision of UN WPP Country Totals, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4PN93PB. Accessed 22 October 2021.",  # noqa: E501
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
        "sci:doi":
        "10.7927/H49C6VHW",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Population Density, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H49C6VHW. Accessed 22 October 2021.",  # noqa: E501
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
        "sci:doi":
        "10.7927/H4F47M65",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Population Density Adjusted to Match 2015 Revision UN WPP Country Totals, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4F47M65. Accessed 22 October 2021.",  # noqa: E501
    }),
}
