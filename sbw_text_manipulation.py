###########################################################################
#    SBW - Sharada-Braille-Writer
#    Copyright (C) 2012-2013 Nalin.x.Linux GPL-3
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

import os
import gtk
import os
from espeak import espeak

class text_manipulation():		
	def on_abbreviations_open_activate(self,wedget,data=None):
		abbreviations = open("/usr/share/pyshared/sbw/data/abbreviations.txt",'r')
		self.textbuffer.set_text(abbreviations.read())
		self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
		self.set_main_label("Edit the abbreviation List.")
	
	def on_abbreviations_save_activate(self,wedget,data=None):
		abbreviations = open("/usr/share/pyshared/sbw/data/abbreviations.txt",'w')
		start, end = self.textbuffer.get_bounds()
		text = self.textbuffer.get_text(start, end)
		for line in text.split("\n"):
			if len(line.split("  ")) == 2:
				abbreviations.write("%s\n"%(line))
				#abbreviations.write("%s  %s\n"%(line.split("~")[0],line.split("~")[1]))
		abbreviations.close()
		self.set_main_label("Abbreviation List saved.")		
		
	def on_abbreviations_restore_activate(self,wedget,data=None):
		abbreviations = open("/usr/share/pyshared/sbw/data/abbreviations.txt",'w')
		abbreviations_default = open("/usr/share/pyshared/sbw/data/abbreviations_default.txt",'r')
		abbreviations.write(abbreviations_default.read())
		abbreviations.close()
		self.set_main_label("Abbreviation List Restored to Default!")
		
	
	def on_open_activate(self,wedget,data=None):
		open_file = gtk.FileChooserDialog(title="Select the file to open" ,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                open_file.set_current_folder("%s"%(os.environ['HOME']))
                filter = gtk.FileFilter()
                filter.add_pattern("*.txt")
                filter.add_pattern("*.text")
                open_file.add_filter(filter)
                response = open_file.run()
                if response == gtk.RESPONSE_OK:
					to_read = open("%s" % (open_file.get_filename()))
					to_open = to_read.read()
					try:
						self.textbuffer.set_text(to_open)
					except IOError:
						self.set_main_label("Sorry could not open this file!")
					else:
						self.set_main_label("%s opend"%(open_file.get_filename()))
						self.save_file_name = open_file.get_filename()
						self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
                open_file.destroy()


	def on_save_activate(self,wedget,data=None):
		start,end = self.textbuffer.get_bounds()
		text = self.textbuffer.get_text(start,end)
		if (text == ""):
			self.set_main_label("Nothing to save")
		else:		
			try:
				self.save_file_name
			except AttributeError:
				self.set_main_label("file name please?")				
				save_file = gtk.FileChooserDialog(title="Save ",action=gtk.FILE_CHOOSER_ACTION_SAVE,
		                     buttons=(gtk.STOCK_SAVE,gtk.RESPONSE_OK))    
				save_file.set_current_folder("%s"%(os.environ['HOME']))
				save_file.set_current_name(text[0:10]);
				save_file.set_do_overwrite_confirmation(True);
				filter = gtk.FileFilter()
				filter.add_pattern("*.txt")
				filter.add_pattern("*.text")
				save_file.add_filter(filter)
				response = save_file.run()
				if response == gtk.RESPONSE_OK:
					self.save_file_name = "%s"%(save_file.get_filename())
					open("%s" %(self.save_file_name),'w').write(text)
					self.textbuffer.set_modified(False)	
					self.set_main_label("File Saved to %s"%(self.save_file_name))
					save_file.destroy()
					return True
				else:
					save_file.destroy()
					return False
					
					
			else:
				open("%s" %(self.save_file_name),'w').write(text)	
				self.textbuffer.set_modified(False)
				self.set_main_label("File Saved.")
				return True
			
	def on_gtk_save_as_activate(self,wedget,data=None):
		del self.save_file_name
		self.on_save_activate(self);
															                     			
	def on_new_activate(self,wedget,data=None):
		if self.textbuffer.get_modified() == True:
			dialog =  gtk.Dialog("Start new without saving ?",self.window,gtk.DIALOG_DESTROY_WITH_PARENT,
			("Save", gtk.RESPONSE_ACCEPT, "Cancel" ,gtk.RESPONSE_CLOSE, "Start-New!", gtk.RESPONSE_REJECT))                           						
			response = dialog.run()
			dialog.destroy()				
			if response == gtk.RESPONSE_REJECT:
				start, end = self.textbuffer.get_bounds()
				self.textbuffer.delete(start, end)
				self.set_main_label("New")
				self.run = self.c_count = 0
				del self.save_file_name													
			elif response == gtk.RESPONSE_ACCEPT:
				if (self.on_save_activate(self)):
					start, end = self.textbuffer.get_bounds()
					self.textbuffer.delete(start, end)
					self.set_main_label("New")
					self.run = self.c_count = 0
					del self.save_file_name
				else:
					self.set_main_label("File not saved!") 
		else:
			self.set_main_label("New")
			self.run = self.c_count = 0
			

	def on_Punch_File_activate(self,wedget,data=None):
		punch_file = gtk.FileChooserDialog(title="Select the file to open" ,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                punch_file.set_current_folder("%s"%(os.environ['HOME']))
                filter = gtk.FileFilter()
                filter.add_pattern("*.txt")
                filter.add_pattern("*.text")
                punch_file.add_filter(filter)
                response = punch_file.run()  
                if response == gtk.RESPONSE_OK:
					to_read = open("%s"%(punch_file.get_filename()))
					to_open = to_read.read()
					try:
						self.textbuffer.insert_at_cursor(to_open)
					except IOError:
						self.set_main_label("Sorry could not open this file!")
					else:
						self.set_main_label("%s Punched"%(punch_file.get_filename()))
					self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
		punch_file.destroy()
                

			
	def on_window_delete_event(self,wedget,data=None):
		if self.textbuffer.get_modified() == True:
			dialog =  gtk.Dialog("Close without saving ? Press escape to quit!.",self.window,gtk.DIALOG_DESTROY_WITH_PARENT,
			("Save", gtk.RESPONSE_ACCEPT, "Quit", gtk.RESPONSE_CLOSE))                           						
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_CLOSE:
				gtk.main_quit()			
			elif response == gtk.RESPONSE_ACCEPT:
				if (self.on_save_activate(self)):
					gtk.main_quit()
				else:
					self.set_main_label("File not saved!")
			else:
				gtk.main_quit()
		else:
			gtk.main_quit()

			
								
	def on_Read_Me_activate(self,wedget,data=None):
		read_me = open("/usr/share/pyshared/sbw/data/help.txt",'r')
		read_me_text = read_me.read()
		self.textbuffer.set_text(read_me_text)
		start,end = self.textbuffer.get_bounds()
		self.textbuffer.place_cursor(start)
		self.textbuffer.set_modified(False)
	def on_contraction_guide_activate(self,wedget,data=None):
		guide = open("/usr/share/pyshared/sbw/data/contraction-guide.txt",'r')
		guide_text = guide.read()
		self.textbuffer.set_text(guide_text)
		start,end = self.textbuffer.get_bounds()
		self.textbuffer.place_cursor(start)
		self.textbuffer.set_modified(False)	
