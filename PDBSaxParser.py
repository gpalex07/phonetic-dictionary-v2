#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import PDBUtils
import PDBWikiBracketsTagParser
import xml.sax

TAG_TITLE = 'title'
TAG_TEXT = 'text'

CODE_NO_HEADER_FOUND = -1

HEADER_LEVEL_LANGAGE_SECTION = 2
HEADER_LEVEL_WORD_TYPE_SECTION = 3

# This class is responsible for extracting tags contained
# in the wikicode of a wiktionary page.
class WikicodeTagExtractor:
   # Parses the line and returns:
   #  -the header level, if any. (wikitag '=== header ===')
   #  -any bracket tag (wikitag '{{something}}')
   @staticmethod
   def parseLine(line, just_after_word_type_section):
      header_level = WikicodeTagExtractor.extractWikiHeaderTagLevel(line)
      brackets_tag = WikicodeTagExtractor.extractWikiBracketsTag(line)
      return header_level, brackets_tag
   
   # Returns the level of the header contained in the line (if any), 
   # or returns CODE_NO_HEADER_FOUND otherwise.
   # NOTE: the headers are defined using the '=' sign.
   #       The number of '=' defines the header level (<H1>, <H2>, <H3> etc)
   # Eg: '== section_name =='    --> <H1> 
   #     '=== section_name ==='  --> <H2> 
   #      etc.
   # More details here: https://en.wikipedia.org/wiki/Help:Wiki_markup#Sections
   @staticmethod
   def extractWikiHeaderTagLevel(line):
      section_level = CODE_NO_HEADER_FOUND
      search_res = re.search('([=]+)(.*?)([=]+)', line)
      if search_res:
         opening_tag = search_res.group(1)
         section_level = len(opening_tag)
      return section_level
      
   # Retuns any expression of type "{{something}}" (=wiki brackets tag).
   @staticmethod
   def extractWikiBracketsTag(line):
      wiki_tag = ''
      search_res = re.search('{{(.+?)}}', line)
      if search_res:
         wiki_tag = search_res.group(0)
      return wiki_tag
      


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
      self.text_tag_line_parser = WikicodeTagExtractor()
      self.just_after_word_type_section = False
   
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
         #lng, phonetic, self.just_after_word_type_section = self.text_tag_line_parser.parseLine(line, self.just_after_word_type_section)
         header_level, brackets_tag = self.text_tag_line_parser.parseLine(line, self.just_after_word_type_section)
         
         if brackets_tag:
            is_word_type_section = PDBWikiBracketsTagParser.WikiBracketsTagParser.isWordTypeSection(brackets_tag)
         # if the line is something like this "=== {{S|adverbe|fr}} ==="
         #if header_level==HEADER_LEVEL_LANGAGE_SECTION and is_word_type_section:
            
         
         lng =''
         if lng and lng != self.current_section_lng:
            #print 'Lng:', lng
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