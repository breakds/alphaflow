from setuptools import setup, find_packages

setup(
    name='alphaflow',
    version='0.1.0',
    description='A minimalist computation graph based pipeline system in python',
    author='Break Yang',
    author_email='breakds@gmail.com',
    # find_package() without any arguments will serach the same
    # directory as the setup.py for modules and packages.
    packages=find_packages(),
    include_package_data=True,
    entry_points={},
    python_requires='>=3.6',
)
