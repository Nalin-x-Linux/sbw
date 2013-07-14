# coding: latin-1

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
import pango

from sbw import sbw_text_manipulation
from sbw import sbw_tools

#Changing directory to Home folder
os.chdir(os.environ['HOME'])

class writer(sbw_text_manipulation.text_manipulation,sbw_tools.tools):
	def __init__ (self):
		self.letter = {}
		self.guibuilder = gtk.Builder()
		self.guibuilder.add_from_file("/usr/share/pyshared/sbw/ui/braille.glade")
		self.window = self.guibuilder.get_object("window")
		self.textview = self.guibuilder.get_object("textview")
		self.label = self.guibuilder.get_object("label")
		self.textbuffer = self.textview.get_buffer()
		
		self.language_and_code = {}
		
		self.punctuation_and_name = {".":"Dot","!":"Exclamation",":":"Colon",",":"Coma","-":"Hyphen",";":"Semi-Colon",
			"?":"Question-mark","'":"quote/apostrophe","(":"Opening bracket",")":"Closing bracket","<":"Lessthan",">":"Greaterthan","[":"Left square bracket",
			"]":"Right square bracket","{":"Left Brace","}":"Right Brace",'"':"Double Quote"}
		
		self.delete_list = {'minus','backslash','equal','bracketright','bracketleft','apostrophe',\
		'slash','period','comma','grave','exclam','at','numbersign','dollar','percent','asciicircum','ampersand'\
		,'asterisk','parenleft','parenright','underscore','plus','bar','braceright','braceleft','quotedbl','colon',\
		'question','greater','less'}

		self.language_code_one = {"english":0,"spanish":1,"hindi":2,"malayalam":3,"tamil":4}
		self.language_code_two = {0:"english",1:"spanish",2:"hindi",3:"malayalam",4:"tamil"}
			
		self.get_configuration()
		self.activate_configuration()

		
		self.capitol_switch = False		
		self.run = 0
		self.c_count = 0
		
		self.stick = False
		
		#Language and contractions
		self.dot_one_three_five_six_language_list = {"malayalam"}
		self.dot_one_five_six_language_list = {"malayalam"}
				
		self.dot_three_language_list = {"malayalam"}
		self.dot_three_six_language_list = {"malayalam","hindi"}
		
		self.dot_four_language_list = {"english"}
		self.dot_four_five_language_list = {"english"}
		self.dot_four_five_six_language_list = {"english"}
		self.dot_four_six_language_list = {"english"}
		
		self.dot_five_language_list = {"english","malayalam"}
		self.dot_five_six_language_list = {"english"}
		
		self.dot_six_language_list = {"english","malayalam"}
		#self.dot__language_list = {"english","malayalam"}
		
		# Intiating thred in PyGtk
		gtk.threads_init()
		
		self.guibuilder.connect_signals(self)
		self.textview.grab_focus()
		self.window.maximize()
		self.window.show()
		gtk.main()
		


	def on_textview_output_key_release_event(self,widget,event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		start = self.textbuffer.get_iter_at_offset(self.c_count)				
		mark = self.textbuffer.get_insert()
		end = self.textbuffer.get_iter_at_mark(mark)

		if keyname.lower() in "fdsjklgh":
			if (self.run == 0):
				pressed_letters_disordered = self.textbuffer.get_text(start,end,False)
				self.run = len(pressed_letters_disordered)-1
				pressed_letters = "";
				self.textbuffer.delete(start,end);
				converted_letter = ""
				for letter in "fdsjklgh":
					if letter in pressed_letters_disordered.lower():
						pressed_letters += letter.lower()
				#One	
				if self.simple_mode == 0 and pressed_letters == "fskl" and self.language in self.dot_one_three_five_six_language_list:
					self.letter_load("%s_one_three_five_six"%self.language,self.language);self.stick = True;
				elif self.simple_mode == 0 and pressed_letters == "fkl" and self.language in self.dot_one_five_six_language_list:
					self.letter_load("%s_one_five_six"%self.language,self.language);self.stick = True;
				
				#Three	
				elif self.simple_mode == 0 and pressed_letters == "s" and self.language in self.dot_three_language_list:
					self.letter_load("%s_three"%self.language,self.language);
				elif self.simple_mode == 0 and pressed_letters == "sl" and self.language in self.dot_three_six_language_list:
					self.letter_load("%s_three_six"%self.language,self.language);self.stick = True
					
				#Four	
				elif self.simple_mode == 0 and pressed_letters == "j" and self.language in self.dot_four_language_list:
					self.letter_load("%s_four"%self.language,self.language);
				elif self.simple_mode == 0 and pressed_letters == "jk" and self.language in self.dot_four_five_language_list:
					self.letter_load("%s_four_five"%self.language,self.language);self.stick = True;
				elif self.simple_mode == 0 and pressed_letters == "jkl" and self.language in self.dot_four_five_six_language_list:
					self.letter_load("%s_four_five_six"%self.language,self.language);self.stick = True;
				elif self.simple_mode == 0 and pressed_letters == "jl" and self.language in self.dot_four_six_language_list:
					self.letter_load("%s_four_six"%self.language,self.language);self.stick = True;
				
				#Five
				elif self.simple_mode == 0 and pressed_letters == "k" and self.language in self.dot_five_language_list:
					self.letter_load("%s_five"%self.language,self.language)
				elif self.simple_mode == 0 and pressed_letters == "kl" and self.language in self.dot_five_six_language_list:
					self.letter_load("%s_five_six"%self.language,self.language);self.stick = True;
				
				#Six																																				
				elif self.simple_mode == 0 and pressed_letters == "l" and self.language in self.dot_six_language_list:
					self.letter_load("%s_six"%self.language,self.language);
					
				else:
					#Deleate the Word
					if pressed_letters == "gh":
						iter = end.copy()
						iter.backward_word_start()
						text = self.textbuffer.get_text(iter,end)
						self.textbuffer.delete(iter, end)
						self.set_main_label("Word %s deleted"%(text))
						self.capitol_switch = False
					
					#Deleate the charecter
					elif pressed_letters == "h":
						iter = end.copy()
						iter.backward_char()
						text = self.textbuffer.get_text(iter,end)
						self.textbuffer.delete(iter,end)
						self.set_main_label("%s deleted"%(text))
					else:
						try:
							converted_letter = self.letter[pressed_letters]
						except KeyError:
							pass
						
						if self.capitol_switch == True:
							self.textbuffer.insert_at_cursor(converted_letter.upper())
							self.set_main_label("Capital %s"%converted_letter);
							self.capitol_switch = False
						else:
							self.textbuffer.insert_at_cursor(converted_letter)
							self.set_main_label(converted_letter);
						self.letter_load("%s_middle"%self.language,self.language)
			else:
				if self.run >= 0:
					self.run -= 1
				else:
					self.run = 0
					
				if self.run == 0:
					if self.stick == False:
						self.letter_load("%s_middle"%self.language,self.language)
					else:
						self.stick = False

		
		if (keyname == "g" and self.language == "english" and len(pressed_letters_disordered) == 1):
			self.capitol_switch = True

		
		#Load the abbriviation for last word
		elif (keyname == "a" and not self.textbuffer.get_has_selection()):
			end.backward_char()
			start.backward_word_start()
			text = self.textbuffer.get_text(start,end)
			self.letter = {}
			for line in open("/usr/share/pyshared/sbw/data/abbreviations.txt",'r'):
				(key, val) = line[:-1].split("  ")
				self.letter[key] = val
			try:
				converted_letter=self.letter[text]
			except KeyError:
				print self.set_main_label("No abbreviation Found!")
				end.forward_char()
				self.textbuffer.backspace(end,True,True)
			else:
				end.forward_char()
				self.textbuffer.delete(start,end);
				self.textbuffer.insert_at_cursor(converted_letter)
				self.set_main_label(converted_letter)
			self.letter_load("%s_middle"%self.language,self.language)
					
		#If Space then load the orginal list	
		elif keyname == "space":
			self.letter_load(self.language,self.language)
			mark = self.textbuffer.get_insert()
			iter = self.textbuffer.get_iter_at_mark(mark)
			if iter.get_chars_in_line() >= self.limit:
				self.set_main_label("Limit exeeded!");

		
		elif keyname == "semicolon":
			self.letter_load_punctuations(self)
			start = end.copy();
			start.backward_char()
			self.textbuffer.delete(start,end)



		elif keyname == "Return":
			self.set_main_label("New Line")

		else:
			if (keyname in "~34567890zxcvbnmeqwertyuiop"):
				self.textbuffer.backspace(end,True,True)
			elif keyname in self.delete_list:
				self.textbuffer.backspace(end,True,True)
			else:
				print keyname;
			
		mark = self.textbuffer.get_insert()
		iter = self.textbuffer.get_iter_at_mark(mark)
		self.c_count = iter.get_offset() 
		print self.run,"  ",self.c_count
		if self.run < 0:
			self.run = 0
			self.textbuffer.backspace(end,True,True)
		
		
	def on_textview_output_button_release_event(self,widget,data=None):
		mark = self.textbuffer.get_insert()
		iter = self.textbuffer.get_iter_at_mark(mark)
		self.c_count = iter.get_offset()
	
	#Pass Text to main label for orca
	def set_main_label(self,text):
		try:
			text = self.punctuation_and_name[text];
		except:
			pass
		if (self.label.get_label() != "<b><span size='x-large'>%s</span></b>"%text):
			self.label.set_label("<b><span size='x-large'>%s</span></b>"%text);
		else:
			self.label.set_label("<b><span size='x-large'> %s</span></b>"%text);

			
				

############################################################
####### Key value loading functions ########################
	def letter_load(self,file_name,language):
		self.language = language
		if (file_name == "numerical_middle"):
			file_name = "numerical"
		self.letter = {}
		for line in open("/usr/share/pyshared/sbw/data/%s.txt"%file_name,'r'):
			(key, val) = line.split()
			self.letter[key] = val

	def letter_load_english_start(self,wedget,data=None):
		self.letter_load("english","english")
		self.set_main_label("English activated")
		
	def letter_load_hindi_start(self,wedget,data=None):
		self.letter_load("hindi","hindi")
		self.set_main_label("Hindi activated")

	def letter_load_spanish_start(self,wedget,data=None):
		self.letter_load("spanish","spanish")
		self.set_main_label("Spanish activated")		
		
	def letter_load_malayalam_start(self,wedget,data=None):
		self.letter_load("malayalam","malayalam")
		self.set_main_label("Malayalam activated")

	def letter_load_tamil_start(self,wedget,data=None):
		self.letter_load("tamil","tamil")
		self.set_main_label("Tamil activated")

	def numerical(self,wedget,data=None):
		self.letter_load("numerical","numerical")
		self.set_main_label("Numarical activated")

	def letter_load_punctuations(self,wedget,data=None):
		self.letter = {}
		for line in open("/usr/share/pyshared/sbw/data/punctuations.txt",'r'):
			(key, val) = line.split()
			self.letter[key] = val
			
############## End of Loading Functions #####################
#############################################################

if __name__ == "__main__":
	writer()
