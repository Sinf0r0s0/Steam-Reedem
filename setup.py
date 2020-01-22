import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="steamreedem",
    version="0.0.1",
    author="Sinf0r0s0",
    author_email="noteprof213@gmail.com",
    description="Automates the Steam key redeem process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/Sinf0r0s0/Steam-Reedem",
    packages=['steamreedem'],
    install_requires=['requests', 'pycryptodome'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
