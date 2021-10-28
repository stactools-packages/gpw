# flake8: noqa

from pyproj import CRS
from pystac import Link, Provider, ProviderRole

GPW_EPSG = 4326
GPW_CRS = CRS.from_epsg(GPW_EPSG)
GPW_LICENSE = "CC-BY-4.0"
GPW_LICENSE_LINK = Link(
    rel="license",
    target="https://creativecommons.org/licenses/by/4.0/legalcode",
    title="Creative Commons Attribution 4.0 International",
)
GPW_PROVIDER = Provider(
    name=
    "Center for International Earth Science Information Network - CIESIN - Columbia University",
    roles=[ProviderRole.PRODUCER, ProviderRole.PROCESSOR, ProviderRole.HOST],
    url=
    "https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-count-rev11",
)
GPW_BOUNDING_BOX = [-180.000000, 90.000000, 180.000000, -90.000000]
GPW_TILING_PIXEL_SIZE = (10001, 10001)

GPW_POP_ID = "GPW-population"
GPW_POP_TITLE = "Gridded Population of the World (GPW) v4.11, Population Datasets"
GPW_POP_DESCRIPTION = (
    f"The Gridded Population of the World, Version 4 (GPWv4) Revision 11 Population Datasets (population count, "
    f"UN WPP-adjusted population count, population density, and UN WPP-adjusted population density) consist "
    f"of estimates of human population (number of persons per pixel) and population density (number of persons "
    f"per square kilometer), consistent with national censuses and population registers, for the years 2000, 2005, "
    f"2010, 2015, and 2020. Where indicated by name, values have been adjusted to match the 2015 Revision of the "
    f"United Nation's World Population Prospects (UN WPP) country totals.")

GPW_POP_START_YEAR = "2000"
GPW_POP_END_YEAR = "2020"
