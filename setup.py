from setuptools import setup

setup(name='convert360',
      version='0.1',
      description='Tool to convert 360 videos between different projections.',
      url='https://github.com/MateusZitelli/convert360',
      author='Mateus Zitelli',
      author_email='zitellimateus@gmail.com',
      license='GPLv3',
      packages=['convert360'],
      zip_safe=True,
      install_requires=[
          'imageio',
          'PyOpenGL',
          'PyOpenGL_Accelerate',
      ],
      scripts=['bin/convert360'])
