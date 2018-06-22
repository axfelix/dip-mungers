from paramiko import SSHClient
from paramiko import AutoAddPolicy
from scp import SCPClient
import sys
import os

def dummy_sanitizer(s):
	return s

if len(sys.argv) != 3:
	print("This app uses 2 arguments: the server name and the local DIP path, e.g. 'dogwood /Users/garnett/Desktop/transfer-345393'")
	sys.exit()

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect((sys.argv[1] + ".archives.sfu.ca"), username="nginx")

local_dip_path = sys.argv[2]
remote_dip_path = ("/home/nginx/" + os.path.basename(local_dip_path))

with SCPClient(ssh.get_transport(), sanitize=dummy_sanitizer) as scp:
	scp.put(local_dip_path, remote_dip_path, recursive=True)

stdin, stdout, stderr = ssh.exec_command("php /usr/share/nginx/atom/symfony import:dip-objects " + remote_dip_path)
ssh.exec_command("/opt/cleanNginxHome.sh")

for x in stdout.readlines():
	if not x.isspace():
		print(x)
for x in stderr.readlines():
	if not x.isspace():
		print(x)