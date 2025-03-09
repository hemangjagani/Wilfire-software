from setuptools import setup

APP = ['app.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['requests', 'folium', 'geopy']
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
