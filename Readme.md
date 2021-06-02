# nbrshell
Set of Jupyter Notebook "cell magic" functions to remotely execute shell script typed in a notebook cell.   
Shell output is streaming back to the notebook.   
Each "cell magic" function has a non-magic equivalent with name ending with "_fn"

---

## Package structure :

    ├── pbrun_as_oracle       │--> connects using paramiko ssh client with password (i.e. no prior keys setup is needed)
    ├── pbrun_as_oracle_fn    │    Then executes pbrun to switch to oracle user and sets oracle environment according 
                                   to provided "oracle_sid", then runs provided shell commands.

    ├── pbrun_as              │--> connects using paramiko ssh client with password (i.e. no prior keys setup is needed)
    ├── pbrun_as_fn           │    Then executes pbrun to switch to another user
                                   Then runs provided shell commands.
    
    ├── exec_shell_script     │--> connects using paramiko ssh client. If password is provided, then connects with password
    ├── exec_shell_script_fn  │    and no prior ssh keys setup is needed.
                                   If password is not provided, then attempts to connect with ssh keys.
                                   Then runs provided shell commands.

    ├── exec_shell_script_ssh    │--> connects using local ssh client with previously setup ssh keys.
    ├── exec_shell_script_ssh_fn │    Useful in cases when paramiko can not connect.

    └── nbrshell_common          │--> common functions and variables.
        └── set_psw                   └--> sets password in memory for use in subsequent executions.

---

## Usage examples:

---

- #### To run shell commands on a remote server:
```python
from nbrshell import exec_shell_script
jupyter_var="This is a string defined in Jupyter"
```
```shell
%%exec_shell_script user@host psw='password'

echo "Running ping :"
echo "--------------"
ping -s www.oracle.com 56 3

echo "Running loop :"
echo "--------------"
for i in 1 2 3 4 5; do
    echo $i
done

echo "Here document :"
echo "--------------"
cat <<-EOF
    This is multiline 
    here document
EOF

echo "Jupyter variable substitution :"
echo "---------------------------"
echo {jupyter_var}

echo "escaping curly braces :"
echo "---------------------------"
echo '\{Curly braces\} need to be escaped to prevent Jupyter variable substitution'
```

Produces output :

```text
Running ping:
--------------
PING www.oracle.com: 56 data bytes
64 bytes from a104-99-86-191.deploy.static.akamaitechnologies.com (104.99.86.191): icmp_seq=0. time=12.871 ms
64 bytes from a104-99-86-191.deploy.static.akamaitechnologies.com (104.99.86.191): icmp_seq=1. time=12.706 ms
64 bytes from a104-99-86-191.deploy.static.akamaitechnologies.com (104.99.86.191): icmp_seq=2. time=12.794 ms

----www.oracle.com PING Statistics----
3 packets transmitted, 3 packets received, 0% packet loss
round-trip (ms)  min/avg/max/stddev = 12.706/12.790/12.871/0.083
Running loop:
--------------
1
2
3
4
5
Here document:
--------------
    This is multiline 
    here document
Jupyter variable substitution:
---------------------------
This is a string defined in Jupyter
escaping curly braces :
---------------------------
{Curly braces} need to be escaped to prevent Jupyter variable substitution
```

---

- #### To run SQLPLUS commands on ORACLE_SID=ORCL on a remote server:

```python
from nbrshell import pbrun_as_oracle, set_psw
set_psw('password')
```
```shell
%%pbrun_as_oracle user@host oracle_sid='ORCL1'

echo "select sysdate from dual;" | sqlplus -s / as sysdba

sqlplus / as sysdba @/dev/stdin <<-EOF
    set echo on
    select 'aaa' from v\$instance;
EOF
```
Produces output :
```text
SYSDATE
---------
01-JUN-21


SQL*Plus: Release 19.0.0.0.0 - Production on Tue Jun 1 22:40:54 2021
Version 19.10.0.0.0

Copyright (c) 1982, 2020, Oracle.  All rights reserved.


Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.10.0.0.0

SQL> 	 select 'aaa' from v$instance;

'AA
---
aaa

SQL> Disconnected from Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.10.0.0.0
```
