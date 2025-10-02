# Working remotely

**Last update**: 20251002-5


### Table of Contents

1. [Terminal multiplexers (screen, tmux)](#screen)
2. [ping](#ping)
3. [ssh, scp, sftp](#ssh.scp.sftp)	 	
4. [References](#references)





### 1. Terminal multiplexers (screen, tmux) <a name="screen"></a>

In high-energy physics, one frequently encounters a situation where the processing of a dataset is feasible only by using large computing facilities. In that case, one needs to connect and organize the work on a remote computer (typically, this amounts to running shell scripts for the automated job submission, merging output files, copying, etc.). It would be very inconvenient if, after each remote login, one would need to set up the working environment from scratch, start all the scripts, etc. In addition, if on a remote computer there is a running process that will not terminate before a user wants to disconnect, it is essential to be able to keep that process running, and reattach to it with a new login later, without affecting the status of that running process.

All these functionalities can be achieved by _terminal multiplexers_. These software tools make it possible to detach and reattach sessions from a terminal running on any computer, including the computers on which only remote access is possible. They also enable the separation of running processes from the shell that started that process (by design, one shell cannot take control of a process started by another shell). In turn, this keeps the remote process running even when the user is disconnected from remote computer (i.e. after its login shell has terminated). Several open-source terminal multiplexers are available, with **screen** and **tmux** being the most popular ones. In this lecture, the primary focus and all examples are provided for **screen**. 

To start a **screen** one executes in the terminal:

```bash
$ screen -S test
```

However, at least at first glance, nothing seems to change. But the important difference is that now we are in a new process, independent from the parent shell, which will keep running even if the parent shell terminates. At any point later, and from any other shell on this computer, we can reattach to this **screen** session named "test", and all processes started in it will be running uninterrupted. To illustrate this, we can in the **screen** session start the following command:

````bash
$ while :; do date; sleep 10s; done
Mo 22. Sep 08:31:51 CEST 2025
Mo 22. Sep 08:32:01 CEST 2025
...
````

The above code snippet will after each 10 seconds print the timestamp in an infinite loop. To detach from this **screen** session, we execute:

```bash
$ Ctrl+a+d # hit this combination of keystrokes to detach from screen session
[detached from 536338.test]
```

From the info message "detached from 536338.test" we can read off the process ID (536338) of the **screen** session which we just left, and its name "test". We now illustrate the main point: at any point later we can login again on this computer, and reattach to this very same **screen** session, in the following way:

```bash 
# List all running screen sessions on this computer:
$ screen -ls 
There are screens on:
	536338.test	(22.09.2025 08:31:45)	(Detached)
... list of other screen sessions on this computer, if any ...
Remove dead screens with 'screen -wipe'.
12 Sockets in /run/screen/S-abilandz.

# Reattach to screen session using its process ID 536338, or its name "test":
$ screen -rd "test"
while :; do date; sleep 10s; done
Mo 22. Sep 08:31:51 CEST 2025
Mo 22. Sep 08:32:01 CEST 2025
Mo 22. Sep 08:32:11 CEST 2025
Mo 22. Sep 08:32:21 CEST 2025
Mo 22. Sep 08:32:31 CEST 2025
Mo 22. Sep 08:32:41 CEST 2025
Mo 22. Sep 08:32:51 CEST 2025
Mo 22. Sep 08:33:01 CEST 2025
....
```

As we can see, the process started in **screen** was running uninterrupted in the meantime, even after we detached from it. 

Below is the summary of basic **screen** commands, which can be executed either from the terminal, or within **screen** session.

* When in a terminal:
  * ```screen -S someName``` # start a new screen with name "someName"
  * ```screen -ls``` # list all running screen sessions on this computer
  * ```screen -rd someScreenName``` # reattach to screen session with the name "someScreenName" (alternatively, screen PID can be used)
  * ```kill -9 screenPID``` # terminate screen session from the terminal. Its PID can can be obtained from ```screen -ls```, e.g. in "536338.test", screenPID is 536338
  * ```screen -wipe someScreenName``` # after you killed the certain screen, this step may be necessary &mdash; use this command to wipe out the killed **screen** session from history
  * ```screen -S screenPID.oldName -X sessionname newName``` &mdash; rename screen session after it was created 


* When in **screen** ("+" in the syntax below is a metacharacter, and stands for "_and press_"):

  * ```Ctrl+a+d``` # detach from **screen**

  * ```Ctrl+a+c``` # make new window in the **screen**, running its own process

  * ```Ctrl+a Shift+a``` # set a title for a new window in the **screen**

  * ```Ctrl+a Shift+"``` # menu of all **screen** windows, each running its own independent process

  * ```Ctrl+a+k``` # kill the current window in the **screen** session
  
  * ```Ctrl+a+ESC``` # enters the vertical scroll mode in the current window &mdash; use up and arrow keys, or mouse wheel, to scroll back and forth vertically (press ```ESC``` to go back to the normal mode)
  
  * ```Ctrl+a+:``` # gives internal **screen** prompt starting with ```:``` which accepts internal **screen** commands, for instance: 
  
    ```
    :title someTitle # now this window has title “someTitle”
    ```
  
    Summary of other keywords which **screen** interprets as internal commands can be found at this [link](https://www.gnu.org/software/screen/manual/screen.html#Command-Summary).		  	 

In practice, in a given **screen** session, we establish several windows (see ```Ctrl+a Shift+a``` above), each of running its own process. If within **screen** session we hit the combination ```Ctrl+a Shift+"```, we get the menu of all independent processes running in that **screen**:

```bash
 Num Name
   0 Submit - kta                                                                                                                 
   1 Offline                                                                                                                     
   2 Monitoring                                                                                                                   
   3 Move  
```

Simply selecting 0, 1, 2, or 3, will move us to the environment where any of these processes is executed. When we detach and reattach from the **screen** session, all independent processes in each window keep running uninterrupted. In the very same spirit, if you have a process running in a **screen** on your desktop machine in the office, then you can detach from that **screen** session, go somewhere else, and reattach to that **screen** session remotely from any other computer, and continue your work just like you are still sitting in front of your desktop machine.

Finally, we remark on the environment: since a **screen** session runs in its own process, it will inherit at creation time from the parent shell only the settings of variables exported in the parent shell, and afterward cannot modify them globally. Since each **screen** window runs in its own process, each **screen** window maintains its own independent environment within a given **screen** session.








### 2. ping <a name="ping"></a>

Before connecting remotely to another computer, or before starting to transfer files remotely from one computer to another, we can check from the command line whether the remote computer is accessible (i.e. whether the remote computer is up and running, and whether the network connection to it is stable). Typically, that check is accomplished by using the **ping** command, which checks that packets can reach remote hosts. The **ping** command verifies that the networking system can successfully support communication with another computer on the network:

```bash
ping <IP-address|hostname>
```

Some popular options are:

```bash
ping -c COUNT ... # limit to COUNT attempts
ping -I <network interface> # check directly which network interface is causing trouble
ping -i <interval> # specify the time interval (in seconds) between packets (by default it's 1 second)
ping -t <TTL> # Time to Live (TTL) is maximum number of routers a packet can travel (also number of hops)
ping -s <packetsize> # specifies the number of data bytes to be sent
```

The output of **ping** command shows a report for each packet in an unending list that includes information on whether the attempt was successful or not, along with the response times, for instance:

```bash
# Using the hostname of remote computer:
$ ping nidoqueen.ktas.ph.tum.de
PING nidoqueen.ktas.ph.tum.de (10.152.133.25) 56(84) bytes of data.
64 bytes from nidoqueen.ktas.ph.tum.de (10.152.133.25): icmp_seq=1 ttl=63 time=0.756 ms
64 bytes from nidoqueen.ktas.ph.tum.de (10.152.133.25): icmp_seq=2 ttl=63 time=0.629 ms
64 bytes from nidoqueen.ktas.ph.tum.de (10.152.133.25): icmp_seq=3 ttl=63 time=0.621 ms
64 bytes from nidoqueen.ktas.ph.tum.de (10.152.133.25): icmp_seq=4 ttl=63 time=0.686 ms
...

# Using the IP address of remote computer:
$ ping 10.152.133.25
PING 10.152.133.25 (10.152.133.25) 56(84) bytes of data.
64 bytes from 10.152.133.25: icmp_seq=1 ttl=63 time=0.699 ms
64 bytes from 10.152.133.25: icmp_seq=2 ttl=63 time=0.630 ms
64 bytes from 10.152.133.25: icmp_seq=3 ttl=63 time=0.788 ms
64 bytes from 10.152.133.25: icmp_seq=4 ttl=63 time=0.831 ms
...
```

The above printout can be interpreted as follows: It takes less than 1 ms for the packet of 64 bytes to get to the remote host be responded to (everything less than 1 s is usually perfectly fine). The variable ```icmp_seq``` is the number of packet, and if there is no problem with the routing, packets will be enlisted in consecutive order. 

Finally, we remark on the IP ("Internet Protocol") address. This is a numerical label uniquely assigned to each computer connected to a network. If we know the host name, we can read off its IP address using for instance either **ping** or **nslookup** commands:

```bash
$ ping nidoqueen.ktas.ph.tum.de
PING nidoqueen.ktas.ph.tum.de (10.152.133.25) 56(84) bytes of data.
64 bytes from nidoqueen.ktas.ph.tum.de (10.152.133.25): icmp_seq=1 ttl=63 time=0.756 ms
...
# => IP address of 'nidoqueen' is 10.152.133.25

$ nslookup nidoqueen.ktas.ph.tum.de
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
Name:	nidoqueen.ktas.ph.tum.de
Address: 10.152.133.25
# => IP address of 'nidoqueen' is 10.152.133.25
```

If we need IP address of the computer we are currently working on, it's even simple by using **hostname** command: 

```bash
# Print IP address of this computer:
ga45mof@nidoqueen:~$ hostname -i
10.152.133.25
```

TBI 20250923 See if I want still to add something here, or at least make a bridge towards next section







### 3. ssh, scp, sftp <a name="ssh.scp.sftp"></a>

Secure Shell (SSH) protocol was designed in 1995 by Tatu Ylönen as a secure way of accessing and executing commands on a remote computer, over unsecured network. Through the use of encryption mechanisms authentication across a public network, i.e. sending username and password to remote computer, is made safe. The **ssh** command is typically used to log into a remote computer's shell and to execute commands remotely after connection is established.

Technically, the **ssh** command establishes _encrypted tunnel_ between two computers, using client/server architecture based on TCP/IP (Transmission Control Protocol/Internet Protocol). The **ssh** server, which in essence is the **sshd** process running in the background (i.e. _daemon_), runs on one machine where it listens for incoming connections on TCP port 22. The client then uses TCP port 22 to connect to the server. When connection between two computers is established, a few things happen in the background:

- server and client exchange information about supported protocols for encrypted communication (SSH2 is default nowadays); 

- server and client negotiate the algorithm, followed by the key that both will use for data transfer;

- the key is used only once, for the current connection, and both ends will destroy it when connection terminates;

- for extended sessions the key will change regularly (with 1 hour being the default interval).

We now summarize all steps needed to use **ssh** for remote access and remote command execution:



**Step 1** &mdash; install as a root using **sudo** command the SSH server on the target remote machine (e.g. OpenSSH server):

```bash
$ sudo apt-get install openssh-server
```

This step is rarely needed for remote computer, because an admin responsible for it will install OpenSSH server among the first things on that computer. However, if you want to allow remote access to your own computer (also to yourself), you need to install OpenSSH server with root privileges on your computer. 




**Step 2** &mdash; to change something in the configuration of **ssh** server (e.g. its incoming port), edit with root privileges the configuration file:

```bash
/etc/ssh/sshd_config
```

This step is rarely needed in practice, but if you did change something in this configuration file, you have to restart the **ssh** server:

```bash
$ /etc/init.d/ssh restart # note that this is not the same executable as ssh, which is /bin/ssh
```



**Step 3** &mdash; install as root the OpenSSH client on your own computer:

```bash
$ sudo apt-get install openssh-client
```



**Step 4a** &mdash; login to remote computer using the generic syntax (using the default port 22) and continue to work there:

```bash
$ ssh user@remotehost
# user: the actual user name on a remote computer
# remotehost: IP address or domain name of a remote computer
```

For instance:

```bash
# Connect remotely to "nidoqueen.ktas.ph.tum.de", with username "ga45mof":
$ ssh -Y ga45mof@nidoqueen.ktas.ph.tum.de
ga45mof@nidoqueen.ktas.ph.tum.de's password:
ga45mof@nidoqueen:~$
# ... do your thing in a shell running on a remote computer ...
```

The flag ```-Y``` will enable trusted graphics (the X Window System or X11) forwarding, i.e. executing graphics on remote computer. On the first login, the client will not know the server's host key, and will prompt you to confirm that you really want to establish a connection with this remote computer. After confirming, the program generates the fingerprint.



**Step 4b** &mdash; execute from your computer remotely some commands on a remote computer, and continue to work on your local computer:

```bash
# List the content of your home directory on remote computer:
$ ssh ga45mof@nidoqueen.ktas.ph.tum.de 'ls -al'
ga45mof@nidoqueen.ktas.ph.tum.de's password:
... list of files ...

# List the content of your home directory on remote computer, 
# and redirect it to a file on your local computer:
$ ssh ga45mof@nidoqueen.ktas.ph.tum.de 'ls -al' > someFile.log
ga45mof@nidoqueen.ktas.ph.tum.de's password:

$ cat someFile.log
... list of files ...
```

It is straightforward to execute remotely multiple commands using ```;``` to separate them:

```bash
$ ssh ga45mof@nidoqueen.ktas.ph.tum.de 'hostname; pwd; date'
ga45mof@nidoqueen.ktas.ph.tum.de's password: 
nidoqueen.ktas.ph.tum.de
/home/ktas/ga45mof
Wed Sep 24 09:14:30 CEST 2025
```

Each time the **ssh** command was executed, the password prompt appeared to re-authenticate, before new connection can be established. This step can be circumvented by using public key for authentication as an alternative &mdash; this is explained in subsection "Public and private keys" further below. 

The **scp** ("Secure Copy") command comes within the SSH package, and it can be used to securely copy files between computers on a network. This includes the case when one wants to copy a file from a local computer to remote computer, or vice versa. 

The metacharacters ```@``` and ```:``` have a special meaning in the syntax of **scp** command:

* ```@``` &mdash; separates the user name and the name of remote computer;

* ```:``` &mdash; separates the name of remote computer from some pathname on that computer. 

Basic use cases of the **scp** command are summarized as follows:  

```bash
# copying a file from remote to local computer:
scp userName@remoteComputer:pathOnRemote pathOnLocal

# copying a file from local to remote computer:
scp pathOnLocal userName@remoteComputer:pathOnRemote
```

The same syntax can be used to copy securely directories from one computer to another, only **scp** has to be replaced with **scp -r**.

**Example 1:**  Copy into a current working directory the file _someFile.txt_, which sits in a directory ```${HOME}/someDir``` on a remote computer named ```nidoqueen.ktas.ph.tum.de```, on which a user has an account named ```ga45mof```.

```bash
$ scp ga45mof@nidoqueen.ktas.ph.tum.de:~/someDir/someFile.txt .
ga45mof@nidoqueen.ktas.ph.tum.de's password:
someFile.txt                                   100%    0     0.0KB/s   00:00 
```

Note that for a home directory on remote computer, we have used metacharacter ```~```, and not the environment variable ```$HOME```, because the latter would have been expanded by a shell on a local computer. On a contrary, `~` is expanded only if it is the first character of a word and it is unquoted:

```bash
$ echo $HOME
/home/abilandz

$ echo "$HOME"
/home/abilandz

$ echo ~
/home/abilandz

$ echo :~
:~

$ echo ~:
/home/abilandz:

$ echo "~:"
~:
```



**Example 2:** Copy a directory  ```${HOME}/someDir``` from local computer, into home directory on a remote computer named ```nidoqueen.ktas.ph.tum.de```, on which a user has an account named ```ga45mof```.

```bash
$ scp -r ${HOME}/someDir ga45mof@nidoqueen.ktas.ph.tum.de:~/
ga45mof@nidoqueen.ktas.ph.tum.de's password:
someDir                                   100%    0     0.0KB/s   00:00 
```

As a rule of thumb, when using the **scp** command, refer to home directory on a local computer with ```${HOME}```, and on remote computer with ```~``` metacharacter. The **scp** command can be only used for transferring files from one computer to another, and cannot do other things like list directories on remote computer or delete files remotely. That can be achieved with the **sftp** ("Secure File Transfer Protocol") command, which is introduced next.

The **sftp** command can be used interactively on a remote computer, and is basically a secure version of an old **ftp** command. One establishes an interactive session on remote computer by using the following generic syntax:

```bash
sftp userName@remoteComputer
```

For instance, to establish an interactive session on a remote computer ```nidoqueen.ktas.ph.tum.de``` as a user ```ga45mof```:

```bash
$ sftp ga45mof@nidoqueen.ktas.ph.tum.de
ga45mof@nidoqueen.ktas.ph.tum.de's password:
Connected to nidoqueen.ktas.ph.tum.de.
sftp> 
```

We are now running interactive session remotely, and **sftp** command is waiting to interpret our command input. To see which commands **sftp** can accept, hit TAB + TAB in the **sftp** promt:

```
sftp> TAB + TAB
bye       cd        chdir     chgrp     chmod     
chown     df        dir       exit      get       
help      lcd       lchdir    lls       lmkdir    
ln        lpwd      ls        lumask    mkdir     
mget      mput      progress  put       pwd       
quit      reget     rename    reput     rm        
rmdir     symlink   version   !         ? 
```

You can get more details about each command this way:

```
sftp> help
Available commands:
bye                               Quit sftp
cd path                           Change remote directory to 'path'
chgrp grp path                    Change group of file 'path' to 'grp'
chmod mode path                   Change permissions of file 'path' to 'mode'
chown own path                    Change owner of file 'path' to 'own'
df [-hi] [path]                   Display statistics for current directory or
                                  filesystem containing 'path'
exit                              Quit sftp
get [-afPpRr] remote [local]      Download file
reget [-fPpRr] remote [local]     Resume download file
reput [-fPpRr] [local] remote     Resume upload file
help                              Display this help text
lcd path                          Change local directory to 'path'
lls [ls-options [path]]           Display local directory listing
lmkdir path                       Create local directory
ln [-s] oldpath newpath           Link remote file (-s for symlink)
lpwd                              Print local working directory
ls [-1afhlnrSt] [path]            Display remote directory listing
lumask umask                      Set local umask to 'umask'
mkdir path                        Create remote directory
progress                          Toggle display of progress meter
put [-afPpRr] local [remote]      Upload file
pwd                               Display remote working directory
quit                              Quit sftp
rename oldpath newpath            Rename remote file
rm path                           Delete remote file
rmdir path                        Remove remote directory
symlink oldpath newpath           Symlink remote file
version                           Show SFTP version
!command                          Execute 'command' in local shell
!                                 Escape to local shell
?                                 Synonym for help
```

A lot of **sftp** commands are self-explanatory, or analogous to **Bash** shell. 

o **get** and **mget** 

```bash
ftp> get someFile
```

=> this downloads 'someFile' from the current remote directory to the current local directory



```bash
ftp> get someFile1 someFile2
```

=> this downloads 'someFile1' from the current remote directory to the file 'someFile2' in the current local directory



```bash
ftp> mget someFile1 someFile2
```

=> this downloads 'someFile1' and 'someFile2' from the current remote directory to the current local directory



=> it is possible to use wildcards

```bash
ftp> mget someFile*
```



Example: **Download new Bash release via ftp:**

```bash
Announcement from Chet:
The first public release of bash-5.2 is now available with the URLs
ftp://ftp.cwru.edu/pub/bash/bash-5.2.tar.gz
ftp://ftp.gnu.org/pub/gnu/bash/bash-5.2.tar.gz

Then, I can simply:

$ ftp
ftp> open ftp.gnu.org # when prompted for a Name, use "ftp" or "anonymous"
                      # for ftp.cwru.edu, use "ftp" both for username and password
ftp> pass # switch on the passive mode. Do it only if you trust the server
ftp> cd /pub/gnu/bash # navigate to Bash dir 
ftp> get bash-5.2.tar.gz
local: bash-5.2.tar.gz remote: bash-5.2.tar.gz
227 Entering Passive Mode (3,216,83,128,125,83).
150 Opening BINARY mode data connection for bash-5.2.tar.gz (10950833 bytes).
226 Transfer complete.
10950833 bytes received in 1.2 seconds (8.7e+03 Kbytes/s)

And that's it!
```



o **put** and **mput** 

=> the other way around (client => server)



o **promt** : toggle prompting, the default is ON

```bash
ftp> prompt
```

Switches off interacting mode when transferring the files (after this, I do not have to press 'y' for each file)



o **mdelete** : deletes multiple files on the server side

o **lpwd** : print pwd on a local machine



**TBI 20250919** See also explanation of some 'ftp' commands here https://www.computerhope.com/issues/ch001246.htm



TBI 20250919 use the following nice example from SO, how **ftp** can read here-doc  https://stackoverflow.com/questions/66348808/ftp-upload-in-bash-script

```bash
#!/bin/bash

connection(){
 ftp -i -n $line << EOS
 user $user $pass
 put $filename
 bye
 EOS
}
```











#### a) Public and private keys

In this section, all steps needed for an authentication via public keys are summarized. TBI 20250930 expand a bit this intro, it's too terse at the moment



**Step 1** &mdash; generate a pair of keys on your local computer:

```bash
$ ssh-keygen -b 2048 -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/abilandz/.ssh/id_rsa):
# just press Enter, and the default file /home/abilandz/.ssh/id_rsa.pub will be used
Enter passphrase (empty for no passphrase): 
# just press Enter
Enter same passphrase again:
# just press Enter again
Your identification has been saved in /home/abilandz/.ssh/id_rsa
Your public key has been saved in /home/abilandz/.ssh/id_rsa.pub
The key fingerprint is:
... some more specific info for this key pair ...
```

This command created a keypair with a public and a private key, based on RSA ("Rivest–Shamir–Adleman") cryptosystem, with a length of 2048 bits. The recommended key length as of 2020 is 2048 bits (the key length doesn't influence the speed of data transfer because this key is not used to encrypt the data). By default, the public key is stored in the file ```${HOME}/.ssh/id_rsa.pub```.



**Step 2** &mdash; copy the public key to remote computer:  

Add the content of file  ```${HOME}/.ssh/id_rsa.pub``` on your local computer, to the file ```$HOME/.ssh/authorized_keys``` on a remote computer (in this example, a user named 'ga45mof' is connecting remotely on a computer named 'nidoqueen.ktas.ph.tum.de'): 

```bash
# Copy a file from your local computer to remote computer, using 'scp' command:
$ scp ${HOME}/.ssh/id_rsa.pub ga45mof@nidoqueen.ktas.ph.tum.de:~/
ga45mof@nidoqueen.ktas.ph.tum.de's password: 
id_rsa.pub                             100%  397   228.6KB/s   00:00    

# Connect to remote computer:
$ ssh -Y ga45mof@nidoqueen.ktas.ph.tum.de
ga45mof@nidoqueen.ktas.ph.tum.de's password:

# Add the content of just copied file with a public key to a list of authorized_keys:
$ cat ${HOME}/id_rsa.pub >> $HOME/.ssh/authorized_keys

# Remove the copied file with a public key:
$ rm ${HOME}/id_rsa.pub
```



**Step 3** &mdash; check if you can connect to remote computer, without being prompted for a password:  

```bash
$ ssh -Y ga45mof@nidoqueen.ktas.ph.tum.de
ga45mof@nidoqueen:~$
# ... do your thing in a shell running on a remote computer ...
```



**Step 4** &mdash; check if you can copy something from remote computer locally, without being prompted for a password:  

```bash
# Copy a file ~/someFile from remote computer, to the current working directory on a local computer
$ scp ga45mof@nidoqueen.ktas.ph.tum.de:~/someFile .
someFile                             100%    123     228.0KB/s   00:00    

# Remark: To copy directories this way, use scp -r
```

Key-based, password-free logins are often used to automate copying to remote machines, backuping some local date on remote machine, etc.



TBC 20250930



=> note that, instead of using Bash aliases, you can define them in ~/.ssh/config file

**TBI see example on page 71 => most likely this is more general that bash alias, as it shall work for all shells**





**Tunneling X Windows System (X11) via ssh (X11 forwarding)** &mdash; TBI 20250910 make new subsection

o sshd emulates an X server and occupies a display (number 11 by default)

o when you login to the server, the server sets the DISPLAY environment variable to this value, i.e. to **localhost:11.0**

o the idea it to avoid collisions with the X server running locally

o the information sent by computer to this display is encrypted, and sent to your computer

=> you can enable automatic X11 forwarding by modifying **ForwardX11 no** field in /etc/ssh/ssh_config

o Xming: X11 display server for Windows






### 4. References <a name="references"></a>

* TBI 20250919 Li
