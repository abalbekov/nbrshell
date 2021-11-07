from setuptools import setup

setup(
    name="nbrshell",
    version="1",
    description='Set of Jupyter Notebook "cell magic" functions to remotely execute shell script typed in a notebook cell.',
    author="A.Balbekov",
    author_email="albert.y.balbekov@gmail.com",
    packages=["nbrshell"], # same as name
    install_requires=["paramiko"]    # external packages
)
