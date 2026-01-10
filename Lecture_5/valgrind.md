<img src="Valgrind_logo.png" alt="drawing" width="600"/>

# Valgrind

**Last update**: 20260110


### Table of Contents

1. [Introduction](#introduction)
2. [A bit of history](#history)
3. [Installation](#installation)
4. [References](#references)





### 1. Introduction <a name="introduction"></a>



### 2. A bit of history <a name="history"></a>



### 3. Installation <a name="installation"></a>

By default, **valgrind** is not installed on Linux distributions. To install the currently supported version for a given Linux distribution, one can proceed by using the standard packaging tools for that distribution, e.g. **apt** ("Advanced Package Tool") on Ubuntu:

```bash
# Install default valgrind version with admin privileges:
$ sudo apt install valgrind

# Check your valgrind version:
$ valgrind --version
valgrind-3.18.1
```

However, there are cases when the custom **valgrind** version needs to be compiled from source (e.g. when a newer version is required than the one currently shipped by default on a given Linux distribution). The list of available **valgrind** versions and the latest releases can be obtained from the following [link](https://valgrind.org/downloads/).

For instance, to compile the custom **valgrind** version ```3.26.0``` from source, one proceeds as illustrated below, depending on whether one has or doesn't have admin privileges.

* In case you do have admin privileges, follow this step-by-step procedure:

    ```bash
    # Uninstall the default outdated version which was shipped 
    # by the Linux package manager. 
    $ sudo apt remove --purge --auto-remove valgrind
    
    # In case the call to the old version is still hashed by Bash 
    # for quicker access, simply execute (this step is harmless in any case):
    $ hash -d valgrind
    
    # Download the custom version, e.g. 3.26.0, in some directory:
    $ mkdir $HOME/valgrind && cd $HOME/valgrind
    $ wget https://sourceware.org/pub/valgrind/valgrind-3.26.0.tar.bz2
    
    # Decompress the downloaded tarball:
    $ tar xvf valgrind-3.26.0.tar.bz2
    $ cd valgrind-3.26.0
    
    # Configure:
    $ ./configure
    # Remark: valgrind executable will be installed
    # by default in /usr/local/bin , see ./configure --help
    
    # Compile valgrind using e.g. 8 CPUs:
    $ make -j 8
    
    # Install system-wide:
    $ sudo make install
    
    # Check your custom valgrind version:
    $ valgrind --version
    valgrind-3.26.0
    ```



* Alternatively, in case you do not have admin privileges, follow this procedure:

    ```bash
    # In case the call to the old version is still hashed by Bash 
    # for quicker access, simply execute (this step is harmless in any case):
    $ hash -d valgrind
    
    # Download the custom version, e.g. 3.26.0, in some directory:
    $ mkdir $HOME/valgrind && cd $HOME/valgrind
    $ wget https://sourceware.org/pub/valgrind/valgrind-3.26.0.tar.bz2
    
    # Decompress the downloaded tarball:
    $ tar xvf valgrind-3.26.0.tar.bz2
    $ cd valgrind-3.26.0
    $ InstallDir=$PWD 
    # This way, valgrind executable will be installed locally
    # in $HOME/valgrind/valgrind-3.26.0/bin
    # Otherwise, specify another path instead of $PWD
    
    # Configure as follows:
    $ ./configure --prefix=$InstallDir
    
    # Compile valgrind using e.g. 8 CPUs:
    $ make -j 8
    
    # Install locally:
    $ make install
    
    # Add installation directory to PATH with higher precedence:
    $ export PATH=$InstallDir/bin:$PATH
    # To make this installation working persistently, you will need to add
    # to ~/.bashrc this line, with fully expanded $InstallDir 
    
    $ which valgrind
    /home/abilandz/valgrind/valgrind-3.26.0/bin/valgrind
    
    # Check which version of cmake is now the default one:
    $ valgrind --version
    valgrind-3.26.0
    ```





### TBI. References <a name="references"></a>

* "_Valgrind Unlocked: Hands‑On Memory Debugging and Performance Profiling for C and C++_", William E. Clark
  * This book was the main reference used in preparing the **valgrind** part of this lecture
* Valgrind website: https://valgrind.org/