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

import enchant
import threading
import multiprocessing
import pango


import os
import gtk
from espeak import espeak
import ConfigParser

class tools():
	def get_configuration(self):
		config = ConfigParser.ConfigParser()
		if config.read('.sbw.cfg') != []:
			self.language = self.language_code_two[int(config.get('cfg','language'))]
			self.font = config.get('cfg','font')
			self.font_color = config.get('cfg','font_color')
			self.background_color = config.get('cfg','background_color')
			self.limit = int(config.get('cfg','line_limit'))
			self.simple_mode = int(config.get('cfg','simple_mode'))
		else:
			config.add_section('cfg')
			config.set('cfg', 'language', '1')
			config.set('cfg', 'font','Georgia 14')
			config.set('cfg', 'font_color','#fff')
			config.set('cfg', 'background_color','#000')			
			config.set('cfg', 'line_limit','100')
			config.set('cfg', 'simple_mode','0')
			with open('.sbw.cfg', 'wb') as configfile:
				config.write(configfile)
			self.get_configuration()
			
	def activate_configuration(self):
		pangoFont = pango.FontDescription(self.font)
		self.textview.modify_font(pangoFont)
		self.textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.Color(self.font_color))
		self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(self.background_color))
		self.letter_load(self.language,self.language)		

	def on_Preferences_activate(self,wedget,data=None):
		self.preferences_builder = gtk.Builder()
		self.preferences_builder.add_from_file("/usr/share/pyshared/sbw/ui/preferences.glade")
		self.preferences_builder.connect_signals(self)
		self.preferences_window = self.preferences_builder.get_object("window")
		self.preferences_builder.get_object("fontbutton").set_font_name(self.font)
		self.preferences_builder.get_object("colorbutton_font").set_color(gtk.gdk.Color(self.font_color))
		self.preferences_builder.get_object("colorbutton_background").set_color(gtk.gdk.Color(self.background_color))
		self.preferences_builder.get_object("spinbutton_line_limit").set_value(self.limit)
		self.preferences_builder.get_object("combobox_language").set_active(self.language_code_one[self.language])
		self.preferences_builder.get_object("checkbutton_simple_mode").set_active(self.simple_mode)
		self.preferences_window.show()
	
	
	def on_button_apply_clicked(self,wedget,data=None):
		config = ConfigParser.ConfigParser()
		self.font = self.preferences_builder.get_object("fontbutton").get_font_name()
		self.font_color = str(self.preferences_builder.get_object("colorbutton_font").get_color())
		self.background_color = str(self.preferences_builder.get_object("colorbutton_background").get_color())
		self.limit = self.preferences_builder.get_object("spinbutton_line_limit").get_value_as_int()
		self.language = self.language_code_two[self.preferences_builder.get_object("combobox_language").get_active()]
		self.simple_mode = int(self.preferences_builder.get_object("checkbutton_simple_mode").get_active())

		config.read('.sbw.cfg')
		config.set('cfg', 'language', self.language_code_one[self.language])
		config.set('cfg', 'font',self.font)
		config.set('cfg', 'font_color',self.font_color)
		config.set('cfg', 'background_color',self.background_color)			
		config.set('cfg', 'line_limit',self.limit)
		config.set('cfg', 'simple_mode',self.simple_mode)
		with open('.sbw.cfg', 'wb') as configfile:
			config.write(configfile)
		self.activate_configuration()
		self.preferences_window.destroy()

	def on_button_preferences_close_clicked(self,wedget,data=None):
		self.preferences_window.destroy()				
			
	def on_About_activate(self,wedget,data=None):
		self.guibuilder_about = gtk.Builder()
		self.guibuilder_about.add_from_file("/usr/share/pyshared/sbw/ui/about.glade")
		self.window_about = self.guibuilder_about.get_object("window")
		self.guibuilder_about.connect_signals({"on_close_clicked" : self.about_close})		
		self.window_about.show()
	
	def about_close(self,wedget,data=None):
		self.window_about.destroy()


#  FUNCTION TO CHECK SPELLING		
	def on_Spell_Check_activate(self,data=None):
		#Loading Dict
		key_value = {"numerical": "en","english" : "en","spanish" : "es","hindi" : "hi","malayalam" : "ml ","tamil" : "ta"}
		self.dict = enchant.Dict("%s" % key_value[self.language])
		
		#Builder And Gui
		builder = gtk.Builder()
		builder.add_from_file("/usr/share/pyshared/sbw/ui/Spell.glade")
		self.spell_window = builder.get_object("window")
		builder.connect_signals(self)
		self.entry = builder.get_object("entry")
		
		self.liststore = gtk.ListStore(str)
		self.treeview = builder.get_object("treeview")
		
		self.treeview.connect("row-activated",self.activate_treeview)
		
		self.treeview.set_model(self.liststore)
		column = gtk.TreeViewColumn("Suggestions : ")
		self.treeview.append_column(column)		
		cell = gtk.CellRendererText()
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 0)
		
					
		self.user_dict={}
		mark = self.textbuffer.get_insert()
		self.word_start = self.textbuffer.get_iter_at_mark(mark)
		self.word_end = self.textbuffer.get_iter_at_mark(mark)

		self.word = self.textbuffer.get_text(self.word_start,self.word_end)	
		while(True):
			try:
				if self.dict.check(self.word) == False and len(self.word) > 1:
					break
			except enchant.errors.Error:
				pass
			else:
				pass
			self.word_start.forward_word_ends(2)
			self.word_end.forward_word_end()
			self.word_start.backward_word_start()
			self.word = self.textbuffer.get_text(self.word_start,self.word_end)
			self.textview.scroll_to_iter(self.word_start, 0.2, use_align=False, xalign=0.5, yalign=0.5)
		
		
		self.liststore.clear()
		for item in self.dict.suggest(self.word):
			self.liststore.append([item])
			
		
		self.context_sentence_start = self.word_start.copy()
		self.context_sentence_end = self.word_start.copy()
		self.context_sentence_start.backward_sentence_start()
		self.context_sentence_end.forward_sentence_end()		
		self.textbuffer.select_range(self.context_sentence_start,self.context_sentence_end)
		
		self.entry.set_text(self.word)
		self.spell_window.show()
	
	def activate_treeview(self,widget, row, col):
		model = widget.get_model()
		text = model[row][0]
		self.entry.set_text(text)
		self.entry.grab_focus()  

	def say_context(self,data=None):
		context_sentence_start = self.word_start.copy()
		context_sentence_end = self.word_start.copy()
		context_sentence_start.backward_sentence_start()
		context_sentence_start.backward_sentence_start()
		context_sentence_end.forward_sentence_end()
		#self.notify(self.textbuffer.get_text(context_sentence_start,context_sentence_end),False,None,True)
				
	def close(self,widget,data=None):
		self.spell_window.destroy()	

	def change(self,data=None):
		#self.textbuffer.remove_tag(self.highlight_tag,self.context_sentence_start,self.context_sentence_end)
		self.textbuffer.delete(self.word_start, self.word_end)
		self.textbuffer.insert(self.word_start, self.entry.get_text())
		self.entry.set_text("")
		self.word_start.forward_word_end()
		self.word_end = self.word_start.copy()
		self.word_start.backward_word_starts(1)		
		self.word = self.textbuffer.get_text(self.word_start,self.word_end)
		self.find_next_miss_spelled()
		
		
	def change_all(self,data=None):
		self.textbuffer.delete(self.word_start, self.word_end)
		self.textbuffer.insert(self.word_start, self.entry.get_text())
		self.user_dict[self.word] = self.entry.get_text()
		self.entry.set_text("")
		self.word_start.forward_word_end()
		self.word_end = self.word_start.copy()
		self.word_start.backward_word_starts(1)		
		self.word = self.textbuffer.get_text(self.word_start,self.word_end)
		self.entry.set_text("")
		self.word_start.forward_word_end()
		self.word_end = self.word_start.copy()
		self.word_start.backward_word_starts(1)		
		self.find_next_miss_spelled()

	def ignore(self,data=None):
		self.entry.set_text("")
		self.word_start.forward_word_ends(2)
		self.word_end = self.word_start.copy()
		self.word_start.backward_word_starts(1)
		self.find_next_miss_spelled()	

	def ignore_all(self,data=None):
		if self.dict.is_added(self.word) == False:
			self.dict.add(self.word)
		self.entry.set_text("")
		self.word_start.forward_word_ends(2)
		self.word_end = self.word_start.copy()
		self.word_start.backward_word_starts(1)	
		self.find_next_miss_spelled()	

	def find_next_miss_spelled(self):
		#self.textbuffer.remove_tag(self.highlight_tag,self.context_sentence_start,self.context_sentence_end)
		if self.word_end.is_end() == True:
			try:
				self.textbuffer.get_text(sentence_start,sentence_end)
			except NameError:
				#self.notify("Spell Checking Compleated!",True,0,True)
				self.spell_window.destroy()
			else:
				pass	
			
		self.word = self.textbuffer.get_text(self.word_start,self.word_end)
		while(True):
			try:
				if self.dict.check(self.word) == False and len(self.word) > 1: 
					break
			except enchant.errors.Error:
				pass
			else:
				pass
			if self.word in self.user_dict.keys():
				self.textbuffer.delete(self.word_start, self.word_end)
				self.textbuffer.insert(self.word_start, self.user_dict[self.word])
				self.entry.set_text("")
				self.word_start.forward_word_end()
				self.word_end = self.word_start.copy()
				self.word_start.backward_word_starts(1)		
				self.word = self.textbuffer.get_text(self.word_start,self.word_end)
			else:
				self.word_start.forward_word_ends(2)
				self.word_end.forward_word_end()
				self.word_start.backward_word_start()
				self.word = self.textbuffer.get_text(self.word_start,self.word_end)
		
		
		self.context_sentence_start = self.word_start.copy()
		self.context_sentence_end = self.word_start.copy()
		self.context_sentence_start.backward_sentence_start()
		self.context_sentence_end.forward_sentence_end()		
		self.textbuffer.select_range(self.context_sentence_start,self.context_sentence_end)
		self.textview.scroll_to_iter(self.word_start, 0.2, use_align=False, xalign=0.5, yalign=0.5)
		
		
		
		self.entry.set_text(self.word)
		self.liststore.clear()
		for item in self.dict.suggest(self.word):
			self.liststore.append([item])
		
		self.entry.grab_focus()
		
	#Audio Converter	
	def on_Audio_converter_activate(self,wedget,data=None):
		try:
			start,end = self.textbuffer.get_selection_bounds()
		except ValueError:
			print "Nothing selected!"
		else:
			self.text_to_convert = self.textbuffer.get_text(start,end)
			to_convert = open("temp.txt",'w')
			to_convert.write(self.text_to_convert)
			to_convert.close()
			
			builder = gtk.Builder()
			builder.add_from_file("/usr/share/pyshared/sbw/ui/audio_converter.glade")
			builder.connect_signals(self)
			self.audio_converter_window = builder.get_object("window")
			
			
			
			self.spinbutton_speed = builder.get_object("spinbutton_speed")
			self.spinbutton_pitch = builder.get_object("spinbutton_pitch")
			self.spinbutton_split = builder.get_object("spinbutton_split")
			self.spinbutton_vloume = builder.get_object("spinbutton_vloume")
			
			voice = builder.get_object("combobox_language_convert")
			for item in espeak.list_voices():
				voice.append_text(item.name)
			voice.set_active(12)
				
			voice.connect('changed', self.change_voice)
			self.audio_converter_window.show()		                

	def change_voice(self, voice):
		self.model_voice = voice.get_model()
		self.index_voice = voice.get_active()
		
	def close_audio_converter(self,widget,data=None):
		self.audio_converter_window.destroy()	
		
	def convert_to_audio(self,widget,data=None):
		self.filename = gtk.FileChooserDialog("Type the output wav name",
                               None,
                               gtk.FILE_CHOOSER_ACTION_SAVE,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_SAVE, gtk.RESPONSE_OK))
                self.filename.set_current_folder("%s/Lios"%(os.environ['HOME']))
                self.filename.run()
                self.file_to_output = self.filename.get_filename()
                self.filename.destroy()
                threading.Thread(target=self.record_to_wave,args=()).start()
                self.audio_converter_window.destroy()
		
	def record_to_wave(self):
		convert_ps = multiprocessing.Process(target=self.convert_function)
		convert_ps.start()
		while convert_ps.is_alive():
			pass
			
	def convert_function(self):
		os.system('espeak -a %s -v %s -f temp.txt -w %s.wav --split=%s -p %s -s %s' % (self.spinbutton_vloume.get_value(),self.model_voice[self.index_voice][0],self.file_to_output,self.spinbutton_split.get_value(),self.spinbutton_pitch.get_value(),self.spinbutton_speed.get_value()))
