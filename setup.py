from setuptools import find_packages, setup

setup(name="microservices",
      version = "0.1",
      description = "Example of Microservices using Flask",
      author = "Umer Mansoor",
      platforms = ["any"],
      license = "BSD",
      packages = find_packages(),
      install_requires = ["Flask==0.10.1", "requests==2.5.1", "wsgiref==0.1.2" ],
      )
