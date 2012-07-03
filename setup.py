try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='django-daterange-filter',
    version='0.0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Django",
        "South",
    ],
    packages= find_packages(),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    entry_points="""
""",
)
