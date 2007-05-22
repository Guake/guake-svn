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
#######################       TODO      ###########################
##do the applet show/hide each instance of guake-window, else limit only one applet to be added
##Save/load preferences of user
##Poder exibir animação do guake tanto em TOP quanto em BOTTON, de preferencia right and left too
##Criar gtk.HScroll para determinar a porcentagemd e comprimento do guake pela tela.
##Adicionar Checkbox na janela main para determinar se guake fica acida das outras janelas ou não.
##Zerar o gtk.Image() do Prefiew na janela de Preferencias quando nao tiver nehuma rquivo selecionado
##permitir copiar/colar no terminal a partir de menu de contexto
import pygtk
import sys,os
pygtk.require('2.0')
import gc
import gtk,egg
import gnomeapplet
from main import guakeWin
import locale,gettext
import common
locale_domain = 'guake'
locale_dir = './locale'

locale.setlocale(locale.LC_ALL,'')
gettext.bindtextdomain(locale_domain,locale_dir)
gettext.textdomain(locale_domain)
_ = gettext.gettext

class guakeMain:
    def __init__(self):
        self.widgetTree = gtk.glade.XML(common.APP_DIR + 'glade/guake.glade')
        self.TrayMenu = self.widgetTree.get_widget('trayMenu')
        ##Menus:
        self.mnuShowHide = self.widgetTree.get_widget('mnuShowHide')
        self.mnuShowHide.connect("activate",self.show_hide)
        self.mnuPrefs = self.widgetTree.get_widget('mnuPrefs')
        self.mnuPrefs.connect("activate",self.showPrefs)
        self.mnuAbout = self.widgetTree.get_widget('mnuAbout')
        self.mnuAbout.connect("activate",self.showAbout)
        self.mnuQuit = self.widgetTree.get_widget('mnuQuit')
        self.mnuQuit.connect("activate",self.quit)
        self.win=guakeWin(self)
        self.abtDialog=""
        self.appletID=0
        self.visible=False
        try:
            self.tray = gtk.StatusIcon()
            self.trayStyle = 'gtk'
        except:
            from egg import trayicon
            self.tray = trayicon.TrayIcon(common.APP_NAME)
            self.trayStyle = 'egg'   
            
        if self.trayStyle == 'gtk':
            self.tray.set_from_file(common.APP_ICON)
            self.tray.set_tooltip(common.APP_NAME)
            self.tray.connect("popup-menu", self.show_menu, None)
            self.tray.connect("activate", self.show_hide, None)            
        elif self.trayStyle == 'egg':
            self._trayimage = gtk.Image()
            self._trayimage.set_from_file(common.APP_ICON)          
            
            _eventbox = gtk.EventBox()  
            _eventbox.add(self._trayimage)
            self.tray.connect("enter-notify-event",self.mouseOver)
            self.tray.connect("leave-notify-event",self.mouseOut)
            self.tray.connect("button-press-event",self.eggClickInterface)
            self.tray.add(_eventbox)        
            self.tray.show_all()    
    def mouseOver(self,*args):
        if self.trayStyle == 'gtk':
            self.tray.set_from_file(common.APP_ICON_OVER)
        elif self.trayStyle == 'egg':
            self._trayimage.set_from_file(common.APP_ICON_OVER)  
    def mouseOut(self,*args):
        if self.trayStyle == 'gtk':
            self.tray.set_from_file(common.APP_ICON)
        elif self.trayStyle == 'egg':
            self._trayimage.set_from_file(common.APP_ICON)  
    def eggClickInterface(self,tray,mouse):
        #todo: what happen if user swap the buttons? (right to left and left to right)
        #will need a method to detect user mouse preferences and swap mouse.button ==2 ?
        print "Mouse button %d clicked:"%mouse.button
        
        if mouse.button==1:
            self.show_hide(tray)
        elif mouse.button==3:
            self.show_menu(status_icon=tray,button=mouse.button,activate_time=mouse.time)

    def show_hide(self, *args):
        """ Show and Hide the main window. """
        self.tela = self.win.window.get_screen()
        if self.visible == False:
            self.win.show(self.tela.get_width(),self.tela.get_height())
            self.visible=True
        else:
            self.win.hide()
            self.visible=False
        
    def show_menu(self, status_icon, button, activate_time, arg0=None):
        self.TrayMenu.popup(None, None, None, button, activate_time)
        
    def __menuBuilder(self):
        pass

    def showPrefs(self,*args):
        self.win.showPrefs(self.win.prefDialog)
    def showAbout(self,*args):
        self.win.showAbout(self.win.abtDialog)
    def showWindow(self):
        self.tela=self.win.window.get_screen()
        if (self.orient == 0 or self.orient == 1):
            self.wwidth =self.tela.get_width()
            self.wheight =self.tela.get_height()
        elif (self.orient == 2 or self.orient == 3):
            self.wwidth =self.tela.get_height()
            self.wheight =self.tela.get_width()
        self.win.show(self.wwidth,self.wheight)
        self.set_widgets()
    def quit(self,*args):
        common.saveSession()
        sys.exit(0)
guakeMain()
gtk.main()
