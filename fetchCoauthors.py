#! /bin/env python
from Bio import Entrez
import sys
from datetime import date

# Written by Casey Dunn, http://dunnlab.org

default = "NA"

#sys.argv=["null","matz@utexas.edu", "Matz MV"]

if len(sys.argv) != 3:
	print """

Downloads and parses author lists, including author affiliations, for all 
publications by a specified author from the last four years. The intent is 
to create a table of collaborators, as required for NSF grant submissions.

Data are retrieved from PubMed. This script is intended only to make a 
first pass at the table, which then needs manual inspection and correction 
for various issues including:

	- Co-authors will be duplicated if they are on multiple papers
	- Not all papers are in PubMed
	- The author name may hit multiple authors
	- Not all metadata are available for all papers in PubMed
	- This script may choke on non-ascii characters

Usage:
python parse_authors.py email@university.edu "Dunn CW"

Where:
  email@university.edu is your email. Requested by NCBI for automated 
 searches of ENTREZ.
  "Dunn CW" is the author name and initials that you are searching for.


Requires BioPython.

	"""

else:
	email = sys.argv[1]
	author_name = sys.argv[2]
	from_year = date.today().year - 4

	Entrez.email = email

	term_string = '({}[Author]) AND ("{}"[Date - Publication] : "3000"[Date - Publication])'.format(author_name, from_year)

	handle = Entrez.esearch(db="pubmed", term=term_string)
	record = Entrez.read(handle)
	idlist = record["IdList"]


	handle = Entrez.efetch("pubmed", id=idlist, retmode="xml")
	records = Entrez.parse(handle)

	print "Year\tTitle\tPubMedID\tDOI\tName\tAffiliation"

	for record in records:
		ArticleIdList = record['PubmedData']['ArticleIdList']
		ArticleIdDict = dict()
		for item in ArticleIdList:
			ArticleIdDict[item.attributes['IdType']] = str(item)

		doi = ArticleIdDict.get('doi', default)
		pubmed = ArticleIdDict.get('pubmed', default)

		year = default
		if len(record['MedlineCitation']['Article']['ArticleDate']) > 0:
			year = record['MedlineCitation']['Article']['ArticleDate'][0]['Year']

		title = record['MedlineCitation']['Article']['ArticleTitle']

		author_list = record['MedlineCitation']['Article']['AuthorList']
		for author in author_list:
			
			try:
				last = author['LastName'].encode('ascii', 'ignore')
				first = author['ForeName'].encode('ascii', 'ignore')
			except:
				last = default
				first = default
			affiliation = default
			if len(author['AffiliationInfo']) > 0:
				affiliation = author['AffiliationInfo'][0]['Affiliation'].encode('ascii', 'ignore')
			print '{}\t{}\t{}\t{}\t{}, {}\t{}'.format(year, title, pubmed, doi, last, first, affiliation)
