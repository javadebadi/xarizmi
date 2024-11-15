# Import required functions
from pathlib import Path

from setuptools import find_packages, setup

import xarizmi

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


# Call setup function
setup(
    author="Javad Ebadi",
    author_email="javad@javadebadi.com",
    description=(
        "Xarizmi (read Khwarizmi) project is an educational project that"
        "contains tools for technical analysis in Python."
    ),
    name="xarizmi",
    packages=find_packages(include=["xarizmi", "xarizmi.*"]),
    version=xarizmi.__version__,
    install_requires=[
        "pydantic==2.7.0",
        "scipy>=1.13.1",
        "numpy~=1.24",
        "mplfinance",
        "matplotlib",
        "yfinance~=0.2",
        "TA-Lib",
    ],
    python_requires=">=3.11",
    license="Apache 2.0",
    url="https://github.com/javadebadi/xarizmi",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
