#!/usr/bin/env python
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
import pygtk
import gobject
pygtk.require('2.0')
gobject.threads_init()

import gtk
import vte
from pango import FontDescription
import gconf
import dbus

import os
import sys

import utils
import common
from common import _
from simplegladeapp import SimpleGladeApp
from statusicon import GuakeStatusIcon
import dbusiface
import globalhotkeys

SHELLS_FILE = '/etc/shells'
GCONF_PATH = '/apps/guake/'
GCONF_KEYS = GCONF_PATH + 'keybindings/'

GHOTKEYS = ((GCONF_KEYS+'global/show_hide', _('Toggle terminal visibility'),
                'F12'),)

LHOTKEYS = ((GCONF_KEYS+'local/new_tab', _('New tab'),),
            (GCONF_KEYS+'local/close_tab', _('Close tab')),
            (GCONF_KEYS+'local/previous_tab', _('Go to previous tab')),
            (GCONF_KEYS+'local/next_tab', _('Go to next tab'),))


class AboutDialog(SimpleGladeApp):
    def __init__(self):
        super(AboutDialog, self).__init__(common.datapath('about.glade'),
                root='aboutdialog')
        # the terminal window can be opened and the user *must* see this window
        self.get_widget('aboutdialog').set_keep_above(True)


class PrefsDialog(SimpleGladeApp):
    def __init__(self, guakeinstance):
        super(PrefsDialog, self).__init__(common.datapath('prefs.glade'),
                root='config-window')

        self.guake = guakeinstance
        self.client = gconf.client_get_default()

        # the first position in tree will store the keybinding path in gconf,
        # and the user doesn't worry with this, lest hide that =D
        model = gtk.TreeStore(str, str, str, bool)
        treeview = self.get_widget('treeview-keys')
        treeview.set_model(model)
        treeview.set_rules_hint(True)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('keypath', renderer, text=0)
        column.set_visible(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Action'), renderer, text=1)
        column.set_property('expand', True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_data('column', 1)
        renderer.connect('edited', self.on_key_edited, model)
        column = gtk.TreeViewColumn(_('Shortcut'), renderer, text=2,
                editable=3)
        column.set_property('expand', False)
        treeview.append_column(column)

        self.populate_shell_combo()
        self.populate_keys_tree()

        # getting values from gconf

        # shells list
        default = self.client.get_string(GCONF_PATH + 'general/default_shell')
        combo = self.get_widget('shells-combobox')
        model = combo.get_model()
        for i in model:
            value = model.get_value(i.iter, 0)
            if value == default:
                combo.set_active_iter(i.iter)

        # animate flag
        ac = self.client.get_bool(GCONF_PATH + 'general/window_animate')
        self.get_widget('animate-checkbutton').set_active(ac)

        # on top flag
        ac = self.client.get_bool(GCONF_PATH + 'general/window_ontop')
        self.get_widget('ontop-checkbutton').set_active(ac)

        # winsize
        val = self.client.get_int(GCONF_PATH + 'general/window_size')
        self.get_widget('winsize-hscale').set_value(val)

        # tab pos
        val = self.client.get_string(GCONF_PATH + 'general/tabpos')
        if val == 'bottom':
            self.get_widget('tabbottom-radiobutton').set_active(True)
        else:
            self.get_widget('tabtop-radiobutton').set_active(True)

        # font
        val = self.client.get_string(GCONF_PATH + 'style/font/style')
        self.get_widget('fontbutton').set_font_name(val)

        val = self.client.get_string(GCONF_PATH + 'style/font/color')
        try:
            color = gtk.gdk.color_parse(val)
            self.get_widget('font-colorbutton').set_color(color)
        except (ValueError, TypeError):
            # unable to parse color
            pass

        # background
        val = self.client.get_string(GCONF_PATH+'style/background/color')
        try:
            color = gtk.gdk.color_parse(val)
            self.get_widget('bg-colorbutton').set_color(color)
        except (ValueError, TypeError):
            # unable to parse color
            pass

        val = self.client.get_string(GCONF_PATH+'style/background/image')
        self.get_widget('bgimage-filechooserbutton').set_filename(val)

        val = self.client.get_int(GCONF_PATH+'style/background/transparency')
        self.get_widget('transparency-hscale').set_value(val)

        # the terminal window can be opened and the user *must* see this window
        self.get_widget('config-window').set_keep_above(True)

    # -- populate functions --

    def populate_shell_combo(self):
        cb = self.get_widget('shells-combobox')
        if os.path.exists(SHELLS_FILE):
            lines = open(SHELLS_FILE).readlines()
            for i in lines:
                possible = i.strip()
                if possible and not possible.startswith('#'):
                    cb.append_text(possible)
        cb.append_text(sys.executable)

    def populate_keys_tree(self):
        model = self.get_widget('treeview-keys').get_model()

        giter = model.append(None)
        model.set(giter, 0, '', 1, _('Global hotkeys'))

        for i in GHOTKEYS:
            child = model.append(giter)
            hotkey = self.client.get_string(i[0])
            model.set(child,
                    0, i[0],
                    1, i[1],
                    2, hotkey,
                    3, True)

        giter = model.append(None)
        model.set(giter, 0, '', 1, _('Local hotkeys'))

        for i in LHOTKEYS:
            child = model.append(giter)
            hotkey = self.client.get_string(i[0])
            model.set(child,
                    0, i[0],
                    1, i[1],
                    2, hotkey,
                    3, True)

        self.get_widget('treeview-keys').expand_all()

    # -- callbacks --

    def on_shells_combobox_changed(self, combo):
        citer = combo.get_active_iter()
        if not citer:
            return
        shell = combo.get_model().get_value(citer, 0)
        self.client.set_string(GCONF_PATH + 'general/default_shell', shell)

    def on_animate_checkbutton_toggled(self, bnt):
        self.client.set_bool(GCONF_PATH + 'general/window_animate',
                bnt.get_active())

    def on_ontop_checkbutton_toggled(self, bnt):
        self.client.set_bool(GCONF_PATH + 'general/window_ontop',
                bnt.get_active())

    def on_winsize_hscale_value_changed(self, hscale):
        val = hscale.get_value()
        self.client.set_int(GCONF_PATH + 'general/window_size', int(val))

    def on_tabbottom_radiobutton_toggled(self, bnt):
        st = bnt.get_active() and 'bottom' or 'top'
        self.client.set_string(GCONF_PATH + 'general/tabpos', st)
        self.guake.set_tabpos()

    def on_tabtop_radiobutton_toggled(self, bnt):
        st = bnt.get_active() and 'top' or 'bottom'
        self.client.set_string(GCONF_PATH + 'general/tabpos', st)
        self.guake.set_tabpos()

    def on_fontbutton_font_set(self, fb):
        self.client.set_string(GCONF_PATH + 'style/font/style',
                fb.get_font_name())
        self.guake.set_font()

    def on_font_colorbutton_color_set(self, bnt):
        c = common.hexify_color(bnt.get_color())
        self.client.set_string(GCONF_PATH + 'style/font/color', c)
        self.guake.set_fgcolor()

    def on_bg_colorbutton_color_set(self, bnt):
        c = common.hexify_color(bnt.get_color())
        self.client.set_string(GCONF_PATH + 'style/background/color', c)
        self.guake.set_bgcolor()

    def on_bgimage_filechooserbutton_selection_changed(self, bnt):
        files = bnt.get_filenames()
        if files:
            self.client.set_string(GCONF_PATH + 'style/background/image',
                    files[0])
            self.guake.set_bgimage()

    def on_transparency_hscale_value_changed(self, hscale):
        val = hscale.get_value()
        self.client.set_int(GCONF_PATH + 'style/background/transparency',
                int(val))
        self.guake.set_alpha()

    def on_key_edited(self, renderer, path, key, model):
        giter = model.get_iter(path)
        gconf_path = model.get_value(giter, 0)
        model.set(giter, 2, key)
        self.client.set_string(gconf_path, key)


class Guake(SimpleGladeApp):
    def __init__(self):
        super(Guake, self).__init__(common.datapath('guake.glade'))
        self.client = gconf.client_get_default()

        # setting global hotkey!
        globalhotkeys.init()
        key = self.client.get_string(GHOTKEYS[0][0])
        globalhotkeys.bind(key, self.show_hide)

        # trayicon!
        tray_icon = GuakeStatusIcon()
        tray_icon.connect('popup-menu', self.show_menu)
        tray_icon.connect('activate', self.show_hide)
        tray_icon.show_all()

        self.window = self.get_widget('window-root')
        self.notebook = self.get_widget('notebook-teminals')
        self.toolbar = self.get_widget('toolbar')
        self.mainframe = self.get_widget('mainframe')

        self.window.set_keep_above(True)
        self.window.set_geometry_hints(min_width=1, min_height=1)

        self.term_list = []

        self.getScreenSize()
        self.visible = False

        self.addTerm()

    def show_menu(self, *args):
        menu = self.get_widget('tray-menu')
        menu.popup(None, None, None, 3, gtk.get_current_event_time())

    def show_hide(self, *args):
        screen = self.window.get_screen()
        w, h = screen.get_width(), screen.get_height()
        if not self.visible:
            self.show(w, h)
            self.setTerminalFocus()
        else:
            self.hide()

    def show(self, wwidth, hheight):
        self.getScreenSize()
        self.window.set_position(gtk.WIN_POS_NONE)
        self.window.set_gravity(gtk.gdk.GRAVITY_NORTH)
        self.window.move(gtk.gdk.screen_width() / 2, 0)
        self.visible = True
        self.window.show_all()
        self.window.stick()
        self.setOnTop(self.ON_TOP)
        self.window.set_resizable(True)
        self.animateShow()

        if not self.term_list:
            self.addTerm()

    def hide(self):
        self.animateHide()
        self.window.hide_all()
        self.window.unstick()
        self.visible = False

    def load_config(self):
        self.configs = utils.prefs()

        self.set_fgcolor()
        self.set_font()
        self.set_bgcolor()
        self.set_bgimage()
        self.set_alpha()
        self.set_tabpos()

        self.fullscreen = False
        try:
            self.use_animation = bool(self.configs.general.animate)
        except:
            self.use_animation =True

        proportion=float(self.configs.general.height)
        self.setAnimationProportions(proportion,100)
        self.ON_TOP=bool(self.configs.terminal.ontop)

    def setDefaultSize(self,userWidth,userHeight):
        self.desiredWidth=userWidth
        self.desiredHeight=userHeight
        
    def setOnTop(self,bool_value):
        self.ON_TOP=bool_value
        self.window.set_keep_above(bool(bool_value))
        if bool_value:
            self.window.stick()
        else:
            self.window.unstick()

    def setAnimationProportions(self, percent, calcValue=100, shownow=False):
        self.getScreenSize()
        self.divisionFactor=int((self.desiredHeight*percent)/calcValue)
        self.multiplyFactor=int(calcValue)
        self.window.set_size_request(self.desiredWidth, 1)

        if percent==1:
            self.fullscreen = True
        else:
            self.fullscreen = False

        while self.divisionFactor < 3:
            self.setAnimationProportions(percent + 0.1)

        if shownow:
            self.animateShow()

    def resize(self, width,height):
        self.getScreenSize()
        self.window.set_resizable(True)
        self.window.resize(width,height)
        self.window.set_default_size(width,height)

    def animateShow(self, *args):
        if not self.use_animation:
            self.use_animation = True

        if self.use_animation:
            self.resize(self.desiredWidth,1)
            for i in range(1, int(self.divisionFactor)):
                self.resize(self.desiredWidth, i * self.multiplyFactor)
                utils.updateUI()

            if self.fullscreen:
                self.getScreenSize()
                self.resize(self.desiredWidth,int(self.height))
                utils.updateUI()
        else:
            self.resize(self.desiredWidth,int(self.divisionFactor)*self.multiplyFactor)

    def animateHide(self,*args):
        if self.use_animation==True:
            l = range(1, int(self.divisionFactor))
            if self.fullscreen==True:
                self.getScreenSize()
                self.resize(self.desiredWidth,self.height)
            else:
                self.resize(self.desiredWidth, l[-1])
                
            for giter in reversed(l):
                self.resize(self.desiredWidth, giter*100)
                utils.updateUI()

    def getScreenSize(self):
        self.height = self.window.get_screen().get_height()
        self.width = self.window.get_screen().get_width()
        self.setDefaultSize(self.width,self.height)

    def determineTabsVisibility(self):
        if self.notebook.get_n_pages() == 1:
            self.notebook.set_show_tabs(False)
        else:
            self.notebook.set_show_tabs(True)

    # -- format functions --

    def set_bgcolor(self):
        color = self.client.get_string(GCONF_PATH+'style/background/color')
        bgcolor = gtk.gdk.color_parse(color)
        for i in self.term_list:
            i.set_color_background(bgcolor)
            i.set_background_tint_color(bgcolor)

    def set_bgimage(self):
        image = self.client.get_string(GCONF_PATH+'style/background/image')
        if image and os.path.exists(image):
            for i in self.term_list:
                i.set_background_image_file(image)

    def set_fgcolor(self):
        color = self.client.get_string(GCONF_PATH+'style/font/color')
        fgcolor = gtk.gdk.color_parse(color)
        for i in self.term_list:
            i.set_color_dim(fgcolor)
            i.set_color_cursor(fgcolor)
            i.set_color_highlight(fgcolor)
            i.set_color_foreground(fgcolor)

    def set_font(self):
        font_name = self.client.get_string(GCONF_PATH+'style/font/style')
        font = FontDescription(font_name)
        for i in self.term_list:
            i.set_font(font)

    def set_alpha(self):
        alpha = self.client.get_int(GCONF_PATH+'style/background/transparency')
        for i in self.term_list:
            i.set_background_transparent(bool(alpha))
            i.set_background_saturation(alpha / 100.0)

    def set_tabpos(self):
        pos = self.client.get_string(GCONF_PATH+'general/tabpos')
        if pos == 'bottom':
            self.mainframe.reorder_child(self.notebook, 0)
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)
        else:
            self.mainframe.reorder_child(self.notebook, 1)
            self.notebook.set_tab_pos(gtk.POS_TOP)
           
    # -- callbacks --

    def on_prefs_menuitem_activate(self, *args):
        PrefsDialog(self)

    def on_about_menuitem_activate(self, *args):
        AboutDialog()

    def on_add_button_clicked(self, *args):
        self.addTerm()

    def on_terminal_exited(self, widget):
        self.deletePage(self.notebook.page_num(widget))

    def on_close_button_close_clicked(self, widget, index):
        self.deletePage(self.notebook.page_num(self.term_list[index]))
        self.setTerminalFocus()

    # -- misc functions --

    def addTerm(self):
        LastPos = self.notebook.get_n_pages()
        self.term_list.append(vte.Terminal())

        self.term_list[LastPos].show()
        self.term_list[LastPos].set_emulation('xterm')

        # TODO: make new terminal opens in the same dir of the already in use.
        shell_name = self.client.get_string(GCONF_PATH+'general/default_shell')
        self.term_list[LastPos].fork_command(shell_name,
                directory=os.path.expanduser('~'))

        image = gtk.Image()
        image.set_from_file(common.datapath('close.svg'))
        
        label = gtk.Label('Terminal %s' % (LastPos+1))
        label.connect('button-press-event', self.setTerminalFocus)

        button = gtk.Button()
        button.set_image(image)
        button.set_relief(gtk.RELIEF_NONE)
        button.connect('clicked', self.on_close_button_close_clicked, LastPos)

        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(1)
        hbox.pack_start(label)
        hbox.pack_start(button)
        hbox.show_all()

        self.term_list[LastPos].set_flags(gtk.CAN_DEFAULT)
        self.term_list[LastPos].set_flags(gtk.CAN_FOCUS)
        self.term_list[LastPos].connect('child-exited',
                self.on_terminal_exited)
        self.term_list[LastPos].grab_focus()
        
        self.notebook.append_page(self.term_list[LastPos], hbox)
        self.notebook.set_current_page(LastPos)
        self.notebook.connect('focus-tab',self.setTerminalFocus)
        self.notebook.connect('select-page',self.setTerminalFocus)
        self.determineTabsVisibility()
        self.load_config()

    def setTerminalFocus(self, *args):
        self.term_list[-1].grab_focus()

    def deletePage(self, pagepos):
        self.term_list.pop(pagepos)
        self.notebook.remove_page(pagepos)
        self.determineTabsVisibility()
        if not self.term_list:
            self.hide()


def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-s', '--show-hide', dest='show_hide',
            action='store_true', default=False,
            help=_('Toggles the visibility of the terminal window'))

    parser.add_option('-p', '--preferences', dest='show_preferences',
            action='store_true', default=False,
            help=_('Shows Guake preference window'))

    parser.add_option('-a', '--about', dest='show_about',
            action='store_true', default=False,
            help=_('Shows Guake\'s about info'))

    parser.add_option('-q', '--quit', dest='quit',
            action='store_true', default=False,
            help=_('Says to Guake go away =('))

    options, args = parser.parse_args()

    if options.show_hide:
        # do the show/hide!
        pass

    if options.show_preferences:
        # shows preference window
        pass

    if options.show_about:
        # shows about window
        pass

    if options.quit:
        # go away!
        pass

if __name__ == '__main__':
    main()
    Guake().run()
