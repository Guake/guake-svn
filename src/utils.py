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
import datetime
import time
import sys, os, ConfigParser
import gobject
import dbus
import dbus.service
import dbus.glib
import gtk
import locale
locale.setlocale(locale.LC_ALL, '')

import common


import locale,gettext

locale_domain = 'guake'
locale_dir = './locale'

locale.setlocale(locale.LC_ALL,'')
gettext.bindtextdomain(locale_domain,locale_dir)
gettext.textdomain(locale_domain)
_ = gettext.gettext

class prefs:
    def __init__(self):
        self.home = os.path.expanduser("~")
        if not self.home.endswith("/"):
            self.home += "/.config/"
        if not os.path.exists(self.home):
            os.mkdir(self.home)
        self.configFile = self.home + "guake-terminal.conf"  
        self.configuration = ConfigParser.ConfigParser()
        if not os.path.exists(self.configFile):
            self._create_new()
        self.terminal = Terminal(self)
        self.general = General(self)

    def _create_new(self):
        self.terminal = Terminal(self)
        self.general = General(self)
        
        self.terminal.shell = property(self.terminal.get_shell,self.terminal.set_shell)
        self.configuration.add_section("terminal")
        self.terminal.set_shell(0)
        self.terminal.set_fontstyle("DejaVu Sans Mono 10")
        self.terminal.set_fontcolor("#FFFFFF")
        self.terminal.set_bgimage("")
        self.terminal.set_bgcolor("#000000")
        self.terminal.set_transparent(1)
        self.terminal.set_alpha(50)
        self.terminal.set_ontop(True)
        self.configuration.add_section("general")
        self.general.set_animate(1)
        self.general.set_tabsplace(0)
        self.general.set_height(50)
        self.general.set_key("F12")

    def write(self,section=None,key=None,value=None):
        self.configuration.set(section, key, value)
        try:
            fopen = open(self.configFile,"w")
            self.configuration.write(fopen)
            fopen.close()
            ##print section,key,value
            return True
        except:
            return False
            
    def read(self,section=None,key=None):
        try:
            try:
                self.configuration.read(self.configFile)
                return self.configuration.get(section,key)
            except:
                self._create_new()
        except:
            return False
        
class Terminal:
    def __init__(self,installer):
        self.parent = installer

    def get_shell(self):
        return str(self.parent.read("terminal", "shell")).strip()

    def set_shell(self,shells):
        try:
            self.parent.write("terminal", "shell",int(shells))
            return True
        except:
            return False
    shell = property(get_shell, set_shell)

    def get_fontstyle(self):
        return str(self.parent.read("terminal", "fontstyle"))

    def set_fontstyle(self,fontstyle):
        try:
            self.parent.write("terminal", "fontstyle",str(fontstyle))
            return True
        except:
            return False            
    fontstyle = property(get_fontstyle,set_fontstyle)
    def get_fontcolor(self):
        return str(self.parent.read("terminal", "fontcolor"))
    def set_fontcolor(self,fontcolor):
        try:
            self.parent.write("terminal", "fontcolor",str(fontcolor))
            return True
        except:
            return False            
    fontcolor = property(get_fontcolor,set_fontcolor)

    ###########################################################################
    def get_bgimage(self):
        return str(self.parent.read("terminal", "bgimage"))
    def set_bgimage(self,bgimage):
        try:
            self.parent.write("terminal", "bgimage",str(bgimage))
            return True
        except:
            return False            
    bgimage = property(get_bgimage,set_bgimage)
    ###########################################################################
    def get_bgcolor(self):
        return str(self.parent.read("terminal", "bgcolor"))
    def set_bgcolor(self,bgcolor):
        try:
            self.parent.write("terminal", "bgcolor",str(bgcolor))
            return True
        except:
            return False                
    bgcolor = property(get_bgcolor,set_bgcolor)
    ###########################################################################
    def get_transparent(self):
        return int(self.parent.read("terminal", "transparent"))
    def set_transparent(self,transparent):
        try:
            self.parent.write("terminal", "transparent",int(transparent))
            return True
        except:
            return False            
    transparent = property(get_transparent,set_transparent)
    ###########################################################################
    def get_alpha(self):
        return float(self.parent.read("terminal", "alpha")) /100
    def set_alpha(self,alpha):
        try:
            self.parent.write("terminal", "alpha",int(alpha))
            return True
        except:
            return False            
    alpha = property(get_alpha,set_alpha)
    ###########################################################################
    def get_ontop(self):
        return int(self.parent.read("terminal", "ontop")) 
    def set_ontop(self,ontop):
        try:
            self.parent.write("terminal", "ontop",int(ontop))
            return True
        except:
            return False            
    ontop = property(get_ontop,set_ontop)
    ###########################################################################

class General:
    def __init__(self,installer):
        self.parent = installer   
    ##########################################################################
    def get_animate(self):
        return int(self.parent.read("general", "animate"))
    def set_animate(self,animate):
        try:
            self.parent.write("general", "animate",int(animate))
            return True
        except:
            return False
    animate = property(get_animate,set_animate)
    ###########################################################################
    def get_tabsplace(self):
        return int(self.parent.read("general", "tabsplace"))
    def set_tabsplace(self,tabsplace):
        try:
            self.parent.write("general", "tabsplace",int(tabsplace))
            return True
        except:
            return False
    tabsplace = property(get_tabsplace,set_tabsplace)
    ###########################################################################    
    def get_height(self):
        return float(self.parent.read("general", "height")) /100
    def set_height(self,height):
        try:
            self.parent.write("general", "height",float(height))
            return True
        except:
            return False            
    height = property(get_height,set_height)
    ###########################################################################    
    def get_key(self):
        return str(self.parent.read("general", "key")) 
    def set_key(self,key):
        try:
            self.parent.write("general", "key",str(key))
            return True
        except:
            return False            
    key = property(get_key,set_key)
    ###########################################################################        
def forceExit():
    try:
        import gc
        gc.collect()
        gtk.main_quit()
        sys.exit(1)
    except:
        pass    

class guakeDBUS:
    def __init__(self,args):
        self.bus = dbus.SessionBus()
        self.args=args

    def test_dbus(self,bus, interface):
        obj = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        remote_object = bus.get_object("org.gnome.Guake.DBUS","/org/gnome/Guake/DBUS")##"/DaemonDBus")
        self.iface = dbus.Interface(remote_object, "org.gnome.Guake.DBUS")
        dbus_iface = dbus.Interface(obj, 'org.freedesktop.DBus')
        avail = dbus_iface.ListNames()
        return interface in avail

    def isRunning(self):
        try:
            if self.test_dbus(self.bus, 'org.gnome.Guake.DBUS'):
                print _('Guake is already running...')
                import time
                if "--showhide" in self.args:
                    self.iface.show_hide()
                elif "--preferences" in self.args:
                    self.iface.show_prefs()
                elif "--about" in self.args:
                    self.iface.show_about()
                elif "--quit" in self.args:
                    self.iface.exitGuake()
                else:
                    forceExit()
                return True 
        except dbus.DBusException, e:
            print e
            forceExit()
            
    def killGuake(self):
        if self.isRunning() == True:
            try:
                self.iface.quit()
                del self.iface
                del self
            except:
                pass
            
class user:
    preferences=prefs()

import gconf

def AddGconfKey():
    entry = gconf.client_get_default()
    metacity_keycommand = "/apps/metacity/keybinding_commands/command_12"
    metacity_keybind = "/apps/metacity/global_keybindings/run_command_12"
    oldKeycommand12 = entry.get_string(metacity_keycommand)
    oldkeybind12 = entry.get_string(metacity_keybind)
    entry.set_string(metacity_keycommand,"python %s --showhide"%common.APP_PY)
    entry.set_string(metacity_keybind,user.preferences.general.key)
    return (metacity_keybind,metacity_keycommand)

def restoreGconfKeys(oldkey,oldcommand):
    entry = gconf.client_get_default()
    metacity_keycommand = "/apps/metacity/keybinding_commands/command_12"
    metacity_keybind = "/apps/metacity/global_keybindings/run_command_12"
    entry.set_string(metacity_keycommand,oldcommand)
    entry.set_string(metacity_keybind,oldkey)
    return True

def updateUI():
    time.sleep(0.0000000000000001)
    while gtk.events_pending(): gtk.main_iteration()
