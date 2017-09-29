from setuptools import setup
setup(
    name="mini-kep-parsers",
    version="0.1",
    packages=[
        'parsers',
        'parsers.getter'
    ],
    install_requires=[
        'arrow',
        'pandas',
    ]
)
