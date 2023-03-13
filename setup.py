from setuptools import setup, find_namespace_packages


setup(
    name="clean_folder",
    version="0.0.1",
    description="Folder cleaner",
    author="Yaroslav",
    author_email="fenixm22@gmail.com",
    url="https://github.com/kubitskyi/goit_folder_cleane_2.git",
    license="MIT",
    classifiers=[
        "Programming Launguage :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operatinf System :: OS Independent",],
    packages=find_namespace_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['clean_folder = folder_cleaner.main:main']}
)