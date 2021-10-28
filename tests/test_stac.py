import os
import unittest
from tempfile import TemporaryDirectory

import pystac

from stactools.gpw import cog, stac
from tests import test_data


class StacTest(unittest.TestCase):
    def test_create_cog(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files/raw")
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
            test_path = test_data.get_path("data-files/raw")
            paths = [
                os.path.join(test_path, d) for d in os.listdir(test_path)
                if d.lower().endswith(".tif")
            ]

            for path in paths:
                output_path = os.path.join(tmp_dir)
                cog.create_cog(path, output_path, tile=True)

            cogs = [p for p in os.listdir(tmp_dir) if p.endswith("_cog.tif")]

            self.assertEqual(len(cogs), 1)

    def test_create_pop_item(self):
        with TemporaryDirectory() as tmp_dir:

            test_path = test_data.get_path("data-files/tiles")
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
