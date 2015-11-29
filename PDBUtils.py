#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Langages of the wiktionary
class WikiLang:
   fr = 'fr'
   active = fr # The langage for which the script are building a phonetic dictionary.
   

   
   
written_phonetic = []
def appendNewPhonetic(phonetic):
   if phonetic not in written_phonetic:
      print 'Adding phonetic:', phonetic
      dict_file.write(' '+phonetic)
      written_phonetic.append(phonetic)
      
      
def TitleContainsExcludedWord(title):
   excluded_titles = ['MediaWiki:']
   must_exclude = any(excluded_title in title for excluded_title in excluded_titles)
   print excluded_titles[0], 'in', title, excluded_titles[0] in title
   if must_exclude == True:
      print 'must exclude', title
   return must_exclude
      

   
      
   # This functions tries to find a 'word type' section in the current line.
   # Eg. for https://fr.wiktionary.org/wiki/affluent
   #   Since the word 'affluent' is an homograph, there are several 'word type' sections
   #   (adjective, verb form etc)
   #     Eg. here the 'word type' section of the html page for the adjective form of 'affluent':
   #       |Adjectif [modifier | modifier le wikicode]
   # More details here: https://fr.wiktionary.org/wiki/Wiktionnaire:Structure_des_pages
   def searchWordTypeSection(self, line):
      word_type = ''
      search_res = re.search('{{S\\|(.+?)|'+PDBUtils.WikiLang.active, line) # don't include the end because
      if search_res:
         word_type = search_res.group(1)
         print 'word_type=', word_type, line
      return word_type
      
   # The langage section in wiktionary is a ruban that indicates the langage of the word.
   # Eg. for https://fr.wiktionary.org/wiki/ok there are several langage section
   # such as 'Bimin', 'Espéranto', 'Gagaouze', 'Iwam', 'Muyu du Nord', 'Muyu du Sud' etc.
   def searchLangageSection(self, line):
      langage = ''
      search_res = re.search('==([ ]*?){{langue\\|(.+?)}}([ ]*?)==', line)
      if search_res:
         langage = search_res.group(2)
         print 'Lng:', langage
      return langage
   
   # Extracts the transcription located immediatly under the "word type" section in the wikicode.
   # Eg. for https://fr.wiktionary.org/wiki/affluent
   #   Since the word 'affluent' is an homograph, there are several 'word type' sections
   #   (adjective, verb form etc), and under each section there is a phonetic transcription of the word.
   #     Eg. for the adjective form of 'affluent', here the word type section and the associated transcription line:
   #       |Adjectif [modifier | modifier le wikicode]
   #       |affluent \a.fly.ɑ̃\
   def searchPhoneticUnderWordTypeSection(self, line):
      phonetic = ''
      search_res = re.search("'''(.+?)''' {{pron\\|(.+?)\\|"+PDBUtils.WikiLang.active+"}}", line)
      if search_res:
         phonetic = search_res.group(2)
      return phonetic
      
   # This function extracts the template expression in the current line (if any).
   # The phonetic tables are stored as a template expression.
   # (for info: the wiki engine then converts this text expression into an html table).
   # Eg. the phonetic table for the word 'affluent' is: {{fr-accord-cons|a.fly.ɑ̃|t}}
   #     https://fr.wiktionary.org/w/index.php?title=affluent&action=submit
   def tryExtractingPhoneticTableExpression(self, line):
      expression = ''
      search_res = re.search("{{(.+?)\\|(.+?)}}", line)
      if search_res:
         expression = search_res.group(0)
      return expression
   
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
   #  - the transcription located immediatly under the "word type" section in the wikicode.
   #     NOTE: this transcription will be extracted only when no phonetic table is available
   #           (since that transcription is always containted in the table, when there is one).
   def searchPhonetic(self, line, just_after_word_type_section):
      section_phonetic = self.searchPhoneticUnderWordTypeSection(line)
      
      if just_after_word_type_section:
         self.tryExtractingPhoneticTableExpression(line)
      return section_phonetic