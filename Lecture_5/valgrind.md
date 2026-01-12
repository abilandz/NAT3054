<img src="Valgrind_logo.png" alt="drawing" width="600"/>

# Valgrind

**Last update**: 20260112


### Table of Contents

1. [Introduction](#introduction)
2. [A bit of history](#history)
3. [Installation](#installation)
4. [Memory management: **Memcheck**](#memcheck)
5. [Heap profiling: **Massif**](#massif)
6. [References](#references)





### 1. Introduction <a name="introduction"></a>

Valgrind is an advanced programming tool for debugging, memory management, memory-leak detection, and profiling of Linux programs. Its primary use case is to detect any sort of memory-related problems, but it also can be used to optimize and speed up program execution by determining bottlenecks at runtime. 

Valgrind uses the _dynamic binary instrumentation (DBI)_ technique, meaning that any executable can be inspected with Valgrind as it is (i.e. no code modification or recompilation is necessary). This particularly means that Valgrind can also be used for proprietary programs for which we do not have access to the source code at all. This comes with a price, however: when a program is examined by Valgrind, it will run slower by a factor of 5-100, depending which Valgrind tool is used. Nevertheless, this still pays off when compared to endless manual debugging sessions ("guess and try recompilation", etc.).

A few additional remarks:

- **Supported programming languages** &mdash; Valgrind works with programs written in any programming language (compiled, just-in-time compiled, or interpreted), because its starting point are program binaries. In practice, however, it is mostly used for programs written in C and C++.

* **Supported platforms** &mdash; Primarily Unix descendants, including Linux, BSD, MacOS, Android, Solaris, etc (see the full list at this [link](https://valgrind.org/info/platforms.html)). Windows is not supported because porting the existing code to it is neither easy nor straightforward.

* **Tools** &mdash; The most important Valgrind tools are **Memcheck**, **Cachegrind**, **Callgrind**, and **Massif**, but there are many other ones available (see the full list at this [link](https://valgrind.org/info/tools.html)). For instance, memory-management problems (e.g. memory leaks) can be detected with the **Memcheck** tool, and it can be used within Valgrind with the following example syntax:

  ```bash
  $ valgrind --tool=memcheck someExecutable
  ```

  On the other hand, to detect with **Massif** which parts of the program are responsible for the most memory allocation (so-called _heap profiling_), one can use the following syntax:

  ```bash
  $ valgrind --tool=massif someExecutable
  ```

  and so on for other tools. In this lecture, the usage of Valgrind will be primarily demonstrated through the usage of **Memcheck** and **Massif**.





### 2. A bit of history <a name="history"></a>

The original author of Valgrind is Julian Seward, and the initial release appeared in 2002. The name is pronounced as "val-grinned" and it originates from the Nordic mythology: Valgrind is the name of the main entrance to Valhalla (the Hall of the Chosen Slain in Asgard, "grind" means "gate" in Norwegian). Contrary to frequent misconception, the name Valgrind is not short for "value grinder" (even though one can see it that way...).

Valgrind is written in C and is actively maintained and developed &mdash; its online source code repository can be found at this [link](https://sourceware.org/git/valgrind.git). As of October 2025, the latest stable release is version ```3.26.0```.





### 3. Installation <a name="installation"></a>

By default, **valgrind** is not installed on Linux distributions. To install the currently supported version for a given Linux distribution, one can proceed by using the standard packaging tools for that distribution, e.g. **apt** ("Advanced Package Tool") on Ubuntu:

```bash
# Install default valgrind version with admin privileges:
$ sudo apt install valgrind

# Check your valgrind version:
$ valgrind --version
valgrind-3.18.1
```

However, there are cases when the custom **valgrind** version needs to be compiled from source (e.g. when a newer version is required than the one currently shipped by default on a given Linux distribution). The list of available **valgrind** versions and the latest releases can be obtained from the following [link](https://valgrind.org/downloads/) at the Valgrind official website, of from the Valgrind [online](https://sourceware.org/git/?p=valgrind.git;a=summary) source code repository.

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




### 4. Memory management: **Memcheck** <a name="memcheck"></a>





### 5. Heap profiling: **Massif** <a name="massif"></a>





### TBI. References <a name="references"></a>

* "_Valgrind Unlocked: Hands‑On Memory Debugging and Performance Profiling for C and C++_", William E. Clark
  * This book was the main reference used in preparing the **valgrind** part of this lecture
* Valgrind website: https://valgrind.org/
* Valgrind repository: https://sourceware.org/git/valgrind.git
* Wikipedia: https://en.wikipedia.org/wiki/Valgrind