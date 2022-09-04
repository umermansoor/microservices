from setuptools import find_packages, setup

setup(name="microservices",
      version = "0.1",
      description = "Example of Microservices using Flask",
      author = "Umer Mansoor",
      platforms = ["any"],
      license = "BSD",
      packages = find_packages(),
      install_requires = ["Flask==1.0", "requests==2.20.0", "wsgiref==0.1.2" ],
      )
