import io
import os

from setuptools import find_packages, setup


# Package meta-data.
NAME = 'gotify-tray'
DESCRIPTION = 'A tray notification application for receiving messages from a Gotify server.'
URL = 'https://github.com/seird/gotify-tray'
EMAIL = "k.dries@protonmail.com"
REQUIRES_PYTHON = '>=3.8.0'
with open("version.txt", "r") as f:
    VERSION = f.read()

# What packages are required for this module to be executed?
REQUIRED = [
    'requests', 'PyQt6', 'websocket-client', 'python-dateutil'
]

# What packages are optional?
EXTRAS = {
    # 'socks5 proxy': ['pysocks'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=EMAIL,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    # packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    packages=find_packages(),
    package_data={
        'gotify_tray.gui.images': ['*.ico', '*.png'],
        'gotify_tray.gui.themes.default': ['*.qss', '*.svg', '*.png'],
        'gotify_tray.gui.themes.dark_purple': ['*.qss', '*.svg', '*.png'],
        'gotify_tray.gui.themes.light_purple': ['*.qss', '*.svg', '*.png'],
    },
    data_files = [
    ],

    entry_points={
        'console_scripts': ['gotify-tray=gotify_tray.__main__:main'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)
