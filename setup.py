from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as fp:
        return [line[:-1] for line in fp]
    return []


setup(
    name='brand_car_scraper',
    version='1.0.0',
    author='Pedro Uceda and Pablo Campillo',
    author_email='',
    packages=find_packages(where='.'),
    scripts=[
        'bin/scrap',
    ],
    data_files=[
    ],
    url='https://github.com/pablo-campillo/brand_car_scraper',
    license='LICENSE',
    description='A package for monitoring pig activity by computer vision',
    long_description=open('README.md').read(),
    install_requires=get_requirements(),
)
