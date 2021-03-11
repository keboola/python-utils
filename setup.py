import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

project_urls = {
    'Documentation': 'https://htmlpreview.github.io/?https://raw.githubusercontent.com/keboola/'
                     'python-utils/main/docs/api-html/utils/date.html'
}

setuptools.setup(
    name="keboola.utils",
    version="1.0.1",
    author="Keboola KDS Team",
    project_urls=project_urls,
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    install_requires=[
        'dateparser',
        'pytz'
    ],
    author_email="support@keboola.com",
    description="General utility library for Python applications running in Keboola Connection environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keboola/python-utils",
    packages=['keboola.utils'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.7'
)
