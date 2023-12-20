from setuptools import setup

setup(name='clean_folder',
      version='0.2.1',
      description='https://github.com/Krom4rd/Krom4rd',
      author='Oleh Novosad',
      author_email='krom4rd@gmail.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.sort:terminal_starter']},
      packages=['usefull'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)


