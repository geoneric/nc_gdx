import glob
import os
import shutil
import unittest
from nc_gdx.gdx_ import *


class GDXTest(unittest.TestCase):

    def test_gdx_installed(self):
        path = shutil.which("gdx")
        self.assertTrue(path is not None)


    def test_gdx_data_mounted(self):
        gdx_data_pathname = os.environ.get("GDX_DATA") or "/gdx_data"
        self.assertTrue(os.path.isdir(gdx_data_pathname))

        knowledge_table_directory_pathname = \
            os.path.join(gdx_data_pathname, "kt")
        self.assertTrue(os.path.isdir(knowledge_table_directory_pathname))
        self.assertTrue(len(glob.glob(
            os.path.join(knowledge_table_directory_pathname, "*.tab"))) > 0)

        raster_directory_pathname = \
            os.path.join(gdx_data_pathname, "raster")
        self.assertTrue(os.path.isdir(raster_directory_pathname))
        self.assertTrue(len(glob.glob(
            os.path.join(raster_directory_pathname, "*.asc"))) > 0)


if __name__ == "__main__":
    unittest.main()
