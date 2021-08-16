# flake8: noqa

from pyproj import CRS
from pystac import Link, Provider, ProviderRole

GPW_ID = "GPW"
GPW_EPSG = 4326
GPW_CRS = CRS.from_epsg(GPW_EPSG)
GPW_TITLE = "Gridded Population of the World (GPW) v4, Population Count, v4.11"
LICENSE = "CC-BY-4.0"
LICENSE_LINK = Link(
    rel="license",
    target="https://creativecommons.org/licenses/by/4.0/legalcode",
    title="Creative Commons Attribution 4.0 International",
)

DESCRIPTION = """The Gridded Population of the World, Version 4 (GPWv4): Population Count, Revision 11 consists of estimates of human population (number of persons per pixel), consistent with national censuses and population registers, for the years 2000, 2005, 2010, 2015, and 2020."""

GPW_PROVIDER = Provider(
    name=
    "Center for International Earth Science Information Network - CIESIN - Columbia University",
    roles=[ProviderRole.PRODUCER, ProviderRole.PROCESSOR, ProviderRole.HOST],
    url=
    "https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-count-rev11")

GPW_BOUNDING_BOX = [-180.000000, 90.000000, 180.000000, -90.000000]
GPW_START_YEAR = '2000'
GPW_END_YEAR = '2020'
