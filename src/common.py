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
import gtk, sys
import os
import locale
import gettext

locale_domain = 'guake'
locale_dir = './locale'

locale.setlocale(locale.LC_ALL,'')
gettext.bindtextdomain(locale_domain,locale_dir)
gettext.textdomain(locale_domain)
_ = gettext.gettext

def test_dbus(bus, interface):
    obj = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
    dbus_iface = dbus.Interface(obj, 'org.freedesktop.DBus')
    avail = dbus_iface.ListNames()
    return interface in avail

def std_visible(value):
    if not value:
        sys.stderr = open('/dev/null', 'w')
        sys.stdout = open('/dev/null', 'w')
    else:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

def datapath(x):
    f = os.path.abspath(os.path.join('..', 'data', x))
    if not os.path.exists(f):
        raise IOError('No sunch file or directory')
    return f

def hexify_color(c):
    h = lambda x: hex(x).replace('0x', '').zfill(4)
    return '#%s%s%s' % (h(c.red), h(c.green), h(c.blue))
