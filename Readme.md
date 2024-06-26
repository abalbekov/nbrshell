# nbrshell - Notebook Remote Shell
v1.0.14 Mar 2024

Set of Jupyter Notebook "cell magic" functions to execute remote shell script typed in a notebook cell, 
with shell script output streaming back to the notebook.

This makes it possible to write a notebook with freeform text in markdown cells and shell constructs in code cells, 
producing shell script output in output cells. This makes this a good solution for documentation purposes, prototyping, 
teaching, demoing and explaining working with unix shell, as well as templating solution for repetitive script executions.

Each "cell magic" has a non-magic equivalent function with name ending with "_fn".

Similarly, there is also Oracle database-specific "cell magic" allowing to run sqlplus commands in a remote sqlplus. 

This package uses paramiko library, which is distributed under GNU Lesser General Public License v2.1


## Package structure :

    ├── pbrun_as_oracle          │──> connects via paramiko ssh client with a password (no prior ssh 
    ├── pbrun_as_oracle_fn       │    keys setup is needed), then executes pbrun to switch to oracle account,
                                 │    then sets oracle environment according to provided "oracle_sid"
                                 │    and runs provided shell commands as oracle user.

    ├── pbrun_as                 │──> connects via paramiko ssh client with password (no prior ssh 
    ├── pbrun_as_fn              │    keys setup is needed), then executes pbrun to switch to another user,
                                 │    provided as a parameter. Then runs provided shell commands.
    
    ├── exec_shell_script        │──> connects using paramiko ssh client. If password is provided, then 
    ├── exec_shell_script_fn     │    connects with password and no prior ssh keys setup is needed.
                                 │    If password is not provided, then attempts to connect with ssh keys.
                                 │    Then runs provided shell commands.

    ├── exec_shell_script_ssh    │──> connects using local ssh client with previously setup ssh keys.
    ├── exec_shell_script_ssh_fn │    Useful in cases when paramiko will not connect.

    └── pbrun_sqlplus            │──> runs cell content via sqlplus on a remote host, after connecting  
                                 │    to the remote host with ssh, becoming oracle with pbrun and 
                                 │    setting some common Oracle environment variables.
                                    
    └── nbrshell_common          │──> common functions and variables.
        └── set_psw                   └──> sets password in memory for use in subsequent cell executions.
        └── set_nbrshell_env          └──> saves nbr environment parameters for use in subsequent executions.


## Usage examples:

1. ### To run shell commands on a remote server:

	First load remote execution package:
	
	```python
	import nbrshell as nbr
	
	# define jupyter python variable:
	jupyter_var="This is a string defined in Jupyter"
	```
	Then execute shell script on a remote server:
	
	```shell
	%%exec_shell_script user@host ssh_psw='password'
	
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
	
	This will stream following shell output in Jupyter output cell :
	
	<div style="width: 100%;">
		<img src="https://raw.githubusercontent.com/abalbekov/nbrshell/main/nbrshell/readme_svg/exec_shell_script_output.svg" style="width: 100%;" alt="Click to see the source">
	</div>
	
	The ssh connection parameters can also be set once using `nbr.set_nbrshell_env()` function, in which case it will not be necessary 
	to include them in subsequent cell magic commands, thus allowing for less cluttered notebook.


2. ### To run Oracle sqlplus on a remote server
    - #### One option is to give all connection parameters on cell command line:

        First load remote execution function:
        
        ```python
        import nbrshell as nbr
        ```
    
        Then run remote sqlplus commands with full command line options:
        
        ```python
        %%pbrun_sqlplus username@hostname ssh_psw='password1' oracle_sid='ORCL1' oracle_conn='/ as sysdba'
        
        select sysdate from dual;
        show user
        show parameters sga_target
        ```
        
        which produces below output cell:
        
        <div style="width: 100%;">
            <img src="https://raw.githubusercontent.com/abalbekov/nbrshell/main/nbrshell/readme_svg/pbrun_sqlplus_output_1.svg" style="width: 100%;" alt="Click to see the source">
        </div>


    - #### Another option is to set connection parameters once with `nbr.set_nbrshell_env()`,
        and then run remote sqlplus commands in multiple cells without command line parameters.
        Password can be hidden with `getpass` or `stdiomask` module if needed:

        ```python
        # set nbr environment :
        nbr.set_nbrshell_env(
                ssh_conn='username@hostname',
                ssh_psw='password1',
                pbrun_user='oracle',
                oracle_sid='ORCL1',
                oracle_conn='/ as sysdba'
        )
        ```
        
        ```python
        %%pbrun_sqlplus
        
        select sysdate from dual;
        show user
        ```

        <div style="width: 100%;">
            <img src="https://raw.githubusercontent.com/abalbekov/nbrshell/main/nbrshell/readme_svg/pbrun_sqlplus_output_2.svg" style="width: 100%;" alt="Click to see the source">
        </div>

        ```python
        %%pbrun_sqlplus
        
        select 'aaa' from v$instance;
        show parameters sga_target
        ```

        <div style="width: 100%;">
            <img src="https://raw.githubusercontent.com/abalbekov/nbrshell/main/nbrshell/readme_svg/pbrun_sqlplus_output_3.svg" style="width: 100%;" alt="Click to see the source">
        </div>

## Installation:

From PyPi:
```python
python -m pip install nbrshell
```

or from Github URL:
```python
python -m pip install nbrshell@git+https://github.com/abalbekov/nbrshell
```


	
	