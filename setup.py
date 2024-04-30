from setuptools import setup

setup(name='configclass',
      version='0.1',
      description='A simple configuration class for Python',
      #url='http://ictshore.com/',
      author='Terrasque',
      package_dir={"": "src"},
      author_email='terrasque@thelazy.net',
      license='MIT',
      packages=['configclass'],
      install_requires=["dacite"],
      zip_safe=False)