from agentarchives import atom
import xmltodict
import glob
import csv
import os
import re
import sys

if len(sys.argv) != 3:
	print("This app uses 2 arguments: the server name and the local DIP path, e.g. 'dogwood /Users/garnett/Desktop/transfer-345393'")
	sys.exit()

dip_names = []

csvpath = glob.glob(sys.argv[2] + '/objects/*.csv')[0]
with open(csvpath, "r") as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		new_row = {}
		for key, value in row.items():
			if "filename" in key:
				new_row["filename"] = value
			if "slug" in key:
				new_row["slug"] = value
		dip_names.append(new_row)

metspath = glob.glob(sys.argv[2] + '/METS*.xml')[0]
with open(metspath, "r") as metsfile:
	mets = metsfile.read()

metstree = xmltodict.parse(mets)

with open(os.path.normpath(os.path.expanduser("~/.atomapi")), "r") as apikey:
	api_token = apikey.read()

client = atom.AtomClient(("https://" + sys.argv[1] + ".archives.sfu.ca"), api_token, 443)

for dip_name in dip_names:
	dip_name["filename"] = re.sub(r"\S+?-\S+?-\S+?-\S+?-\S+?-", "", dip_name["filename"])
	for techMD in metstree["mets:mets"]["mets:amdSec"]:
		try:
			if os.path.splitext(techMD["mets:techMD"]["mets:mdWrap"]["mets:xmlData"]["premis:object"]["premis:objectCharacteristics"]["premis:objectCharacteristicsExtension"]["rdf:RDF"]["rdf:Description"]["System:FileName"])[0] == os.path.splitext(dip_name["filename"])[0]:
				size = techMD["mets:techMD"]["mets:mdWrap"]["mets:xmlData"]["premis:object"]["premis:objectCharacteristics"]["premis:objectCharacteristicsExtension"]["rdf:RDF"]["rdf:Description"]["System:FileSize"]
		except:
			pass

	client.add_digital_object(dip_name["slug"], title=dip_name["filename"], size=size)