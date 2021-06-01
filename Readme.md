# nbrshell
Set of Jupyter Notebook "cell magic" functions to remotely execute shell script typed in a notebook cell.   
Shell output is streaming back to the notebook.   
Each "cell magic" function has non-magic equivalent with name ending with "_fn"

---

Package structure :

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
