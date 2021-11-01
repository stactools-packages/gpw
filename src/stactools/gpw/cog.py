import logging
import os
from glob import glob
from subprocess import CalledProcessError, check_output
from tempfile import TemporaryDirectory
from typing import List, Union

import rasterio

from stactools.gpw.constants import GPW_TILING_PIXEL_SIZE

logger = logging.getLogger(__name__)


def create_cog(
    input_path: str,
    output_dir: str,
    raise_on_fail: bool = True,
    dry_run: bool = False,
    tile: bool = False,
    expanded_bbox: List[Union[float, int, str]] = [],
) -> str:
    """Create COG from a tif

    Args:
        input_path (str): Path to tif.
        output_path (str): The path to which the COG will be written.
        raise_on_fail (bool, optional): Whether to raise error on failure.
            Defaults to True.
        dry_run (bool, optional): Run without downloading tif, creating COG,
            and writing COG. Defaults to False.
        tile (bool, optional): Tile the tiff into many smaller files
        expanded_bbox (list, optional): Expand input bounding box before processing. Bounding
            box should be in the order: [xmin, ymin, xmax, ymax]

    Returns:
        str: The path to the output COG(s)
    """

    try:
        if dry_run:
            logger.info(
                "Would have downloaded TIF, created COG, and written COG")
        else:
            if tile:
                return create_retiled_cogs(input_path, output_dir,
                                           raise_on_fail, dry_run,
                                           expanded_bbox)
            else:
                output_path = os.path.join(
                    output_dir,
                    os.path.basename(input_path)[:-4] + "_cog.tif")
                create_single_cog(input_path, output_path, raise_on_fail,
                                  dry_run)

    except Exception:
        logger.error("Failed to process {}".format(output_dir))

        if raise_on_fail:
            raise

    return output_path


def create_single_cog(
    input_path: str,
    output_path: str,
    raise_on_fail: bool = True,
    dry_run: bool = False,
) -> str:
    """Create COG from a TIFF
    Args:
        input_path (str): Path to the GeoTiff data.
        output_path (str): The path to which the COG will be written.
        raise_on_fail (bool, optional): Whether to raise error on failure.
            Defaults to True.
        dry_run (bool, optional): Run without downloading TIFF, creating COG,
            and writing COG. Defaults to False.
    Returns:
        str: The path to the output COG.
    """

    output = None
    try:
        if dry_run:
            logger.info("Would have read TIFF, created COG, and written COG")
        else:
            logger.info("Converting TIFF to COG")
            logger.debug(f"input_path: {input_path}")
            logger.debug(f"output_path: {output_path}")
            cmd = [
                "gdal_translate",
                "-of",
                "COG",
                "-co",
                "NUM_THREADS=ALL_CPUS",
                "-co",
                "BLOCKSIZE=512",
                "-co",
                "COMPRESS=DEFLATE",
                "-co",
                "LEVEL=9",
                "-co",
                "PREDICTOR=YES",
                "-co",
                "OVERVIEWS=IGNORE_EXISTING",
                input_path,
                output_path,
            ]

            try:
                output = check_output(cmd)
            except CalledProcessError as e:
                output = e.output
                raise
            finally:
                logger.info(f"output: {str(output)}")

    except Exception:
        logger.error("Failed to process {}".format(output_path))

        if raise_on_fail:
            raise

    return output_path


def create_retiled_cogs(
    input_path: str,
    output_directory: str,
    raise_on_fail: bool = True,
    dry_run: bool = False,
    expanded_bbox: List[Union[float, int, str]] = [],
) -> str:
    """Split tiff into tiles and create COGs
    Args:
        input_path (str): Path to the GeoTiff data.
        output_directory (str): The directory to which the COG will be written.
        raise_on_fail (bool, optional): Whether to raise error on failure.
            Defaults to True.
        dry_run (bool, optional): Run without downloading tif, creating COG,
            and writing COG. Defaults to False.
        expanded_bbox (list, optional): Expand input bounding box before processing. Bounding
            box should be in the order: [xmin, ymin, xmax, ymax]
    Returns:
        str: The path to the output COGs.
    """
    output = None
    try:
        if dry_run:
            logger.info(
                "Would have split TIFF into tiles, created COGs, and written COGs"
            )
        else:
            logger.info("Retiling TIFF")
            logger.debug(f"input_path: {input_path}")
            logger.debug(f"output_directory: {output_directory}")
            with TemporaryDirectory() as tmp_dir:
                if expanded_bbox:
                    input_path = expand_bbox(input_path, tmp_dir,
                                             expanded_bbox)

                cmd = [
                    "gdal_retile.py",
                    "-ps",
                    str(GPW_TILING_PIXEL_SIZE[0]),
                    str(GPW_TILING_PIXEL_SIZE[1]),
                    "-targetDir",
                    tmp_dir,
                    input_path,
                ]
                try:
                    output = check_output(cmd)
                except CalledProcessError as e:
                    output = e.output
                    raise
                finally:
                    logger.info(f"output: {str(output)}")
                file_names = glob(f"{tmp_dir}/*.tif")
                for f in [
                        i for i in file_names
                        if not i.endswith("_expanded.tif")
                ]:
                    input_file = os.path.join(tmp_dir, f)
                    output_file = os.path.join(
                        output_directory,
                        os.path.basename(f).replace(".tif", "") + "_cog.tif",
                    )
                    with rasterio.open(input_file, "r") as dataset:
                        contains_data = dataset.read().any()
                    # Exclude empty files
                    if contains_data:
                        logger.debug(f"Tile contains data: {input_file}")
                        create_single_cog(input_file, output_file,
                                          raise_on_fail, dry_run)
                    else:
                        logger.debug(f"Ignoring empty tile: {input_file}")

    except Exception:
        logger.error("Failed to process {}".format(input_path))

        if raise_on_fail:
            raise

    return output_directory


def expand_bbox(
    input_path: str,
    tmp_dir: str,
    expanded_bbox: List[Union[float, int, str]] = [],
) -> str:
    output_path = os.path.join(
        tmp_dir,
        f'{os.path.basename(input_path).replace(".tif", "_expanded.tif")}')
    cmd = [
        "gdalwarp",
        "-overwrite",
        "-co",
        "NUM_THREADS=ALL_CPUS",
        "-co",
        "COMPRESS=DEFLATE",
        "-te",
        str(expanded_bbox[0]),
        str(expanded_bbox[1]),
        str(expanded_bbox[2]),
        str(expanded_bbox[3]),
        "-ts",
        "43200",
        "21600",
        input_path,
        output_path,
    ]

    try:
        output = check_output(cmd)
    except CalledProcessError as e:
        output = e.output
        raise
    finally:
        logger.info(f"output: {str(output)}")

    return output_path
