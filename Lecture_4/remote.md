# Working remotely

**Last update**: 20250919


### Table of Contents

1. [Terminal multiplexers (screen, tmux)](#screen)
2. [ping](#ping)
3. [ssh](#ssh)
4. [scp](#scp)
5. [ftp](#ftp)
6. [sftp](#sftp) 
7. [References](#references)





### 1. Terminal multiplexers (screen, tmux) <a name="screen"></a>

TBI 20250918 add some introductory text

This is the summary of basic 'screen' commands, which is really a great software if you want to do your thing without interruption from multiple machines. For instance, if you have a process running in 'screen' on your desktop machine in the office, then you can detach from that screen session, go somewhere else, and re-attach to that screen session remotely from any other machine in this world, and continue just like you are sitting in front of your desktop machine.



When in terminal:

- screen -S <name> # start a new screen with <name>

- screen -ls # what are the running screen sessions on my machine?

- screen -rd <screen-session-name> # re-attach to particular screen, from anywhere in the world, e.g. screen -rd 3612.pts-12.anteb

- kill -9 <screen-PID> # where <screen-PID> you can get from screen -ls, e.g. in "3612.pts-12.anteb" screen-PID is 3612

- screen -wipe <screen-name> # after you killed the certain screen, use also this command to wipe it out from history

  
  

When in 'screen':

* Ctrl+a+d # detach from screen
* Ctrl+a+c # make new session in the screen
* Ctrl+a Shift+a # name a new session in the screen
* Ctrl+a Shift+" # menu of screen sessions
* Ctrl+a+K # kill the current session in the screen




### 2. ping <a name="ping"></a>

Before connecting remotely on another computer, or before starting to transfer files remotely from one computer to another, we can check from the command line whether the remote computer is accessible (i.e. whether the remote computer is up and running, and whether the network connection to it is stable). Typically, that check is being accomplished by using the **ping** command, which checks that packets can reach remote hosts. The **ping** command verifies that the networking system can successfully support communication with another computer on the network:

```bash
ping <IP-address|hostname>
```

Some popular options are:

```bash
ping -c COUNT ... # limit to COUNT attemnts
ping -I <network interface> # check directly which network interface is causing trouble
ping -i <interval> # specify the time interval (in seconds) between packets (by default it's 1 second)
ping -t <TTL> ... # Time to Live (TTL) is maximum number of routers a packet can travel (also number of hops)
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



TBI 20250919 shall I document here how to determine IP address of a computer? If I am on that computer, it's simple: 

```bash
# Print IP address of this computer:
$ hostname -i
127.0.1.1

# Connect remotely by using IP:
$ ssh -Y someUserName@127.0.1.1
```

TBI 20250919 I could also add more elaborate example when I am not on the computer









### 3. ssh <a name="ssh"></a>

TBI 20250919 basic commands and examples



**ssh** : Secure Shell (SSH)

o 'encrypted tunnel'

o the SSH client/server architecture is based on TCP/IP

o the ssh server (sshd) runs on one machine, where it listens for incoming connections on TCP port 22

o the client simply uses TCP port 22 to connect to the server

o when connection is established, few things happen in the background

  => server and client exchange information about supported protocols (SSH2 is default these days)

  => encryption is much safer with SSH2

  => the server and client negotiate then the algorithm, followed by key that both will use for data transfer

  => the key is used only once, for the current connections, and both ends destroy it when connection terminates

  => for extended sessions the key will change regularly, with 1h being the default interval



**o Step 1**: install as root the SSH server on the target machine (e.g. OpenSSH)

```bash
apt-get install openssh-server
```



**o Step 2:** to change something in the configuration of ssh server (e.g. incoming port), edit the file:

```bash
/etc/ssh/sshd_config
```

If you did change someting in the configuration, restart the ssh server:

```bash
/etc/init.d/ssh restart # AB note that this is note the same thing as ssh, which is /bin/ssh
```



**o Step 3**: install as root the OpenSSH client on your own machine

```bash
apt-get install openssh-client
```



**o Step 4:** establish the connection using default port 22:

```bash
ssh user@remotehost
# user: the actual user name on the server
# remotehost: IP address or domain name of the server

Example:
ssh ga45mof@transfer.ktas.ph.tum.de # or ssh -l ga45mof transfer.ktas.ph.tum.de

Example: Connection via non-default port 1777
ssh -p 1777 ga45mof@transfer.ktas.ph.tum.de
```

o on first login, the client will not know the server's host key, and will prompt you to confirm that you really want to establish a connection with this remote machine. After confirming, the program generates the fingerprint



o Running commands on remote machines:

```bash
ssh ga45mof@transfer.ktas.ph.tum.de "ls -l" > someFile.log
```

Note that someFile.log is on your local machine!



o Running multiple commands remotely:

```bash
transfer 'ls -al; pwd; date'> temp4444.log # running multiple commands remotely
# note that transfer is alias, i.e.:
$ alias transfer
alias transfer='ssh -Y ga45mof@transfer.ktas.ph.tum.de'
```



**PUBLIC AND PRIVATE KEYS**  &mdash; TBI 20250919 make a subsection here

o How to circumvent a need to type passwords again and again?

=> public key authentication is an alternative

**Step 1:** generate a pair of keys

```bash
ssh-keygen -b 1024 -t rsa
```

=> this created a keypair with a public and a private key, based on RSA approach, with a length of 1024 bits

=> when prompted to enter password, press Enter twice

=> recommended key length as of 2020 is 2048 (the key length doesn't influence the speed of data transfer because this key is not used to encrypt the data)

=> this program will tell you where it has dumped the public key, typically named 'id.rsa.pub'



**Step 2:** 

o add a content of 'id.rsa.pub' on your local machine, to the following file on sever side: $HOME/.ssh/authorized_keys

=> the recommendation is to copy it via floppy or usb, avoid tranfer via email of ftp

AB: but I guess it shell be also fine via scp:

```bash
scp <path-on-local-machine>/id.rsa.pub ga45mof@transfer.ktas.ph.tum.de:~/
ssh -Y ga45mof@transfer.ktas.ph.tum.de
cat ~/id.rsa.pub >> $HOME/.ssh/authorized_keys
rm ~/id.rsa.pub
```

o passwords protect keys for interactive sessions

o key-based, password-free logins are often used to automate copying to remote machines, backuping some local date on remote machine, etc.

o ssh aliases

=> note that, instead of using Bash aliases, you can define them in ~/.ssh/config file

**TBI see example on page 71 => most likely this is more general that bash alias, as it shall work for all shells**





**Tunneling X Windows System (X11) via ssh (X11 forwarding)** &mdash; TBI 20250910 make new subsection

o sshd emulates an X server and occupies a display (number 11 by default)

o when you login to the server, the server sets the DISPLAY environment variable to this value, i.e. to **localhost:11.0**

o the idea it to avoid collisions with the X server running locally

o the information sent by computer to this display is encrypted, and sent to your computer

=> you can enable automatic X11 forwarding by modifying **ForwardX11 no** field in /etc/ssh/ssh_config

o Xming: X11 display server for Windows




### 4. scp <a name="scp"></a>


scp => comes  with SSH package
=> copy files via SSH

o the meaning of : is special in scp => it separates the name of remote machine from the pathname

Basic use cases:
```bash
# copying from remote to local:
scp <remoteComputer>:<path-on-remote> <path-on-local>

# copying from local to remote:
scp <path-on-local> <remoteComputer>:<path-on-remote>

# copying from multiple remmote machines locally in one go also possible:
scp <remoteComputer1>:<path-on-remote> <remoteComputer2>:<path-on-remote> <path-on-local>

# copying from one remote machine to another remote machine is also possible:
scp <remoteComputer1>:<path-on-remote> <remoteComputer2>:<path-on-remote>
```





### 5. ftp <a name="ftp"></a>

TBI 20250919 add some intro here



o FTP (File Transfer Protocol) => internet protocol for file transfer between client and server

o the server listens for connection requests across the networks

o many FTP servers on Internet provide anonymous service (no password is required)

o FTP transmits usernames, passwords, etc. in plain text, therefore its unsecure (sftp is secure version)



```bash
ftp ftp.server.com # opens a connection to ftp server
# or alternatively, first launch ftp client, and then use its keyword 'open'
ftp> open ftp.server.com # opens a connection to ftp server from ftp client promt
```

or on some servers:

```bash
ftp username@ftp.server.com # opens a connection to ftp server
```

o username: 'anonymous', 'ftp', or username+password



**FTP prompt ftp>exit**

o a lot of ftp commands are self-explanatory, or analogous to Bash shell

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




### 6. sftp <a name="sftp"></a>

 sftp => comes  with SSH package
=> transfer files via SSH

o **sftp** uses the same command structure as **scp**, but it has two modus operandi: interactive and batch

```bash
sftp <remoteComputer>:<path-on-remote> <path-on-local>
```



=> interactive encrypted FTP session on remote machine:

```bash
sftp ga45mof@transfer.ktas.ph.tum.de
sftp>
# now interactively I can use standard FTP commands like 'get' or 'put'

These are the commands supported in interactive sftp mode:
sftp> help
Available commands:
bye                                Quit sftp
cd path                            Change remote directory to 'path'
chgrp grp path                    Change group of file 'path' to 'grp'
chmod mode path                    Change permissions of file 'path' to 'mode'
chown own path                    Change owner of file 'path' to 'own'
df [-hi] [path]                    Display statistics for current directory or
                                  filesystem containing 'path'
exit                              Quit sftp
get [-afPpRr] remote [local]      Download file
reget [-fPpRr] remote [local]      Resume download file
reput [-fPpRr] [local] remote      Resume upload file
help                              Display this help text
lcd path                          Change local directory to 'path'
lls [ls-options [path]]            Display local directory listing
lmkdir path                        Create local directory
ln [-s] oldpath newpath            Link remote file (-s for symlink)
lpwd                              Print local working directory
ls [-1afhlnrSt] [path]            Display remote directory listing
lumask umask                      Set local umask to 'umask'
mkdir path                        Create remote directory
progress                          Toggle display of progress meter
put [-afPpRr] local [remote]      Upload file
pwd                                Display remote working directory
quit                              Quit sftp
rename oldpath newpath            Rename remote file
rm path                            Delete remote file
rmdir path                        Remove remote directory
symlink oldpath newpath            Symlink remote file
version                            Show SFTP version
!command                          Execute 'command' in local shell
!                                  Escape to local shell
?                                  Synonym for help
```

from internet: SCP is only for transferring files, and can't do other things like list remote directories or removing files, which SFTP does do.







### 7. References <a name="references"></a>

* TBI 20250919 Li
