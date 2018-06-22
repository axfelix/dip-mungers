from agentarchives import atom
import xmltodict
import glob
import csv
import os
import re

if len(sys.argv) != 3:
	print("This app uses 2 arguments: the server name and the local DIP path, e.g. 'dogwood /Users/garnett/Desktop/transfer-345393'")
	sys.exit()

dip_names = []

csvpath = glob.glob(sys.argv[2] + '/objects/*.csv')[0]
with open(csvpath, "r") as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		for key in row.keys():
			if "filename" in key:
				row["filename"] = row.pop(key)
			if "slug" in key:
				row["slug"] = row.pop(key)
		dip_names.append(row)

metspath = glob.glob(sys.argv[2] + '/METS*.xml')[0]
with open(metspath, "r") as metsfile:
	mets = metsfile.read()

metstree = xmltodict.parse(mets)

with open(os.path.normpath(os.path.expanduser("~/.atomapi")), "r") as apikey:
	api_token = apikey.read()

client = atom.AtomClient(("http://" + sys.argv[1] + ".archives.sfu.ca"), api_token, 80)

for dip_name in dip_names:
	dip_name["filename"] = re.sub(r"\S+?-\S+?-\S+?-\S+?-\S+?-", "", dip_name["filename"])
	for techMD in metstree["mets:mets"]["mets:amdSec"]:
		try:
			if techMD["mets:techMD"]["mets:mdWrap"]["mets:xmlData"]["premis:object"]["premis:objectCharacteristics"]["premis:objectCharacteristicsExtension"]["rdf:RDF"]["rdf:Description"]["System:FileName"] == dip_name["filename"]:
				size = techMD["mets:techMD"]["mets:mdWrap"]["mets:xmlData"]["premis:object"]["premis:objectCharacteristics"]["premis:objectCharacteristicsExtension"]["rdf:RDF"]["rdf:Description"]["System:FileSize"]
		except:
			pass

	client.add_digital_object(dip_name["slug"], title=dip_name["filename"], size=size)