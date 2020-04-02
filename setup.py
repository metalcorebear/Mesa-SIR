import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mesa_SIR",  # Replace with your own username
    version="0.0.2",
    author="Mark Bailey and Tom Pike",
    author_email="mark.mbailey@gmail.com",
    description="A Mesa extension for SIR models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metalcorebear/COVID-Agent-Based-Model",
    packages=setuptools.find_packages(),
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Life',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)
