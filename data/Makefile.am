@INTLTOOL_XML_RULE@
@INTLTOOL_DESKTOP_RULE@

uidir = $(datadir)/guake
ui_DATA = \
	about.glade \
	guake.glade \
	prefs.glade

pixmapsdir = $(datadir)/pixmaps/guake
pixmaps_DATA = \
	close.svg \
	guake.svg \
	left_in.svg \
	littleguakelogo.svg \
	statusicon_out.png \
	tabup.svg \
	down_in.svg \
	guake.png \
	guakeabt.png \
	left_normal.svg \
	new_guakelogo.png \
	right_in.svg \
	statusicon_over.png \
	up_in.svg \
	addTerm.svg \
	down_normal.svg \
	guakelogo.svg \
	littleguakelogo.png \
	no-pil.png \
	right_normal.svg \
	tabdown.svg \
	up_normal.svg


# .desktop file
Multimediadir = $(datadir)/applications
Multimedia_in_files = guake.desktop
Multimedia_DATA = $(Multimedia_in_files:.desktop.in=.desktop)

# dbus service file
servicedir = $(datadir)/dbus-1/services
service_in_files = org.gnome.Guake.service.in
service_DATA = $(service_in_files:.service.in=.service)

# schema file.
# not using GCONF_SCHEMA_FILE_DIR because it is
# sending our schemafile to /usr dir =/
schemadir = $(sysconfdir)/gconf/schemas
schema_DATA = guake.schemas

if GCONF_SCHEMAS_INSTALL
install-data-local: $(schema_DATA)
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) $(GCONFTOOL) --makefile-install-rule $(srcdir)/$(schema_DATA);
endif

EXTRA_DIST = $(ui_DATA) \
			 $(pixmaps_DATA) \
			 $(schema_DATA) \
			 guake.desktop.in

