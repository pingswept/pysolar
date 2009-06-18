#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import horizon

class Base:

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)

        self.top_level_hbox = gtk.HBox()
        self.button_column = gtk.VButtonBox()
        self.image_column = gtk.VBox()
        self.load_image_button = gtk.Button('Load image')
        self.despherify_button = gtk.Button('Despherify')
        self.horizon_button = gtk.Button('Find horizon')
        self.add_sun_paths_button = gtk.Button('Add sun paths')

#        self.chooser = gtk.FileChooserDialog(title=None, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        self.load_image_button.connect('clicked', FileSelectionExample)
        self.despherify_button.connect('clicked', horizon.despherifyImage)
#        self.horizon_button.connect('clicked', horizon)
        self.add_sun_paths_button.connect('clicked', horizon.addSunPaths)

        self.image = gtk.Image()

        self.window.add(self.top_level_hbox)
        self.top_level_hbox.pack_start(self.button_column)
        self.top_level_hbox.pack_end(self.image_column)
        self.button_column.pack_start(self.load_image_button)
        self.button_column.pack_start(self.despherify_button)
        self.button_column.pack_start(self.horizon_button)
        self.button_column.pack_start(self.add_sun_paths_button)
        self.image_column.pack_start(self.image)

        self.image.set_from_file('images/sun_path_2009-03-19_800x400.jpg')

        self.image.show()
        self.load_image_button.show()
        self.despherify_button.show()
        self.horizon_button.show()
        self.add_sun_paths_button.show()
        self.image_column.show()
        self.button_column.show()
        self.top_level_hbox.show()
        self.window.show()

    def delete_event(self, widget, event, data=None):
        # could intercept and add "Are you sure?" dialog here
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

class FileSelectionExample:
    # Get the selected filename and print it to the console
    def file_ok_sel(self, w):
        print "%s" % self.filew.get_filename()

    def destroy(self, widget):
        gtk.main_quit()

    def __init__(self, Data):
        # Create a new file selection widget
        self.filew = gtk.FileSelection("File selection")

        self.filew.connect("destroy", self.destroy)

        # Connect the ok_button to file_ok_sel method
        self.filew.ok_button.connect("clicked", self.file_ok_sel)
                                                                            
        # Connect the cancel_button to destroy the widget
        self.filew.cancel_button.connect("clicked", lambda w: self.filew.destroy())

        # Lets set the filename, as if this were a save dialog,
        # and we are giving a default filename
        self.filew.set_filename('penguin.png')
        self.filew.show()

if __name__  == '__main__':
    base = Base()
    base.main()
