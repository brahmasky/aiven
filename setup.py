from setuptools import setup

setup(name='myAiven',
      version='0.1',
      description='First project with Aiven',
      url='https://github.com/brahmasky/aiven_homework',
      author='Paco Luo',
      author_email='paco.luo@gmail.com',
      license='MIT',
      packages=['myAiven'],
      # zip_safe=False
      install_requires=[
       "requests",
       "kafka-python",
       "psycopg2-binary",
       "bcrypt",
      ],      
    )
