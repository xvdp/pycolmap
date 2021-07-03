import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
    name="pycolmap",
    version="0.0.1",
    author="True Price",
    description="PyColmap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/google/nerfies/third_party/pycolmap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


import sys
import subprocess as sp
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
    raise RuntimeError("Python 3+ required.")

def readme():
    with open('README.md') as _fo:
        return _fo.read()

def set_version(version):
    with open('pycolmap/version.py', 'w') as _fi:
        _fi.write("version='"+version+"'")
    return version

def get_git_info():
    try:
        branches = sp.check_output(['git', 'branch']).strip().decode('ascii').split("\n")
        branch = [b for b in branches if b[0] == "*"][0].lstrip("*").lstrip(" ").rstrip(" ")
        commit = sp.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('ascii')
        return branch, commit
    except:
        return "0", "0"

def setup_package():
    ''' setup '''
    metadata = dict(
        name='pycolmap',
        version=set_version(version='0.0.1'),
        description='python >= 3.6',
        url="https://github.com/xvdp/pycolmap",
        author='True Price',
        license='MIT',
        install_requires=['numpy', 'plyfile'],
        packages=find_packages(),
        long_description=readme())

    setup(**metadata)

if __name__ == '__main__':
    setup_package()

