# -*- coding: utf-8; -*-
"""
Copyright (C) 2007 Gabriel Falcão <gabrielteratos@gmail.com>
Copyright (C) 2007 Lincoln de Sousa <lincoln@archlinux-br.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""
from distutils.core import setup, Extension
from commands import getoutput

# things to compile globalhotkeys module!
_libs = getoutput('pkg-config gtk+-2.0 pygobject-2.0 --libs').split()
_dirs = getoutput('pkg-config gtk+-2.0 pygobject-2.0 --cflags').split()
GTK_LIBS = [x.replace('-l', '') for x in _libs]
GTK_DIRS = [x.replace('-I', '') for x in _dirs]

module1 = Extension('globalhotkeys',
            define_macros=[('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0'),],
            include_dirs=GTK_DIRS,
            libraries=GTK_LIBS,
            sources=['src/globalhotkeys/eggaccelerators.c',
                'src/globalhotkeys/keybinder.c',
                'src/globalhotkeys/globalhotkeys.c'],
            extra_compile_args=['-O3'],)

setup(name='Guake',
      version='1.0',
      description='Guake terminal emulator for gnome',
      author=('Gabriel Falcão', 'Lincoln de Sousa'),
      author_email=('gabrielteratos@gmail.com', 'lincoln@archlinux-br.org'),
      license='GPL',
      url='http://guake-gnome-vte.sf.net',
      long_description = '''Guake is a quake style terminal emulator for gnome
desktop environment''',
      ext_modules = [module1])
