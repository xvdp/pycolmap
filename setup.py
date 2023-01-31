from setuptools import setup, find_packages

def readme():
    with open('README.md') as _fo:
        return _fo.read()

def set_version(version):
    with open('pycolmap/version.py', 'w') as _fi:
        _fi.write("version='"+version+"'")
    return version

def install_requires():
    with open('requirements.txt') as _fo:
        return _fo.read().split()

def setup_package():
    ''' setup '''
    metadata = dict(
        name='pycolmap',
        version=set_version(version='0.0.3'),
        description='python >= 3.6',
        url="https://github.com/xvdp/pycolmap",
        author='True Price',
        license='MIT',
        install_requires=install_requires(),
        packages=find_packages(),
        long_description=readme())

    setup(**metadata)

if __name__ == '__main__':
    setup_package()
# python setup.py install