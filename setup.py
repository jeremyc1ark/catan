from setuptools import setup
setup(
   name='catan-emulator',
   version='1.0',
   description='Digital version of the board game Settlers of Catan',
   license="MIT",
   long_description=None,
   author='Jeremy Clark',
   author_email='shiblisa0@gmail.com',
   url="None",
   packages=['catan'],  #same as name
   install_requires=[
       'decorate_all_mehtods',
       'pytest'
   ], #external packages as dependencies
   scripts=[]
)
