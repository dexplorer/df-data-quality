import setuptools

setuptools.setup(
    name="dq_app",
    version="1.0.2",
    scripts=["./scripts/dq_app"],
    author="Rajakumaran Arivumani",
    description="DQ validation app install.",
    url="https://github.com/dexplorer/df-data-quality",
    packages=["dq_app"],
    # packages = find_packages(),
    install_requires=[
        "setuptools",
        "pandas >= 2.1.4",
        "numpy >= 1.26.4",
        "great-expectations==1.3.0",
        "requests",
        "utils@git+https://github.com/dexplorer/utils#egg=utils-1.0.3",
        "metadata@git+https://github.com/dexplorer/df-metadata#egg=metadata-1.0.9",
        "app_calendar@git+https://github.com/dexplorer/df-app-calendar#egg=app_calendar-1.0.2",
    ],
    python_requires=">=3.12",
)
