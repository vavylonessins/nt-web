"""
setup.py
"""

from setuptools import setup

setup(name='pyntweb',
      version='0.2.30',
      description='''
NTWeb - это экосистема компиляторов, которая планирует прийти на замену существующим в web стандартам: 
HTML, CSS, JS. На данный момент код на её языках переводится в традиционные языки web, так же 
традиционные языки нативно поддерживаются в самом коде

Посесите оффициальную группу проекта: https://t.me/+ft6pYhYcqtk3NDdi'''.replace("\n", ""),
      packages=['ntml', 'webfalco', 'ntcss'],
      license='GNU GPL 3.0',
      install_requires=['parglare', 'colorama'],
      author_email='talismanchet@vk.com',
      zip_safe=False)
