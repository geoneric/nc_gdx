import codecs
import os.path
import re
import shlex
import subprocess
import sys
import tempfile


def assert_file_exists(
        pathname):

    if not os.path.isfile(pathname):
        raise RuntimeError(
            "Path {} does not exist or does not refer to "
            "a regular file".format(pathname))


def assert_directory_exists(
        pathname):

    if not os.path.isdir(pathname):
        raise RuntimeError(
            "Path {} does not exist or does not refer to "
            "a directory".format(pathname))


def assert_directories_exist(
        pathnames):

    for pathname in pathnames:
        assert_directory_exists(pathname)


def patch_script(
        script_file_pathname,
        raster_directory_pathname,
        table_directory_pathname,
        result_directory_pathname,
        mask_pathname=None):

    # All pathnames in the script must become absolute.
    raster_directory_pathname = os.path.abspath(raster_directory_pathname)
    table_directory_pathname = os.path.abspath(table_directory_pathname)
    result_directory_pathname = os.path.abspath(result_directory_pathname)
    mask_pathname = os.path.abspath(mask_pathname) \
        if mask_pathname is not None else None
    script = codecs.open(script_file_pathname, "r", "latin1").read()


    # Patch pathname of mask raster --------------------------------------------
    # The first line contains the relative pathname to the mask. By default
    # this is the name of the full area. It is located in the raster
    # directory.
    if mask_pathname is None:
        mask_pathname = "{}/fullarea.asc".format(raster_directory_pathname)
    script = script.replace("fullarea.asc", mask_pathname, 1)


    # Patch unzip commands -----------------------------------------------------
    # Unzip commands reference files in the local directory, while they
    # are stored in the raster directory. Instead of copying the zip, let's
    # just reference the original.
    # cmd unzip -u <file> -> cmd unzip -u <path>/<file>
    script = re.sub(
        r"cmd unzip -u[ \t]*(\w+)",
        r"cmd unzip -u {}/\1".format(raster_directory_pathname),
        script)


    # Patch references to tables -----------------------------------------------
    # In the script, tables are referenced using relative pathnames.
    # ../kt/<table> -> <path>/<table>
    script = re.sub(
        r"\.\./kt/",
        r"{}/".format(table_directory_pathname),
        script)


    # Patch result path --------------------------------------------------------
    # In the script, results are written to some fixed output directory. We
    # want this to be variable.
    # out/<raster> -> <path>/<raster>
    script = re.sub(
        r"out/",
        r"{}/".format(result_directory_pathname),
        script)

    # cd out -> cd <path>
    script = re.sub(
        r"cd out",
        r"cd {}".format(result_directory_pathname),
        script)

    # # unzip ... Outputmaps ... -> // unzip ... Outputmaps ...
    # script = re.sub(
    #     r"^(cmd .*Outputmaps.*)$",
    #     r"// \1",
    #     script, flags=re.MULTILINE)


    # Patch clean-up -----------------------------------------------------------
    # The script contains a line to remove generated files. Since we are
    # executing in a temp directory which is deleted automatically, we don't
    # need this.
    # cmd find ... xargs rm -> # cmd find ... xargs rm
    script = re.sub(
        r"^(cmd find.*xargs rm)",
        r"// \1",
        script, flags=re.MULTILINE)


    return script


def gdx(
        script_file_pathname,
        raster_directory_pathname,
        table_directory_pathname,
        result_directory_pathname,
        mask_pathname=None):

    # Validate arguments.
    assert_file_exists(script_file_pathname)
    assert_directories_exist(
        [raster_directory_pathname, table_directory_pathname])


    script = patch_script(
        script_file_pathname, raster_directory_pathname,
        table_directory_pathname, result_directory_pathname,
        mask_pathname)
    # print(script)


    with tempfile.TemporaryDirectory() as temp_directory_pathname:

        # Write patched script to new file.
        script_file_pathname = os.path.join(temp_directory_pathname,
                os.path.basename(script_file_pathname))
        open(script_file_pathname, "w").write(script)


        # The gdx command behaves differently, depending on whether the
        # path to the script file is relative or absolute...
        # Make sure that the path to the script is relative. That way it
        # will bail out in case the mask cannot be found. Otherwise it will
        # ask for user input.
        command = "gdx {}".format(os.path.basename(script_file_pathname))

        try:
            subprocess.run(
                shlex.split(command), cwd=temp_directory_pathname,
                universal_newlines=True,
                check=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as exception:
            raise RuntimeError(exception.stderr)
