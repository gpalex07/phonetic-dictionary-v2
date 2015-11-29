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
      

   