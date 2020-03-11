from paramiko import SSHClient
from paramiko import AutoAddPolicy
from scp import SCPClient
import shutil
import sys
import csv
import os
import re

def dummy_sanitizer(s):
	return s

if len(sys.argv) != 4:
	print("This app uses 3 arguments: the server name, your username, and the transfer name, e.g. 'larch garnett RD_2017-08-04_test1'")
	sys.exit()

transfer_name = sys.argv[3]
desktop_path = (os.path.expanduser("~/Desktop")  + "/" + transfer_name)

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())

dip_path_ss = '/data/' + sys.argv[1] + '/dips/**/' + transfer_name + '*/'

if not re.search("[A-Z]", transfer_name):
	dip_path_1 = '/var/archivematica/sharedDirectory/watchedDirectories/uploadedDIPs/*' + transfer_name + "/"
	dip_path_2 = '/var/archivematica/sharedDirectory/watchedDirectories/uploadDIP/*' + transfer_name + "/"
else:
	dip_path_1 = '/var/archivematica/sharedDirectory/watchedDirectories/uploadedDIPs/' + transfer_name + "*/"
	dip_path_2 = '/var/archivematica/sharedDirectory/watchedDirectories/uploadDIP/' + transfer_name + "*/"

try:
	ssh.connect("cherry.archives.sfu.ca", username=sys.argv[2])
	with SCPClient(ssh.get_transport(), sanitize=dummy_sanitizer) as scp:
		scp.get(dip_path_ss, desktop_path, recursive=True)
except:
	ssh.connect((sys.argv[1] + ".archives.sfu.ca"), username=sys.argv[2])
	try:
		with SCPClient(ssh.get_transport(), sanitize=dummy_sanitizer) as scp:
			scp.get(dip_path_1, desktop_path, recursive=True)
	except:
		with SCPClient(ssh.get_transport(), sanitize=dummy_sanitizer) as scp:
			scp.get(dip_path_2, desktop_path, recursive=True)

csv_path = (desktop_path + "/objects/" + transfer_name + ".csv")
objects_list = os.listdir(desktop_path + "/objects")
with open(csv_path, 'w', newline='\n') as csvfile:
	objects_writer = csv.writer(csvfile, delimiter=',')
	objects_writer.writerow(['filename', 'slug'])
	for x in objects_list:
		objects_writer.writerow([x])
