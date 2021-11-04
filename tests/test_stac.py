import os
import unittest
from tempfile import TemporaryDirectory

import pystac
import rasterio

from stactools.gpw import cog, stac
from tests import test_data


class StacTest(unittest.TestCase):
    def test_create_cog(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files/raw/population")
            paths = [
                os.path.join(test_path, d) for d in os.listdir(test_path)
                if d.lower().endswith(".tif")
            ]

            for path in paths:
                cog.create_cog(path, tmp_dir)

            cogs = [p for p in os.listdir(tmp_dir) if p.endswith("_cog.tif")]

            self.assertEqual(len(cogs), 1)

    def test_create_tiled_cog(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files/raw/population")
            paths = [
                os.path.join(test_path, d) for d in os.listdir(test_path)
                if d.lower().endswith(".tif")
            ]

            for path in paths:
                output_path = os.path.join(tmp_dir)
                cog.create_cog(path, output_path, tile=True)

            cogs = [p for p in os.listdir(tmp_dir) if p.endswith("_cog.tif")]

            self.assertEqual(len(cogs), 1)

    def test_create_tiled_cog_expand_bbox(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path(
                "data-files/tiles/ancillary/gpw_v4_data_quality_indicators_rev11_context_30_sec_2_1_cog.tif"  # noqa: E501
            )

            expanded_bbox = [-180, -77, -95, 7]

            output_path = cog.expand_bbox(test_path,
                                          tmp_dir,
                                          expanded_bbox=expanded_bbox)
            cogs = [
                p for p in os.listdir(tmp_dir) if p.endswith("expanded.tif")
            ]
            self.assertEqual(len(cogs), 1)

            with rasterio.open(os.path.join(tmp_dir, output_path)) as src:
                self.assertEqual(int(src.bounds.left), int(expanded_bbox[0]))
                self.assertEqual(int(src.bounds.bottom), int(expanded_bbox[1]))
                self.assertEqual(int(src.bounds.right), int(expanded_bbox[2]))
                self.assertEqual(int(src.bounds.top), int(expanded_bbox[3]))

    def test_create_pop_item(self):
        with TemporaryDirectory() as tmp_dir:

            test_path = test_data.get_path("data-files/tiles/population")
            paths = [
                os.path.join(test_path, d) for d in os.listdir(test_path)
                if d.lower().endswith(".tif")
            ]

            item = stac.create_pop_item(*paths)
            json_path = os.path.join(tmp_dir, f"{item.id}.json")
            item.set_self_href(json_path)
            item.make_asset_hrefs_relative()
            item.save_object()

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]

            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])

            item = pystac.read_file(item_path)

            item.validate()

    def test_create_anc_item(self):
        with TemporaryDirectory() as tmp_dir:

            test_path = test_data.get_path("data-files/tiles/ancillary")

            paths = [
                os.path.join(
                    test_path,
                    "gpw_v4_data_quality_indicators_rev11_context_30_sec_2_1_cog.tif",
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_data_quality_indicators_rev11_mean_adminunitarea_30_sec_2_1_cog.tif",
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_data_quality_indicators_rev11_watermask_30_sec_2_1_cog.tif",
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_basic_demographic_characteristics_rev11_atotpopbt_2010_cntm_30_sec_2_1_cog.tif",  # noqa:E501
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_basic_demographic_characteristics_rev11_atotpopbt_2010_dens_30_sec_2_1_cog.tif",  # noqa:E501
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_basic_demographic_characteristics_rev11_atotpopft_2010_cntm_30_sec_2_1_cog.tif",  # noqa:E501
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_basic_demographic_characteristics_rev11_atotpopft_2010_dens_30_sec_2_1_cog.tif",  # noqa:E501
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_basic_demographic_characteristics_rev11_atotpopmt_2010_cntm_30_sec_2_1_cog.tif",  # noqa:E501
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_basic_demographic_characteristics_rev11_atotpopmt_2010_dens_30_sec_2_1_cog.tif",  # noqa:E501
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_land_water_area_rev11_landareakm_30_sec_2_1_cog.tif",
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_land_water_area_rev11_waterareakm_30_sec_expanded_2_1_cog.tif",
                ),
                os.path.join(
                    test_path,
                    "gpw_v4_national_identifier_grid_rev11_30_sec_2_1_cog.tif",
                ),
            ]

            item = stac.create_anc_item(*paths)
            json_path = os.path.join(tmp_dir, f"{item.id}.json")
            item.set_self_href(json_path)
            item.make_asset_hrefs_relative()
            item.save_object()

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]

            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])

            item = pystac.read_file(item_path)

            item.validate()

    def test_create_pop_collection(self):
        with TemporaryDirectory() as tmp_dir:

            # Create stac collection
            json_path = os.path.join(tmp_dir, "collection.json")

            stac.create_pop_collection(json_path)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection_path = os.path.join(tmp_dir, jsons[0])

            collection = pystac.read_file(collection_path)

            collection.validate()

    def test_create_anc_collection(self):
        with TemporaryDirectory() as tmp_dir:

            # Create stac collection
            json_path = os.path.join(tmp_dir, "collection.json")

            stac.create_anc_collection(json_path)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection_path = os.path.join(tmp_dir, jsons[0])

            collection = pystac.read_file(collection_path)

            collection.validate()
