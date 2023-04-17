from setuptools import setup

setup(
    name='toolbox',
    version='0.1.0',
    py_modules=['toolbox-gpt'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'toolbox = toolbox:cli',
        ],
    },
)