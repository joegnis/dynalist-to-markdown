import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dynalist-to-md-joegnis",
    version="0.0.1",
    author="joegnis",
    author_email="joegnis@users.noreply.github.com",
    description=
    "A tool that converts text exported from Dynalist into Markdown text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joegnis/dynalist-to-markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
