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
import common

class AboutDialog(SimpleGladeApp):
    def __init__(self):
        super(AboutDialog, self).__init__(common.datapath('about.glade'))


class PrefsDialog:
    def __init__(self,guakeInstance):
        super(PrefsDialog, self).__init__(common.datapath('prefs.glade'))


class Msgbox(object):
    """
    MSGBOX Class
    How to use:
        msgbox(type,message)
        
        types:
            0 => Information
            1 => Error
            2 => Confirmation
                Return true ou false
        message:
            string that support pango text markup
    """
    INFO = gtk.MESSAGE_INFO
    ERROR = gtk.MESSAGE_ERROR
    CONFIRM = gtk.MESSAGE_QUESTION

    def __init__(self, t=0, msg=''):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, t,
                gtk.BUTTONS_OK, msg)
        dialog.set_markup(text)
        r = dialog.run()
        dialog.destroy()
        return r
