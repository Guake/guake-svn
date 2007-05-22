#!/usr/bin/python
#-*- coding:utf-8 -*-

 
#        +-----------------------------------------------------------------------------+
#        | GPL                                                                         |
#        +-----------------------------------------------------------------------------+
#        | Copyright (c) Gabriel Falcao <gabrielteratos@gmail.com>                     |
#        |                                                                             |
#        | This program is free software; you can redistribute it and/or               |
#        | modify it under the terms of the GNU General Public License                 |
#        | as published by the Free Software Foundation; either version 2              |
#        | of the License, or (at your option) any later version.                      |
#        |                                                                             |
#        | This program is distributed in the hope that it will be useful,             |
#        | but WITHOUT ANY WARRANTY; without even the implied warranty of              |
#        | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               |
#        | GNU General Public License for more details.                                |
#        |                                                                             |
#        | You should have received a copy of the GNU General Public License           |
#        | along with this program; if not, write to the Free Software                 |
#        | Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. |
#        +-----------------------------------------------------------------------------+

try:
    import pygtk
    import gtk
    import gtk.glade
    from pango import FontDescription
    import time
except ImportError:
    print _('GuakeApplet need python-gtk support installed')
    sys.exit(1)


try:
    import vte
except ImportError:
    print _("Python-VTE module is required.\n")
    from Dialogs import msgbox
    msgbox(1,"Python-VTE module is required.")

    sys.exit(1)

from Dialogs import aboutDialog
from Dialogs import prefsDialog
import utils,common
from utils import prefs




