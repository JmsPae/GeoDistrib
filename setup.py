import setuptools

with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="GeoDistrib",
    version="0.1.0",
    author="James Pae",
    author_email="jameslind01@yahoo.co.uk",
    description="Tool for distributing zonal/cell statistics among contained features.",
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
)