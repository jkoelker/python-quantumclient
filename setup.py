from setuptools import setup, find_packages


version = '0.1'


setup(name='quantum.client',
      version=version,
      description="Quantum cli and pthon bindings",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Jason K\xc3\xb6lker',
      author_email='jason@koelker.net',
      url='',
      license='Apache 2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      quantum = quantum.cli.main:main
      """,
      )
