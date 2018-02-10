from setuptools import setup
setup(
    name="mini-kep-parsers",
    version="0.1",
    packages=[
        'parsers',
        'parsers.getter',
        'parsers.mover',
        'parsers.helper',
    ],
    install_requires=[
        'arrow',
        'pandas',
    ]
)
