#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re

# Phonetic expression types
# These expressions encode the phonetic tables available on some wiktionary pages.
# Eg. for https://fr.wiktionary.org/wiki/affluent
# The following table is stored by the expression "{{fr-accord-cons|a.fly.ɑ̃|t}}"
#     +----------+------------+------------+
#     |          | Singulier  | Pluriel    |
#     +----------+------------+------------+
#     | Masculin | affluent   | affluents  |
#     |          | \a.fly.ɑ̃\  | \a.fly.ɑ̃\  |
#     +----------+------------+------------+
#     |Féminin   | affluente  | affluentes |
#     |          | \a.fly.ɑ̃t\ | \a.fly.ɑ̃t\ |
#     +----------+------------+------------+
TYPE_FR_ACCORD_CONS = 'fr-accord-cons'


# This function returns the label of the template used by the expression.
# The phonetic tables of wiktionary are stored as string expressions.
# Eg. "{{fr-accord-cons|a.fly.ɑ̃|t}}" produces a table with 2 rows/columns
# (masc/fem/sgl/plr)
def getExpressionLabel(expression):
   label = ''
   label_search = re.search('{{(.*?)\|(.*?)}}', expression)
   if label_search:
      label = label_search.group(1)
   return label


# This function chooses the proper parser, depending on the type of the template expression.
# In Wiktionary, some words have phonetic tables (with plural prononciation, etc)
# These tables are stored in the wikicode using a template expression.
# Different template expressions produce different phonetic tables,
# each table needs a specific parser.
def ParsePhoneticTableExpression(expression):
   label = getExpressionLabel(expression)
   phonetic_list = []
   if label == TYPE_FR_ACCORD_CONS:
      print 'equals'
      phonetic_list = fr_accord_cons_parser(expression)
   else:
      raise Exception("Unsupported expression label: '"+label+"'")
   print phonetic_list
   
   
   
   
   
   
# This function returns all the phonetic transcriptions stored in the expression.
# The expression is a way of condensing the phonetic information.
# Eg. for the following expression "{{fr-accord-cons|a.fly.ɑ̃|t}}"
#     the table displayed in the wiktionary page has 4 entries (2 columns, 2 rows)
#     +----------+------------+------------+
#     |          | Singulier  | Pluriel    |
#     +----------+------------+------------+
#     | Masculin | affluent   | affluents  |
#     |          | \a.fly.ɑ̃\  | \a.fly.ɑ̃\  |
#     +----------+------------+------------+
#     |Féminin   | affluente  | affluentes |
#     |          | \a.fly.ɑ̃t\ | \a.fly.ɑ̃t\ |
#     +----------+------------+------------+
#
#     => the job of this function is to return the 4 phonetic entries
#        by working out the expression.
#     NOTE: the returned values may contain duplicates.
def fr_accord_cons_parser(expression):
   assert (getExpressionLabel(expression)==TYPE_FR_ACCORD_CONS)
   
   search = re.search('{{'+TYPE_FR_ACCORD_CONS+'\|(.*?)}}', expression)
   assert (search) # should find something
   
   encoded_phonetic = search.group(1)
   base_phonetic = encoded_phonetic.split('|')[0]
   suffix_phonetic = encoded_phonetic.split('|')[1]
   
   phonetic_list = [base_phonetic, base_phonetic+suffix_phonetic]
      
   return phonetic_list
   
   