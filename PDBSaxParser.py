#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import PDBUtils
import xml.sax

TAG_TITLE = 'title'
TAG_TEXT = 'text'


# This class is responsible for parsing the lines of text located
# between the tag "<text>...</text>" of the wiktionary xml dump.
class TextTagLineParser:
   def parseLine(self, line):
      lng = self.searchLangageSection(line)
      phonetic = self.searchPhonetic(line)
            
      return lng, phonetic
      
   # The langage section in wiktionary is a ruban that indicates the langage of the word.
   # Eg. for https://fr.wiktionary.org/wiki/ok there are several langage section
   # such as 'Bimin', 'Espéranto', 'Gagaouze', 'Iwam', 'Muyu du Nord', 'Muyu du Sud' etc.
   def searchLangageSection(self, line):
      langage = ''
      search_res = re.search('==([ ]*?){{langue\\|(.*?)}}([ ]*?)==', line)
      if search_res:
          langage = search_res.group(2)
      return langage
   
   #
   # Returns the phonetic transcriptions found in the current line.
   #
   # Phonetic transcriptions can be found anywhere in the wikicode.
   # Sometimes a paragraph contains a phnoetic transcription but it's 
   # just a degretion talking about the way the word was pronounced in old times.
   # We don't need these obsolete transcriptions, so we need a filter them.
   # The easiest way is to only extract the transcriptions that we know
   # correspond to current pronouciation.
   # This is way we are only interested in the transcriptions located in 2 specific places:
   #  -the transcriptions in the phonetic table:
   #     Eg. for https://fr.wiktionary.org/wiki/affluent
   #     The following table is the phonetic table on the page for 'affluent':
   #     +----------+------------+------------+
   #     |          | Singulier  | Pluriel    |
   #     +----------+------------+------------+
   #     | Masculin | affluent   | affluents  |
   #     |          | \a.fly.ɑ̃\  | \a.fly.ɑ̃\  |
   #     +----------+------------+------------+
   #     |Féminin   | affluente  | affluentes |
   #     |          | \a.fly.ɑ̃t\ | \a.fly.ɑ̃t\ |
   #     +----------+------------+------------+
   #     These transcriptions are accurate and will be extracted by the function.
   #     NOTE: this table is not available on all pages.
   #  -the transcription located immediatly under the "word type" section are also accurate.
   #     Eg. for https://fr.wiktionary.org/wiki/affluent
   #     Since the word 'affluent' is an homograph, there are several 'word type' sections,
   #     and under each section there is a phonetic transcription of the word.
   #        Eg. for the adjective form of 'affluent', here the section and the transcription lines:
   #        |Adjectif [modifier | modifier le wikicode]
   #        |affluent \a.fly.ɑ̃\
   #     NOTE: this transcription will be extraced only when no phonetic table is available
   #           (since that transcription is always containted in the table, when there is one).   
   def searchPhonetic(self, line):
      section_phonetic = self.searchPhoneticUnderWordTypeSection(line)
      return section_phonetic
      
      
   def searchPhoneticUnderWordTypeSection(self, line):
      phonetic = ''
      #phonetic_search = re.search('{{pron\\|(.*?)\\|'+PDBUtils.WikiLang.native+'}}', line)
      # Extract the phonetic that is placed immedialty under the section title.
      search_res = re.search("'''(.*?)''' {{pron\\|(.*?)\\|"+PDBUtils.WikiLang.active+"}}", line)
      if search_res:
         phonetic = search_res.group(2)
      return phonetic


class DictionaryWritter:
   
   def __init__(self, dict_filename):
      self.dict_file = open(dict_filename, 'w')
      self.nb_written_words = 0
      
   def __del__(self):
      self.dict_file.close()

   def appendNewWord(self, word):
      if self.nb_written_words > 0:
         self.dict_file.write('\n')
      self.dict_file.write(word)
      self.nb_written_words = self.nb_written_words +1
   
   
class WikicodeParser:

   def __init__(self, dictionary_writter):
      self.dict_writter = dictionary_writter
      self.inside_tag_title = False
      self.inside_tag_text = False
      self.current_section_lng = ''
      self.found_phonetics = []
      self.text_tag_line_parser = TextTagLineParser()
   
   def tagTitleOpened(self):
      self.inside_tag_title = True
      # By default the langage is the active one 
      # (except if the langage is explicitly specified by a langage section)
      self.current_section_lng = PDBUtils.WikiLang.active
      # Clear the phonetic results of the previous word.
      found_phonetics = []
   def tagTitleClosed(self):
      self.inside_tag_title = False
   def tagTextOpened(self):
      self.inside_tag_text = True
   def tagTextClosed(self):
      self.inside_tag_text = False
      
   def parseTitle(self, line):
      return line
      
   def parseText(self, line):
      self.current_section_lng = searchLangageSection(line)
      
    
   def parseCurrentLine(self, line):
      if self.inside_tag_title:
         # The title tag in the XML contains the word for the current page.
         word = self.parseTitle(line)
         assert word         
         self.dict_writter.appendNewWord(word)
         print "Word: '"+word+"'"   
      elif self.inside_tag_text:
         lng, phonetic = self.text_tag_line_parser.parseLine(line)
         
         if lng and lng != self.current_section_lng:
            print 'Lng:', lng
            self.current_section_lng = lng
         
   
class SAXHandler(xml.sax.ContentHandler):

   def __init__(self, *args, **kwargs):
      self.wikicode_parser = args[0]
      
   #def __INIT__(self, wikicode__parser):
   #   self.wikicode_parser = wikicode__parser
   
   def startElement(self, name, attrs):
      if name == TAG_TITLE:
         self.wikicode_parser.tagTitleOpened()
      elif name == TAG_TEXT:
         self.wikicode_parser.tagTextOpened()
   
   def endElement(self, name):
      if name == TAG_TITLE:
         self.wikicode_parser.tagTitleClosed()
      elif name == TAG_TEXT:
         self.wikicode_parser.tagTextClosed()
         print "--------------------------------------------------"
         
   def characters(self, line):
      line = line.encode('utf-8')
      line = line.rstrip()
      self.wikicode_parser.parseCurrentLine(line)