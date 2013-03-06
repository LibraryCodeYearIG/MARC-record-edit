#yeah, this also needs cleaning up -> grokked from the main script
import re
import sys
import string
import shutil
import pymarc
import os
from pymarc import Record, Field, MARCReader, MARCWriter


#take out the '' in the date -> command line had the date in there. Need to insert an actual date here
date = re.sub("'", "", date)

#from the main script, the for loop started when the script was working with the spreadsheet of identifiers. 
#I've modified the loop but haven't tested to see if this works yet or not.
#SHIP SHIP SHIP! Fixes coming...

reader = pymarc.MARCReader(open('marc.mrc'))

for marc in reader:	

	record = Record(marc)
	
	#get the bib record from the 907 field prior to deletion
	n = record.get_fields('907')
	for field in n:
		bib_rec_num_raw = field.get_subfields('a')

	#modify subfield to strip out punctuation
	bib_rec_num_raw = str(bib_rec_num_raw)
	bib_rec_raw1 = bib_rec_num_raw.rstrip('\']')
	bib_rec_num = bib_rec_raw1.lstrip('[\'')

	#delet 947 field
	for f in record.get_fields('947'):
		  if f['a'] != '':
			  record.remove_field(f) 

	#add 590 local note for display in the library catalog
	record.add_field(
	Field(
		tag = '590',
		indicators = [' ',' '],
		subfields = [
			'a', 'Purchased with monies from the Python Fund'
		]))	
	
	#add 790 local additional author field to indicate the donor. Our catalog does index the 79X fields in the author index.
	record.add_field(
	Field(
		tag = '790',
		indicators = ['1',' '],
		subfields = [
			'a', 'Python, Doe,',
			'e', 'donor'
		]))
		
	#add 947 local field to indicate that this PDA ebook was purchased via the 'ebrar$supo' local code
	record.add_field(
		Field(
			tag = '947',
			indicators = [' ',' '],
			subfields = [
				'a', 'ebrar$supo'
			]))			

	#add 949 local field for overlay of bib record and creation of order record when record is uploaded into Millennium
	record.add_field(
		Field(
			tag = '949',
			indicators = [' ',' '],
			subfields = [
				'a', '*recs-pda;ov-%s;fd-4sch;od-%s;rd-%s;c1-----;c2-----;c3--;c4-----;rc-----;tl-----;' %(bib_rec_num, date, date)
			]))	

	#delete 907, 998, 910, 945 fields
	for f in record.get_fields('907', '998', '910', '945'):
		  if f['a'] != '':
			  record.remove_field(f) 

	writer = MARCWriter(file('file.dat','a'))
	writer.write(record)
else :
	cursor.close ()
	conn.close ()

writer.close() #closes file.dat
date = re.sub("-", "", date)
os.rename('file.dat', '%s.dat' %(date))
