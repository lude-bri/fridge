from setuptools import setup, find_packages

setup(
  name="Fridge",
  version="0.1.0",
  description="App to help people organize their food inventory",
  author="Zedr0",
  # package_dir={"": "app"},
  # packages=find_packages(include=["app.*"]),
  # include_package_data=True,
  scripts=[
    "scripts/build.sh",
    "scripts/run.sh",
  ],
  install_requires=[
    "setuptools",
    "textual-dev",
    "requests",
    "requests_cache",
  ],
  extras_require={
    "dev": ["debugpy", "ruff"],
  },
)

