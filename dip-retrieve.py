from paramiko import SSHClient
from paramiko import AutoAddPolicy
from scp import SCPClient
import shutil
import sys
import csv
import os

def dummy_sanitizer(s):
	return s

if len(sys.argv) != 4:
	print("This app uses 3 arguments: the server name, your username, and the transfer name, e.g. 'larch garnett RD_2017-08-04_test1'")
	sys.exit()

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect((sys.argv[1] + ".archives.sfu.ca"), username=sys.argv[2])

transfer_name = sys.argv[3]
dip_path = '/var/archivematica/sharedDirectory/watchedDirectories/uploadedDIPs/' + transfer_name + "*/"

desktop_path = (os.path.expanduser("~/Desktop")  + "/" + transfer_name)
with SCPClient(ssh.get_transport(), sanitize=dummy_sanitizer) as scp:
	scp.get(dip_path, desktop_path, recursive=True)

csv_path = (desktop_path + "/objects/" + transfer_name + ".csv")
objects_list = os.listdir(desktop_path + "/objects")
with open(csv_path, 'w', newline='\n') as csvfile:
	objects_writer = csv.writer(csvfile, delimiter=',')
	objects_writer.writerow(['filename', 'slug'])
	for x in objects_list:
		objects_writer.writerow([x])
