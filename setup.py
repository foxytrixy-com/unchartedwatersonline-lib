import setuptools
from version import __version__

setuptools.setup(
    name="unchartedwatersonline-lib",
    version=__version__,
    author="yerihyo",
    author_email="yerihyo@gmail.com",
    description="UWO price image reader",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/foxytrixy-com/unchartedwatersonline-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Windows",
    ],
)
