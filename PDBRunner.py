import PDBUtils
import PhoneticTableParser
import XMLSaxParser
import xml.sax

reload(PDBUtils)
reload(PhoneticTableParser)
reload(XMLSaxParser)

#filename = 'frwiktionary-20151102-pages-meta-current.xml'
filename = 'test_wikicode.xml'


   
dict_filename = 'phonetic_dictionary_'+PDBUtils.WikiLang.active+'.txt'


   
# Wiktionary pages (sometimes) contain tables with phonetic.
# These tables can be of many types, there is a unique template for each type.
# This function tries to detect the template of the table (if any),
# and then calls the proper function to extract all the phonetics in the table.
def searchAccordTemplate(line):
   accord_templates = ['fr-accord-cons', 'fr-inv']
   


               
parser = xml.sax.make_parser()
dictionary_writter = XMLSaxParser.DictionaryWritter(dict_filename)
wikicode_parser = XMLSaxParser.WikicodeParser(dictionary_writter)
sax_handler = XMLSaxParser.SAXHandler(wikicode_parser)
parser.setContentHandler(sax_handler)
parser.parse(open(filename, "r"))
