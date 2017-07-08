from setuptools import setup

setup(name='convert360',
      version='0.1.2',
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
          # 'PyOpenGL_Accelerate==3.0.2',
          'tqdm'
      ],
      scripts=['bin/convert360'])
