from typing import Dict

import pystac
from pystac.extensions.item_assets import AssetDefinition

POP_COUNT_KEY = "pop_count"
POP_COUNT_ADJ_KEY = "pop_count_adj"
POP_DENSITY_KEY = "pop_density"
POP_DENSITY_ADJ_KEY = "pop_density_adj"
ANC_DQI_CONTEXT_KEY = "anc_dqi_context"
ANC_DQI_ADMIN_KEY = "anc_dqi_admin"
ANC_DQI_WATERMASK_KEY = "anc_dqi_watermask"
# TODO: add basic demographic characteristics asset(s)
# ANC_BDC_ = ""
ANC_LAND_AREA_KEY = "anc_land_area"
ANC_WATER_AREA_KEY = "anc_water_area"
ANC_NAT_ID_GRID_KEY = "anc_nat_id_grid"

POP_ITEM_ASSETS: Dict[str, AssetDefinition] = {
    POP_COUNT_KEY:
    AssetDefinition({
        "title":
        "Population Count",
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
        "UN WPP-Adjusted Population Count",
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
        "Population Density",
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
        "UN WPP-Adjusted Population Density",
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

ANC_ITEM_ASSETS: Dict[str, AssetDefinition] = {
    ANC_DQI_CONTEXT_KEY:
    AssetDefinition({
        "title":
        "Data Quality Indicators - Data Context",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Data Quality Indicators - Data Context, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
        "sci:doi":
        "10.7927/H42Z13KG",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Data Quality Indicators, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H42Z13KG. Accessed 22 Octover 2021.",  # noqa: E501
    }),
    ANC_DQI_ADMIN_KEY:
    AssetDefinition({
        "title":
        "Data Quality Indicators - Mean Administrative Unit Area",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Data Quality Indicators - Mean Administrative Unit Area, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
        "sci:doi":
        "10.7927/H42Z13KG",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Data Quality Indicators, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H42Z13KG. Accessed 22 October 2021.",  # noqa: E501
    }),
    ANC_DQI_WATERMASK_KEY:
    AssetDefinition({
        "title":
        "Data Quality Indicators - Water Mask",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Data Quality Indicators - Water Mask, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
        "sci:doi":
        "10.7927/H42Z13KG",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Data Quality Indicators, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H42Z13KG. Accessed 22 October 2021.",  # noqa: E501
    }),
    ANC_LAND_AREA_KEY:
    AssetDefinition({
        "title":
        "Land Area",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Land Area, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
        "sci:doi":
        "10.7927/H4Z60M4Z",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Land and Water Area, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4Z60M4Z. Accessed 22 October 2021.",  # noqa: E501
    }),
    ANC_WATER_AREA_KEY:
    AssetDefinition({
        "title":
        "Water Area",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): Water Area, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
        "sci:doi":
        "10.7927/H4Z60M4Z",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Land and Water Area, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4Z60M4Z. Accessed 22 October 2021.",  # noqa: E501
    }),
    ANC_NAT_ID_GRID_KEY:
    AssetDefinition({
        "title":
        "National Identifier Grid",
        "description": (
            "Gridded Population of the World, Version 4 (GPWv4): UN WPP-Adjusted Population Density, 30 arc-seconds, 1km resolution"  # noqa: E501
        ),
        "type":
        pystac.MediaType.COG,
        "roles": ["data"],
        "sci:doi":
        "10.7927/H4TD9VDP",
        "sci:citation":
        "Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): National Identifier Grid, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4TD9VDP. Accessed 22 October 2021.",  # noqa: E501
    }),
}
