
- v1.1
	- added "cd /tmp" before sending script to pbrun, to avoid 
		```
		shell-init: error retrieving current directory: getcwd: cannot access parent directories: Permission denied
		chdir: error retrieving current directory: getcwd: cannot access parent directories: Permission denied
		```
		from pbrun attempting to run script in connected user directory
		
- v1.0
	- initial version
