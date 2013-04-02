import re
import sys
import string
import os
from pymarc import Record, Field, MARCReader, MARCWriter


#from the main script, the for loop started when the script was working with the spreadsheet of identifiers. 
#I've modified the loop and have tested it, but there still might be bugs to squish.
#SHIP SHIP SHIP! Fixes coming...

#open the file of marc records, exampledump.mrc, which should be in the same place as this script.
#the unicode/utf8 handling code is from https://github.com/edsu/pymarc/issues/7#issuecomment-1346308
records = MARCReader(open('exampledump.mrc'),to_unicode=True, force_utf8=True, utf8_handling='ignore')

#set date variable
date = '2013-05-02'

for marc in records:	
	
	#get the bib record from the 907 field prior to deletion
	n = marc.get_fields('907')
	for field in n:
		bib_rec_num_raw = field.get_subfields('a')

	#modify subfield to strip out punctuation
	bib_rec_num_raw = str(bib_rec_num_raw)
	bib_rec_raw1 = bib_rec_num_raw.rstrip('\']')
	bib_rec_num = bib_rec_raw1.lstrip('[\'')

	#delet 947 field
	for f in marc.get_fields('947'):
		  if f['a'] != '':
			  marc.remove_field(f) 

	#add 590 local note for display in the library catalog
	marc.add_field(
	Field(
		tag = '590',
		indicators = [' ',' '],
		subfields = [
			'a', 'Purchased with monies from the Python Fund'
		]))	
	
	#add 790 local additional author field to indicate the donor. Our catalog does index the 79X fields in the author index.
	marc.add_field(
	Field(
		tag = '790',
		indicators = ['1',' '],
		subfields = [
			'a', 'Python, Doe,',
			'e', 'donor'
		]))
		
	#add 947 local field to indicate that this PDA ebook was purchased via the 'ebrar$supo' local code
	marc.add_field(
		Field(
			tag = '947',
			indicators = [' ',' '],
			subfields = [
				'a', 'ebrar$supo'
			]))			

	#add 949 local field for overlay of bib record and creation of order record when record is uploaded into Millennium
	marc.add_field(
		Field(
			tag = '949',
			indicators = [' ',' '],
			subfields = [
				'a', '*recs-pda;ov-%s;fd-4sch;od-%s;rd-%s;c1-----;c2-----;c3--;c4-----;rc-----;tl-----;' %(bib_rec_num, date, date)
			]))	

	#delete 907, 998, 910, 945 fields
	for f in marc.get_fields('907', '998', '910', '945'):
		  if f['a'] != '':
			  marc.remove_field(f) 
	
	#append record to a generic file.dat file
	writer = MARCWriter(file('file.dat','a'))
	writer.write(marc)

#closes file.dat
writer.close() 

#take the date variable and get rid of the dashes
date = re.sub("-", "", date) 

#rename file.dat to the date in the date variable
os.rename('file.dat', '%s.dat' %(date))
