# -*- coding: utf-8 -*-

import os
import shutil
import zipfile

import requests

from sources import BASE_URL, SOURCES
from errors import FileTypeNotSupported

VIM_DIR = ".vim"
VIM_RC = ".vimrc"


def _make_dirs(path):
    """Make directories in the path recursively."""
    os.makedirs(path, exist_ok=True)
    return True


def _copy_file(src, dst):
    """Copy a file from one directory to another."""
    shutil.copyfile(src, dst)
    return True


def _download_src(url, filename):
    """Download a source file and save it as the filename specified."""
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    return True


def _install_vmb(filename):
    """Install the given vimball file."""
    os.system("vim {filename} -c 'so % | q'".format(filename=filename))
    return True


def _install_zip(filename):
    """Install the given zip file."""
    d, f = os.path.split(filename)
    subdir = f[:-len(".zip")]
    zip_file = zipfile.ZipFile(filename)
    dir_zipped = all([os.path.dirname(name).split("/")[0] == subdir
                      for name in zip_file.namelist()])

    extract_to = d
    if not dir_zipped:
        extract_to = os.path.join(d, subdir)
        _make_dirs(extract_to)

    zip_file.extractall(path=extract_to)

    return True


def _get_file_ext(filename):
    """Extract the file extension of the file given."""
    return filename.split(".")[-1]


def install():
    """Process installation. Build required directories in the file system,
    copy the RC file to the desired location, download sources and set them up
    in the correct places."""
    home_dir = os.path.expanduser("~")
    vim_dir = os.path.join(home_dir, VIM_DIR)

    common_prefix = os.path.commonprefix([home_dir, vim_dir])
    assert home_dir == common_prefix

    _make_dirs(path=vim_dir)
    _copy_file(
        src=os.path.join(os.getcwd(), "vimrc"),
        dst=os.path.join(home_dir, VIM_RC),
    )

    installers = {
        "vim": None,
        "zip": _install_zip,
        "vmb": _install_vmb,
    }

    for subdir in SOURCES:
        _make_dirs(os.path.join(vim_dir, subdir))
        for source in SOURCES[subdir]:
            filename = os.path.join(vim_dir, subdir, source["filename"])
            file_ext = _get_file_ext(filename)
            if file_ext not in installers:
                raise FileTypeNotSupported(
                    "File type not supported: {file_ext}".format(
                        file_ext=file_ext,
                    )
                )

            url = "{base_url}?src_id={src_id}".format(
                base_url=BASE_URL,
                src_id=source["src_id"],
            )
            downloaded = _download_src(url=url, filename=filename)
            installer = installers[file_ext]
            if downloaded and installer:
                installer(filename)

if __name__ == "__main__":
    try:
        install()
        print("Installation complete")
    except Exception as e:
        print("Error: %s" % str(e))
