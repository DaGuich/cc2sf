from setuptools import setup, find_packages


def read_file(file_name):
    with open(file_name, 'r') as f:
        return ''.join(f.readlines())


setup(
    name='cc2sf',
    version='0.0.1',
    author='Matthias Gilch',
    author_email='matthias.gilch.mg@gmail.com',
    license='GPLv2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
    description='C struct to python struct',
    long_description=read_file('README'),
    url='https://github.com/DaGuich/cc2sf',
    packages=find_packages(exclude=['contrib',
                                    'docs',
                                    'tests*']),
    python_requires='>=3'
)
