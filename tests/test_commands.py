import os.path
from tempfile import TemporaryDirectory
import logging
import pystac

from stactools.gpw.commands import create_gpw_command
from stactools.testing import CliTestCase

from tests import test_data

logger = logging.getLogger(__name__)


class CreateCollectionTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_gpw_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            json_path = os.path.join(tmp_dir, "test.json")
            result = self.run_command(
                ["gpw", "create-collection", "-d", json_path])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            # self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(os.path.join(tmp_dir, jsons[0]))

            collection.validate()

    def test_create_cog(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files")
            paths = [
                os.path.join(test_path, d) for d in os.listdir(test_path)
                if d.lower().endswith(".tif")
            ]

            for path in paths:
                result = self.run_command(
                    ["gpw", "create-cog", "-d", tmp_dir, "-s", path])
                self.assertEqual(result.exit_code,
                                 0,
                                 msg="\n{}".format(result.output))

                # cogs = [
                #     p for p in os.listdir(tmp_dir) if p.endswith("_cog.tif")
                # ]

                # self.assertEqual(len(cogs), 1)

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:

            test_path = test_data.get_path("data-files")
            paths = [
                os.path.join(test_path, d) for d in os.listdir(test_path)
                if d.lower().endswith(".tif")
            ]

            result = self.run_command(
                ["gpw", "create-item", "-d", tmp_dir, "-c"] + paths)
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            # self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])

            item = pystac.read_file(item_path)

        item.validate()
