# execute 
# python -m build
# to build wheel
from setuptools import setup, find_packages

# Читаем зависимости из requirements.txt
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="csd_algo",
    version="0.0.1",
    packages=find_packages(),
    # py_modules=["client_axiliary", "generate_timeseries_numpy", 
    #             "models", "usage_example"],
    install_requires=install_requires,  # Передаем зависимости сборщику
    author="Andrei V. Keino",
    author_email='andreikeino@gmail.com'
    description="The web client for the Constant State Dectection in Timeseries algorithm webservice",
    python_requires=">=3.10",
)