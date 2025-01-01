import setuptools

setuptools.setup(
    name="dq_app",
    version="1.0",
    scripts=["./scripts/dq_app"],
    author="Me",
    description="DQ validation app install.",
    packages=["dq_app", "dq_app.utils"],
    # packages = find_packages(),
    install_requires=[
        "setuptools",
        "pandas >= 2.1.4",
        "numpy >= 1.26.4",
        "great-expectations==1.3.0",
    ],
    python_requires=">=3.12",
)
