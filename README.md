# stactools-package gpw

- Name: Gridded Population of the World (GPW) v4, Population Count, v4.11
- Package: `stactools.gpw`
- PyPI: https://pypi.org/project/stactools-gpw/
- Owner: @sparkgeo
- Dataset homepage: https://sedac.ciesin.columbia.edu/data/collection/gpw-v4/sets/browse
- STAC extensions used:
  - [file](https://github.com/stac-extensions/file/)
  - [item-assets](https://github.com/stac-extensions/item-assets/)
  - [proj](https://github.com/stac-extensions/projection/)
  - [raster](https://github.com/stac-extensions/raster/)
  - [scientific](https://github.com/stac-extensions/scientific/)

The Gridded Population of the World, Version 4 (GPWv4) Revision 11 Population Datasets (population count, UN WPP-adjusted population count, population density, and UN WPP-adjusted population density) consist of estimates of human population (number of persons per pixel) and population density (number of persons per square kilometer), consistent with national censuses and population registers, for the years 2000, 2005, 2010, 2015, and 2020. Where indicated by name, values have been adjusted to match the 2015 Revision of the United Nation's World Population Prospects (UN WPP) country totals.

The Gridded Population of the World, Version 4 (GPWv4) Revision 11 Ancillary Datasets (data quality indicators, basic demographic characteristics, land and water area, and national identifier grid) provide context for the population count and density rasters found within the Gridded Population of the World Population Collection.

## Usage

### Using the CLI

```bash
mkdir example_output
# Create a COG - creates example_output/gpw_v4_population_count_rev11_2000_30_sec_cog.tif
stac gpw create-cog -d example_output -s tests/data-files/raw/population/gpw_v4_population_count_rev11_2000_30_sec.tif
# Create a COG - first expanding the dataset bbox, then retiling to 10000 x 10000 pixel COG files. Creates several tif files within example_output.
stac gpw create-cog -d example_output -s tests/data-files/raw/population/gpw_v4_population_count_rev11_2000_30_sec.tif -t -e -180 -90 180 90
# Create a population STAC Item - creates example_output/gpw_v4_rev11_2000_30_sec_2_1.json
stac gpw create-pop-item \
  -d example_output \
  -c \
  tests/data-files/tiles/population/gpw_v4_population_count_rev11_2000_30_sec_2_1_cog.tif \
  tests/data-files/tiles/population/gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev11_2000_30_sec_2_1_cog.tif \
  tests/data-files/tiles/population/gpw_v4_population_density_rev11_2000_30_sec_2_1_cog.tif \
  tests/data-files/tiles/population/gpw_v4_population_density_adjusted_to_2015_unwpp_country_totals_rev11_2000_30_sec_2_1_cog.tif
# Create an ancillary STAC Item - creates example_output/gpw_v4_rev11_30_sec_2_1.json
stac gpw create-anc-item \
  -d example_output \
  -c \
  tests/data-files/tiles/ancillary/gpw_v4_data_quality_indicators_rev11_context_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_data_quality_indicators_rev11_mean_adminunitarea_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_data_quality_indicators_rev11_watermask_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_basic_demographic_characteristics_rev11_atotpopbt_2010_cntm_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_basic_demographic_characteristics_rev11_atotpopbt_2010_dens_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_basic_demographic_characteristics_rev11_atotpopft_2010_cntm_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_basic_demographic_characteristics_rev11_atotpopft_2010_dens_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_basic_demographic_characteristics_rev11_atotpopmt_2010_cntm_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_basic_demographic_characteristics_rev11_atotpopmt_2010_dens_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_land_water_area_rev11_landareakm_30_sec_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_land_water_area_rev11_waterareakm_30_sec_expanded_2_1_cog.tif \
  tests/data-files/tiles/ancillary/gpw_v4_national_identifier_grid_rev11_30_sec_2_1_cog.tif

# Create a population STAC Collection - creates example_output/collection.json
stac gpw create-pop-collection -d example_output/collection.json

# Create a population STAC Collection - creates example_output/collection.json
stac gpw create-anc-collection -d example_output/collection.json
```

### As a python module

```python
from stactools.gpw import cog, stac

# Create a population (or ancillary) STAC Collection
stac.create_pop_collection("example_output/collection.json")
# stac.create_anc_collection("example_output/collection.json")

# Create a COG (optional parameters to retile or expand tiled output)
cog.create_cog("/path/to/local.tif", "/path/to/output_directory")

# Create a population STAC Item
cog_list = [
    Path to population count COG
    Path to adjusted population count COG
    Path to population density COG
    Path to adjusted population density COG
]
stac.create_pop_item(*cog_list)

# Create a population STAC Item
cog_list = [
    Path to Data Quality Indicators - Data Context COG
    Path to Data Quality Indicators - Mean Administrative Unit Area COG
    Path to Data Quality Indicators - Water Mask COG
    Path to Basic Demographic Characteristics - Ttl Pop Count
    Path to Basic Demographic Characteristics - Ttl Pop Density
    Path to Basic Demographic Characteristics - Female Count
    Path to Basic Demographic Characteristics - Female Density
    Path to Basic Demographic Characteristics - Male Count
    Path to Basic Demographic Characteristics - Male Density
    Path to Land Area COG
    Path to Water Area COG
    Path to National Identifier Grid COG
]
stac.create_anc_item(*cog_list)
```
