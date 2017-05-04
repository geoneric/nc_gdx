#!/usr/bin/env python
import os.path
import sys
# import traceback
import docopt
import gdx_


doc_string = """\
Run a GDX script

usage:
    {command} [--mask <mask>] <script> <rasters> <kts> <results>

arguments:
    script      Path to script to run
    rasters     Path to directory containing input rasters
    kts         Path to directory containing knowledge tables
    results     Path to directory to write results to

options:
    -h --help   Show this screen
    --mask <mask>  Path to raster to use as mask

- Existing results will be overwritten
- In case a mask is not passed in, the mask set in the script it used
""".format(
        command=os.path.basename(sys.argv[0]))


def gdx(
        *args,
        **kwargs):

    try:
        gdx_.gdx(*args, **kwargs)
        result = 0
    except Exception as exception:
        # traceback.print_exc(file=sys.stderr)
        sys.stderr.write("{}\n".format(exception))
        result = 1

    return result


if __name__ == "__main__":
    arguments = docopt.docopt(doc_string)
    script_file_pathname = arguments["<script>"]
    raster_directory_pathname = arguments["<rasters>"]
    table_directory_pathname = arguments["<kts>"]
    result_directory_pathname = arguments["<results>"]
    mask_pathname = arguments["--mask"]

    sys.exit(gdx(
        script_file_pathname,
        raster_directory_pathname, table_directory_pathname,
        result_directory_pathname,
        mask_pathname=mask_pathname))
