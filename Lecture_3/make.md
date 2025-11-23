<img src="make_cmake.png" alt="drawing" width="600"/>

# make & cmake

**Last update**: 20251123-1


### Table of Contents

1. [Introduction](#introduction)
2. [Makefile](#makefile)
3. [Shared libraries](#shared.libraries)
4. [The final step: **cmake**](#the.final.step.cmake)
5. [References](#references)





### 1. Introduction <a name="introduction"></a>
The command-line utility **make** is used in the development of large-scale projects consisting of multiple source files, which must be compiled and linked together to create a single executable file. One finds such a modus operandi, for instance, in major collaborations at the Large Hadron Collider, where several hundred developers concurrently develop the analysis framework for a given experiment. 

One can immediately see a potential caveat — would it be necessary to recompile all source files if there were a change in only one of them? This would result in a significant loss of efficiency during code development, as recompiling a large-scale project from scratch typically takes several hours, even on the most powerful computers. An obvious solution (that existed already in the 1970s) would be to use a **linker**: recompile only changed files, and link with previously compiled files. However, in practice, this approach is error-prone because if several source files are modified, it is frequently forgotten to recompile at least one of them, which leads to either compilation errors or pointless debugging sessions (a bug is fixed, but the code is not recompiled). In the past, solving this problem was accomplished through carefully written shell scripts, which were always specific to the project in question. Since this problem was recurring in all large-scale projects, there was a need for a general solution. This is precisely how the command-line utility **make** originated. 

**Historical note**

The first version of **make** was developed by Stuart Feldman in April 1976, in the C programming language, after he and one of his colleagues at Bell Labs (New Jersey, US) spent several hours in the same week debugging the correct source code, by simply forgetting to recompile it after the bug was fixed. Motivated by endless frustration, Stuart Feldman immediately implemented the first version of **make** over the weekend, with infamous "tab-in-column-1" syntax (more on this below!). The very next weekend, the second version of **make** was rewritten from scratch. However, by then, 10+ collaborators at Bell Labs had already picked up the idea and started using the first version of **make** during the week &mdash; "tab-in-column-1" syntax remained in the code, ensuring backward compatibility was not broken.

There are several major implementations of **make** nowadays:
- GNU **make** &mdash; used in this lecture
- BSD **make**
- Microsoft **nmake**

While all implementations of **make** share the same basic ideas and goals, their syntax is frequently incompatible.

**The key idea behind 'make'**

Automatic detection of source files that have been modified can be accomplished by examining the file's metadata, particularly the file's _mtime_ flag. File metadata refers to any information related to a file beyond its content. There are three _timestamps_ as a part of the file's metadata, with the following meaning:  

* **Access (atime)** : last time a file was accessed (opened) and read without any modification   
* **Modify (mtime)** : last time a file was modified (i.e. its content has been edited)
* **Change (ctime)** : last time a file's metadata was changed (e.g. file's permissions)  

These three timestamps are not overkill &mdash; in fact, they enable many compelling features. For each file, its metadata can be displayed with the **stat** command:

 ```bash
 $ stat Lecture_2.md # just specify the abs. or rel. path to file as an argument
   File: Lecture_2.md
   Size: 97805           Blocks: 384        IO Block: 4096   regular file
 Device: 2h/2d   Inode: 12947848928707821  Links: 1
 Access: (0666/-rw-rw-rw-)  Uid: ( 1000/abilandz)   Gid: ( 1000/abilandz)
 Access: 2020-04-15 21:05:26.002857000 +0200
 Modify: 2020-04-28 11:44:53.454187100 +0200
 Change: 2020-04-28 11:45:14.515681300 +0200
  Birth: -
 ```

To get specifically only the _mtime_ ('Modify') flag, one can use the following syntax:

```bash
# Print time of last data modification, in human-readable format:
$ stat -c %y Lecture_2.md
2020-04-28 11:44:53.454187100 +0200

# Print time of last data modification, in seconds since Unix epoch:
$ stat -c %Y Lecture_2.md
1588067093
```

These flags are instantly updated for each file by the underlying operating system. This can cause a lot of stress on the system, however, and to improve overall performance and to prevent disk wear, most Linux distributions disable the _atime_ ('Access') flag from being regularly updated.

The key benefits of **make**:

- Compilation is as efficient as possible — only modified source files are recompiled;
- Trivial errors of forgetting to recompile the modified source file (for instance, files with important bugs fixed) are completely eliminated;
- Solution for automation is general and it can be used for any programming language whose compiler can be run with a shell command (or more generically, for any project where some files must be updated automatically from others whenever the others change);
- Declarative specification language written in the so-called _makefiles_.










### 2. Makefile <a name="makefile"></a>

Before using **make**, one must write a file called *makefile* that describes the relationships among files in your project and provides commands for updating each file. Once the _makefile_ is written, **make** uses that information and compares the modification time _mtime_ flags of two files against each other. In **make**'s parlance, these two files are called _source_ and _target_. If the _source_'s _mtime_ flag is greater than the _target_'s _mtime_ flag (i.e., the _source_ was modified more recently than the _target_), then the _target_ needs to be rebuilt. 

The content of the _makefile_ may look as follows:

```makefile
target : source1 source2 ...
	commands to make target (a.k.a. recipes for this target)
```

This syntax essentially says: For the *target* to be up to date, it must be newer than all the _source_ files 'source1', 'source2', etc. If it is not, run the specified commands to bring the _target_ up to date. The commands are specified on one or more lines that must start with TABs (not with equivalent number of spaces &mdash; this is a common mistake!). This is the infamous "tab-in-column-1" syntax, introduced with the very first version of **make**, and it remained afterward to preserve backward compatibility for the original users, who started using **make** within days of its initial release.

A _target_ is usually the name of a file generated by **make** when it automatically recompiles all specified source files that have changed. However, it can also represent an _action_ that **make** will carry out directly. In that case, the _source_ does not need to be specified, and the typical syntax of a _makefile_ may look as follows:

```makefile
action : 
	commands executed for this action (a.k.a. recipes for this action)
```

By default, when **make** looks for the _makefile_, the **GNU** version of **make** tries the following names, with the following precedence: 'GNUmakefile', 'makefile' or 'Makefile'. In practice, you should call your _makefile_ either 'makefile' or 'Makefile', but if necessary, a custom name can be used with **make -f customMakeFile** or **make --file customMakeFile**. In what follows next, the content of _makefile_ is stored for simplicity in the file named 'makefile'. 

As it is customary, we can start with the 'Hello World' example for **make**, by having the following content in the _makefile_:

```makefile
# this is a comment
hello : 
	echo "Hello World"
```

If we are in the same directory where this _makefile_ was saved, we execute simply:

```bash
$ make hello
echo "Hello World"
Hello World
```

We can implement more commands under the same action 'hello':

```bash
$ cat makefile
# this is a comment
hello : 
	echo "Hello World"
	date

$ make hello
echo "Hello World"
Hello World
date
Sat Oct 11 15:34:23 CEST 2025
```

Or we can separate commands across multiple actions:

```bash
$ cat makefile
# this is a comment
hello : 
	echo "Hello World"
time :
	date
	
$ make hello
echo "Hello World"
Hello World

$ make time
date
Sat Oct 11 15:35:54 CEST 2025
```

We now illustrate what happens if the command for a given action is specified on a line that does not start with TAB:

```bash
$ cat makefile
hello : 
 echo "Hello World"

$ make hello
makefile:3: *** missing separator.  Stop.
```

This limitation can be overcome, if necessary, by using the special variable ```.RECIPEPREFIX```, more on this later. 

We now demonstrate how to, in a real-case scenario, write a _makefile_ and use **make** for the following simple project, which consists of two source files, named 'test1.C' and 'test2.C'. The content of 'test1.C' is:

```C++
#include <stdio.h>
int main()
{
 printf("\n Hi there, from test1! Compilation time was: on %s at %s \n", __DATE__, __TIME__);
 return 0;
}
```

The content of 'test2.C' is:

```C++
#include <stdio.h>
int main()
{
 printf("\n Hi there, from test2! Compilation time was: on %s at %s \n", __DATE__, __TIME__);
 return 0;
}
```

In the _makefile_, we implement the following content:

```makefile
all : test1 test2
test1 : test1.C
	gcc test1.C -o test1 && echo "compilation of test1 succeeded"
	ls -alt test1
test2 : test2.C
	gcc test2.C -o test2 && echo "compilation of test2 succeeded"
	ls -alt test2	
run :
	./test1 && ./test2
clean :
	rm test1 test2
```

All three files are placed in the same working directory:

```bash
# Show the current working directory:
$ ls
makefile  test1.C  test2.C
```

First, as an example, we compile separately only 'test1.C' into an object file 'test1'. From the above _makefile_, the relevant part is: 

```makefile
test1 : test1.C
	gcc test1.C -o test1 && echo "compilation of test1 succeeded"
	ls -alt test1
```

The **make** will interpret this as follows:

1. Compare the _mtime_ flags of a compiled object file 'test1' (_target_) and a specified file 'test1.C' (_source_);
2. If the _mtime_ flag of the file 'test1.C' is greater than the _mtime_ flag of the object file 'test1', execute the specified commands, namely:
   * Execute: ```gcc test1.C -o test1 && echo "compilation of test1 succeeded"```
   * Execute: ```ls -alt test1```

To achieve that, on the command line we execute:

```bash
$ make test1
gcc test1.C -o test1 && echo "compilation of test1 succeeded"
compilation of test1 succeeded
ls -alt test1
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:50 test1
```

However, if we re-execute the same command immediately, nothing will happen:

```bash
$ make test1
make: 'test1' is up to date.
```

We can either change something explicitly in the source code of 'test1.C', or simply directly update its _mtime_ flag with the **touch** command:

```bash
$ touch test1.C
$ make  test1
gcc test1.C -o test1 && echo "compilation of test1 succeeded"
compilation of test1 succeeded
ls -alt test1
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:51 test1
```

As we can see from the above printout, **make** is printing both the commands and the output of those commands. We can silent the printout of commands by using the flag ```--silent``` or its shorter version ``-s``:

```bash
$ touch test1.C
$ make --silent test1
compilation of test1 succeeded
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:52 test1 
```

Alternatively, if we want to silence differentially only specific commands, we can prefix only those commands with ```@```  in the _makefile_:

```makefile
test1 : test1.C
	gcc test1.C -o test1 && echo "compilation of test1 succeeded"
	@ls -alt test1
```

With such a modification in the _makefile_, we get:

```bash
$ touch test1.C
$ make test1
gcc test1.C -o test1 && echo "compilation of test1 succeeded"
compilation of test1 succeeded
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:53 test1
```

The line ```ls -alt test1``` is no longer shown in the printout, only its output, because we have silenced it by prepending ```@``` in front of it in the _makefile_.

To compile both 'test1.C' and 'test2.C', we proceed as follows:

```bash
$ touch test1.C test2.C
$ make all
gcc test1.C -o test1 && echo "compilation of test1 succeeded"
compilation of test1 succeeded
ls -alt test1
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:54 test1
gcc test2.C -o test2 && echo "compilation of test2 succeeded"
compilation of test2 succeeded
ls -alt test2
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:54 test2
```

Now we change the _mtime_ flag only of test1.C:

```bash
$ touch test1.C
$ make all
compilation of test1 succeeded
ls -alt test1
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:55 test1
```

As we can see, only the object file 'test1' was recompiled, because only the _mtime_ flag of the source code 'test1.C' has changed, and **make** has automatically determined this — this is the main benefit of using **make**.

Now we change the _mtime_ flag only of test2.C:

```bash
$ touch test2.C
$ make all
gcc test2.C -o test2 && echo "compilation of test2 succeeded"
compilation of test2 succeeded
ls -alt test2
-rwxr-xr-x 1 abilandz abilandz 15960 Oct 11 15:56 test2
```

In this case, only the object file 'test2' was recompiled, because only the _mtime_ flag of the source code 'test2.C' has changed.

We have implemented two additional actions in the makefile: **run** and **clean**. For the action **run**, we have in the _makefile_ the following definition:

```make
run :
	./test1 && ./test2
```

That means:

```bash
$ make run
./test1 && ./test2

 Hi there, from test1! Compilation time was: on Oct 11 2025 at 15:55:33

 Hi there, from test2! Compilation time was: on Oct 11 2025 at 15:56:38
```

And finally, to clean up the compiled object files, we have implemented the action **clean** in the _makefile_ via the following definition:

```makef
clean :
        rm test1 test2
```

We can execute this action as follows:

```bash
# List the content of the current working directory:
$ ls 
makefile  test1  test1.C  test2  test2.C

# Remove the object files:
$ make clean
rm test1 test2

# List again the content of the current working directory:
$ ls
makefile  test1.C  test2.C
```

Finally, one can list all implemented actions in the _makefile_ by executing **make** + TAB + TAB:

```bash
$ make + TAB +TAB
all    clean    run    test1    test2
```





####  Variables and wildcards in the makefile

Variables are defined and later used in the _makefile_ with the following syntax:

```makefile
someVariable = "Hello World"
hello :
	echo $(someVariable)
```

After executing:

```bash
$ make hello
echo "Hello World"
Hello World
```

Variable names are case-sensitive, and can be any sequence of characters not containing ```:```, ```#```, ```=```, or whitespace. An exception are variables beginning with ```.``` and an uppercase letter, which can have a special meaning to **make** itself (e.g. special variable ```.RECIPEPREFIX```).



The wildcard characters that can be used in a _makefile_ are ```*```, ```?``` and ```[ ... ]```, with the same meaning as in the Bash shell. For instance:

```makefile
# Remove all files with an extension .o:
clean:
	rm -f *.o
```









### 3. Shared libraries <a name="shared.libraries"></a>

Libraries are pre-existing code that is compiled and ready to use. When a logically distinct set of functions is available, it is helpful to build a library from that set of functions, so that the same source code doesn't have to be copied into the current project and recompiled repeatedly. If a bug fix or new feature needs to be implemented in a given function, it must be done only in one place. There are two types of libraries:

- _static_ &mdash; the actual library is placed in the final program during compilation;
- _shared_ &mdash; only a reference to the library is placed inside the final program (i.e. program is _linked_ with a library).

A static library is commonly stored in a file with the extension ```.a```, while a shared library is stored in a file with the ```.so``` extension. The main disadvantage of static libraries is code bloat and the resulting waste of disk space, as the same code with pre-compiled functions appears in multiple programs. In addition, if a change is introduced in a static library, all programs using that library must be recompiled. On the other hand, programs linked with shared libraries do not need to be recompiled when changes are introduced in those libraries &mdash; only the libraries themselves need to be recompiled. When it comes to performance, programs using static libraries will run slightly faster, because all the symbols in the library are already resolved at compile time (with shared libraries, they need to be resolved at run time). Once compiled, programs using static libraries no longer depend on those libraries, which removes the external dependency on library version (this is particularly relevant when a major upgrade of the underlying operating system is performed, during which most libraries are updated to a newer version). In what follows next, we focus on shared libraries, using as an example code written in the C/C++ programming language, and compiled using the open-source **gcc** compiler (originally, _GNU C Compiler_, later renamed into _GNU Compiler Collection_).

The stages needed in the project development utilizing shared libraries can be delineated as follows:

1. _Source code_ &mdash; the standard code development from scratch.
2. _Preprocessor_ &mdash; this stage deals with all the preprocessor directives, to programmatically modify the source code and prepare it for compilation. For instance, in the C/C++ programming language, this step involves processing all lines in the source code that start with a ```#```, such as ```#define```, ```#include```, etc. If the source code contains a line in the preamble ```#include <someHeaderFile.h>```, the preprocessor will literally inline the content of the header file ```someHeaderFile.h``` into that source code. No code compilation occurs at this stage, only programmatic manipulation of source code via the preprocessor. 
3. _Compilation_ &mdash; once the source file has been preprocessed, the compilation takes place over the modified source code. In the C/C++ programming language, at this stage, the **gcc** compiler turns the source code from ```.c``` or ```.cxx``` files into an ```.o``` (object) files. An object file contains machine code specific to the underlying hardware, and it is ready to be included via linking in a final executable (but typically cannot be executed directly).
4. _Linking_ &mdash; at this stage, all of the object files and shared libraries are linked together to make the final executable, which is ready to run. The executable can be started in the terminal from the shell, and is then handed off to the loader.
5. _Loading_ &mdash; this stage happens when the program starts up. The program is scanned for references to shared libraries, and any references found are resolved; the shared libraries are then mapped into the program. This way, only at runtime, different programs re-use exactly the same pre-compiled code stored in the shared libraries.
6. _Build_ &mdash; All stages above combined.

All stages above are now illustrated with a simple example, in which a shared library is created for specific functions and then used in a program afterward.



**Step 1: Source code**

First, we place all function declarations in the header file ```functions.h```, with the following content:

```C
void Hello();
void Bye();
```

For each function declared in the header file, we provide its implementation in the corresponding file ```functions.cxx```:

```c
#include <stdio.h>
#include "functions.h"

void Hello() {
  printf("\n Hello, how is life? \n");
}
void Bye() {
  printf("\n See you later! \n");
}
```

We had to add a line ```#include <stdio.h>```, so that we can use the function **printf** from the standard library ```stdio.h```. With the notation ```< ... >``` we indicate that this header will be taken from one of the standard locations in the filesystem where header files are stored (typically, ```/usr/include```). On the other hand, with the notation ```" ... "```, we indicate that the header file is located in the current working directory. In case of doubt, we can always specify the full path to the header file in the source code instead. 

Finally, the main program (executable) is in the file ```test.cxx```, and it is implemented as follows:

```c
#include <stdio.h>
#include "functions.h"

int main() {
  puts("This is a shared library test...");
  Hello();
  Bye();  
  return 0;
}
```

In this exercise, we will make a library for functions implemented in ```functions.cxx```, and demonstrate how to use that library in the executable **test** obtained after compiling ```test.cxx```.



**Step 2: Compilation**

For compilation of the source code, we use the **gcc** compiler, and we have to compile using the flag ```-fpic``` to create position-independent code (this flag is mandatory for shared libraries, because the generated machine code will not be dependent on a specific address in memory, which is important when several shared libraries are loaded simultaneously in the memory):

```bash
# Check the content of current working directory:
$ ls
functions.cxx  functions.h

# Compile:
$ gcc -c -Wall -Werror -fpic functions.cxx

# Check again the content of current working directory:
$ ls 
functions.cxx  functions.h  functions.o 
```

The compilation step produced a new object file named _functions.o_, which contains the machine (or binary) code, and whose content cannot be inspected with the standard editors (if curious, try nevertheless **cat functions.o** &mdash; you will get a mostly incomprehensible sequence of non-printable characters on the screen).



**Step 3: Creating a shared library from an object file**

This step is straightforward:

```bash
$ gcc -shared -o libfunctions.so functions.o
$ ls
functions.cxx  functions.h  functions.o  libfunctions.so
```

As it can be seen above, this step produced a shared library in the file _libfunctions.so_, which contains the machine code.

  

**Step 4: Linking with a shared library**

Let us compile our main program from the source code _test.C_, by linking it with the shared library in the file _libfunctions.so_, to create our final executable named **test**:

```bash
# Compile and link:
$ gcc -Wall -o test test.cxx -l functions
/usr/bin/ld: cannot find -lfunctions
collect2: error: ld returned 1 exit status
```

The first attempt failed, but we use this failure to clarify a few non-trivial things which are happening at this step. First, note that the option **-l functions** is not looking for a file _functions.o_, but instead for a file _libfunctions.so_. Namely, **gcc** assumes that all libraries start with prefix ```lib``` and end with a file extension ```.so``` (for shared libraries) or ```.a``` (for static libraries). That being written, the option **-l functions.so** would also lead to an error, because **gcc** will be looking for shared library in a file _libfunctions.so.so_. 

We got a compilation error, because the linker **ld** does not know where to find the shared library _libfunctions.so_ (Remark: **gcc** compiler merely acts as a front-end to the linker **ld** at link time). The **gcc** has a list of directories it looks by default for the libraries, but our current working directory which contains the library _libfunctions.so_ is not on that list. By default, **gcc** searches for libraries first in ```/usr/local/lib```, and then in ```/usr/lib``` (but this may vary from one operating system to another). After that, it searches for libraries in the directories specified by the **-L** option, in the order specified on the command line. From documentation:

```bash
 -l LIBNAME, --library LIBNAME
               Search for library LIBNAME

 -L DIRECTORY, --library-path DIRECTORY
               Add DIRECTORY to library search path
```

Since our shared library _libfunctions.so_ is in the current working directory, we can disclose its location to **gcc** with the option **-L $PWD**:

```bash
# Compile and link, telling gcc that the shared library
# "libfunctions.so" is in PWD:
gcc -L $PWD -Wall -o test test.cxx -l functions
```

We have now successfully linked our executable **test** with the pre-compiled shared library _libfunctions.so_.



**Step 5: Loading the shared library at runtime and executing the main programme**

Before a program can be executed, the executable must be loaded from the disk into the primary memory (RAM). This is accomplished by the _loader_, an essential part of an underlying operating system that is responsible for loading programs and libraries into memory. However, if we attempt after compilation and linking to execute our final executable **test**, we get yet another error:

```bash
$ ./test
./test: error while loading shared libraries: libfunctions.so: cannot open shared object file: No such file or directory
```

Now the loader cannot find the shared library. Again, the problem is that the shared library is not in any of the standard locations, so we need to pass to the loader an information about the custom location of our library. The easiest way to accomplish this is to use the environment variable **LD_LIBRARY_PATH**, for instance:

```bash
# Add new location, in this example PWD, to LD_LIBRARY_PATH:
export LD_LIBRARY_PATH=${PWD}:${LD_LIBRARY_PATH}
```

In the above re-definition of environment variable **LD_LIBRARY_PATH**, we have appended its previous content. Otherwise, its redefinition may cause problems with other programs that also rely on **LD_LIBRARY_PATH**.

Finally, after redefinition of **LD_LIBRARY_PATH** we are ready to run:

```bash
# Start the main programme:
$ ./test
This is a shared library test...

 Hello, how is life? 

 See you later! 
```

In the next step, we illustrate the main point of using shared libraries.



**Step 6: Introduce a change in the shared library**

We now introduce some change in the source code of functions in the file _functions.cxx_:

```c
#include <stdio.h>
#include "functions.h"

void Hello() {
 // printf("\n Hello, how is life? \n"); // old version
 puts(" Hello from new version!");
}
void Bye() {
  // printf("\n See you later! \n"); // old version
  puts(" Hasta la vista!");
}
```

We recompile again only the functions:

```bash
# Recompile the object file:
$ gcc -c -Wall -Werror -fpic functions.cxx

# Recompile the shared library:
$ gcc -shared -o libfunctions.so functions.o
```

And finally, the main point &mdash; we can execute the main programme without recompiling it:

```bash
$ ./test
This is a shared library test...
 Hello from new version!
 Hasta la vista! 
```

This becomes particularly beneficial if we have compiled our main programme against many external shared libraries.

Finally, all the above steps are automated with the following example _makefile_:

```bash
workDir = ${PWD}

test : test.cxx
        gcc -L $(workDir) -Wall -o test test.cxx -l functions

fun : functions.o

functions.o : functions.cxx functions.h
        gcc -c -Wall -Werror -fpic functions.cxx
        gcc -shared -o libfunctions.so functions.o
        gcc -L $(workDir) -Wall -o test test.cxx -l functions
        export LD_LIBRARY_PATH=$(workDir):${LD_LIBRARY_PATH}
        ls -alt functions*

all : functions.o test

clean :
        cd $(workDir) && rm *.o

run :
        ./test
```

With such _makefile_, we can simply execute:

```bash
make all
```

If the source code of either 'functions.cxx' or 'functions.h' has been changed, **make** will automatically go through all steps needed to build a share library 'libfunctions.so', but the executable **test** won't be recompiled, because there were no changes in 'test.cxx'.

Vice versa, if there were changes only in the 'test.cxx', the executable **test** will be recompiled from scratch, but the same precompiled shared library 'libfunctions.so' will be used and linked at runtime, since there were no changes in neither 'functions.cxx' nor 'functions.h', 










### 4. The final step: **cmake** <a name="the.final.step.cmake"></a>

CMake ('cross-platform make') is an advanced software development tool used primarily to automate the creation of configuration files for standard native build tools, such as _makefiles_ for the **make**. It was first released in 2000 by Kitware, Inc., a technology company headquartered in Clifton Park, New York, with an initial focus on 3D biomedical imaging of the human body. 



#### Installing cmake

By default, **cmake** is not installed on most Linux distributions. To install the currently supported version for a given Linux distribution, one can proceed by using CMakethe standard packaging tools for that distribution, e.g. **apt-get** on Ubuntu:

```bash
# Install cmake as a root:
$ sudo apt-get install cmake

# Check your cmake version:
$ cmake --version
cmake version 3.22.1

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

In a case when the custom **cmake** version needs to be compiled (e.g. when a newer version is required than the one currently shipped by default on a given Linux distribution), one proceeds as follows:

```bash
# In case you have admin privileges, uninstall the default outdated 
# version which was shipped by the Linux package manager. 
# Othwerwise, skip this step:
$ sudo apt-get remove --purge --auto-remove cmake

# Download the custom version, e.g. 3.23.1 in some directory:
$ mkdir $HOME/cmake && cd $HOME/cmake
$ wget https://cmake.org/files/v3.23/cmake-3.23.1.tar.gz

# Decompress the downloaded tarball:
$ tar -xzvf cmake-3.23.1.tar.gz
$ cd cmake-3.23.1

# Configure:
$ ./bootstrap
---------------------------------------------
CMake 3.23.1, Copyright 2000-2022 Kitware, Inc. and Contributors
Found GNU toolchain
C compiler on this system is: gcc 

... many more lines ...

-- Configuring done
-- Generating done
-- Build files have been written to: /home/abilandz/cmake/cmake-3.23.1
---------------------------------------------
CMake has bootstrapped.  Now run make.

# Compile cmake using e.g. 4 CPUs:
$ make -j 4
[  0%] Building C object Source/kwsys/CMakeFiles/cmsys_c.dir/ProcessUNIX.c.o
[  0%] Building C object Source/kwsys/CMakeFiles/cmsys.dir/ProcessUNIX.c.o
[  1%] Building CXX object Utilities/std/CMakeFiles/cmstd.dir/cm/bits/fs_path.cxx.o
[  2%] Building C object Utilities/KWIML/test/CMakeFiles/kwiml_test.dir/test.c.o

... many more lines ...

[100%] Building CXX object Tests/CMakeLib/CMakeFiles/CMakeLibTests.dir/testCMExtAlgorithm.cxx.o
[100%] Linking CXX executable CMakeLibTests
[100%] Built target CMakeLibTests

# Check your custom cmake version:
$ ./bin/cmake --version
cmake version 3.23.1

CMake suite maintained and supported by Kitware (kitware.com/cmake).

# a) In case you have admin privilages, execute the command below,
# othwerwise, skip this step:
$ sudo make install

# b) If you do not have admin privilages, simply add new 
# install directory to PATH with higher precedence:
$ export PATH=$HOME/cmake/cmake-3.23.1/bin:$PATH
$ which cmake
/home/abilandz/cmake/cmake-3.23.1/bin/cmake

# In case the call to old version is still hashed by Bash 
# for quicker access, simply execute (this step is harmless in any case):
$ hash -d cmake

# Check which version of cmake is now the default one:
$ cmake --version
cmake version 3.23.1

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```



#### Building a standalone executable

As is customary, we start with the "Hello World!" example also for **cmake**. For that sake, the following C/C++ code snippet is used in the file "hello.cxx":

```c++
#include <stdio.h>
int main() {
  printf("\n Hello World! \n\n");
  return 0;
}
```

The directory structure of the project is organized as follows:

```bash
$ mkdir someProject
$ mkdir someProject/src # subdirectory for source code 
```

In the subdirectory "someProject/src", we place the above source code in the file "hello.cpp", while in the top directory "someProject", we place the **cmake** configuration file _CMakeLists.txt_ (or "CML" file for short) with the following content:

```cmake
# Set the oldest 'cmake' version with which the project can be built:
cmake_minimum_required(VERSION 3.22)

# Project name:
project(HelloWorld)

# Define a target:
add_executable(hello)

target_sources(hello
  PRIVATE
    src/hello.cxx
)
```

The command **cmake_minimum_required()** is mandatory, and it will check the version of the currently installed **cmake**. If that version is older than the one specified in the configuration file as a bare minimum to build the project, the following error message will be printed:

```cmake
CMake Error at CMakeLists.txt:3 (cmake_minimum_required):
  CMake 3.23 or higher is required.  You are running version 3.22.1
```

This can happen frequently, in fact, when running remotely on large-scale computing facilities, on which software is not updated too regularly. In that case, one needs to install the custom **cmake** version from source in the personal home directory, as explained in the previous section.

The **project()** command is also mandatory, and it tells **cmake** that what follows is the definition of a software project. In addition, it will steer **cmake** to perform various checks on the settings in the current environment (most notably, whether the necessary compilers are available, etc.).

The command **add_executable()** defines the _target_ to be built, for instance, the final executable of the project, which is obtained by compiling the specified source files.

Finally, the command **target_sources()** specifies all source files to be used when building an executable, which was already defined in the configuration file with the **add_executable()** command. The _scope keyword_ **PRIVATE** in the body of the command **target_sources()** indicates that the specified source files belong only to the executable "hello" in this example (i.e. they are not shared or inherited).

Given the above content of the configuration file _CMakeLists.txt_, we can proceed with configuring **cmake** by executing:

```bash
$ cd someProject
$ cmake -B build
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /home/abilandz/someProject/build
```

The flag ```-B``` instructs **cmake** to make a new subdirectory named "build" in the current project as the directory to generate and store files during the build process. In general, this is an important step to keep the source tree in the subdirectory "src" clean.

If we now inspect the content of "build", we find the following:

```bash
$ ls build
CMakeCache.txt  CMakeFiles  cmake_install.cmake  Makefile
```

As we can see, **cmake** generates automatically a lot of files related to the build process &mdash; most importantly, the _Makefile_ is generated automatically.

Finally, we can build the project, and we have to use the same "build" subdirectory as the command argument, as in the previous configuration step:

```bash
$ cd someProject
$ cmake --build build
[ 50%] Building CXX object CMakeFiles/hello.dir/src/hello.cxx.o
[100%] Linking CXX executable hello
[100%] Built target hello
```

Executable **hello** was built successfully, and is ready to be run:

```bash
$ ./build/hello 

 Hello World! 

```

In the next section, we cover more elaborate examples of using **cmake**, which show its full power.



#### Building a shared library

To build a library using **cmake**, we have to introduce a new command, namely **add_library()**.

TBI 20251123 finalize this example



#### Building a project

Finally, we demonstrate how the full-scale project consisting of the main executable and shared libraries can be built using **cmake**. To facilitate the procedure, we reuse the same project as in the previous sections, which was built by using **make**.

The project is structured as follows:

```
├── CMakeLists.txt
│   ├── test
│       ├── CMakeLists.txt
│       ├── test.cxx
│   ├── mySharedLibrary
│       ├── CMakeLists.txt
│       ├── functions.cxx
│       ├── functions.h
```

The source code of the main executable is in the file "test.cxx", and it will use at run time the shared library from the folder "mySharedLibrary". 

The content of "test.cxx" is as follows:

```C++
#include <stdio.h>
#include "mySharedLibrary/functions.h"

int main() {
  puts("This is a shared library test...");
  Hello();
  Bye();
  return 0;
}
```

The content of "functions.h" is:

```c++
void Hello();
void Bye();
```

Finally, the content of "functions.cxx" is:

```c++
#include <stdio.h>
#include "functions.h"

void Hello() {
  printf("\n Hello, how is life? \n");
}
void Bye() {
  printf("\n See you later! \n");
}
```

In this project, we have 3 configuration files "CMakeLists.txt", with the following content:

```cmake
# Set the oldest 'cmake' version with which the project can be built:
cmake_minimum_required(VERSION 3.22)

# Project name:
project(someProjectName)

add_subdirectory(test)
add_subdirectory(mySharedLibrary)
```

If some "CMakeLists.txt" files are located in subdirectories of the project, the **add_subdirectory()** command will incorporate them when **cmake** is executed for the main "CMakeLists.txt" file. The relative paths used in "CMakeLists.txt" in the subdirectory are relative to that subdirectory.

The content of "test/CMakeLists.txt" is:

```cmake
add_executable(test test.cxx)
target_link_libraries(test PUBLIC mySharedLibrary)
```

Finally, the content of "mySharedLibrary/CMakeLists.txt" is:

```cmake
add_library(
    mySharedLibrary SHARED
    functions.h
    functions.cxx
)

add_compile_definitions(LIBRARY_EXPORTS)
target_include_directories(mySharedLibrary PUBLIC "${PROJECT_SOURCE_DIR}")
```

TBI 20251123 add explanation of all new commands in CML files

Given the above structure and content of all files, the project can be readily built with:

```bash
$ cmake -B build
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /home/abilandz/NAT3054/cmake/project/build

$ cmake --build build
[ 25%] Building CXX object mySharedLibrary/CMakeFiles/mySharedLibrary.dir/functions.cxx.o
[ 50%] Linking CXX shared library libmySharedLibrary.so
[ 50%] Built target mySharedLibrary
[ 75%] Building CXX object test/CMakeFiles/test.dir/test.cxx.o
[100%] Linking CXX executable test
[100%] Built target test
```

Executable is in the build directory, and can be run as follows:

```bash
$ ./build/test/test
This is a shared library test...

 Hello, how is life?

 See you later!
```

TBI 20251123 add a statement that changing either executable or libraries, will only rebuild them differentially. Also, commend that more work is needed in CML, to move executables and shared libraries into common places (e.g. /bin or /lib folder/, etc.()





#### Compiling ROOT from source with cmake

In this example, it is demonstrated how the ROOT v6.32.06 can be built from source using **cmake**.  

```bash
# Make a directory where ROOT source code will be downloaded:
$ RootDir=$HOME/ROOT_v6-32-06
$ mkdir $RootDir && cd $RootDir

# Checkout the desired ROOT version:
$ git clone https://github.com/root-project/root.git
Cloning into 'root'...
remote: Enumerating objects: 1060392, done.
remote: Counting objects: 100% (1315/1315), done.
remote: Compressing objects: 100% (702/702), done.
remote: Total 1060392 (delta 886), reused 616 (delta 613), pack-reused 1059077 (from 3)
Receiving objects: 100% (1060392/1060392), 1.41 GiB | 39.94 MiB/s, done.
Resolving deltas: 100% (772069/772069), done.
Updating files: 100% (31068/31068), done.

$ cd root
$ git checkout v6-32-06
Updating files: 100% (22591/22591), done.
Note: switching to 'v6-32-06'.
... more information ...

# Make a build directory:
$ cd .. && mkdir build && cd build

# Configure with cmake before starting compilation:
$ cmake ../root
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
... more information ...
-- Configuring done
-- Generating done
-- Build files have been written to: /home/abilandz/ROOT_v6-32-06/build

# Finally, start building using e.g. 4 CPUs:
$ cmake --build . -- -j 4
[  0%] Creating directories for 'AFTERIMAGE'
[  0%] Creating directories for 'VDT'
[  0%] Creating directories for 'OPENUI5'
... many more lines ...
```






### 5. References <a name="references"></a>
* _"UNIX A History and a Memoir"_, Brian Kernighan
  * Section TBI 20250909:
* "GNU make" Manual is available at this [link](https://www.gnu.org/software/make/)
* ["CMake Tutorial"](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)
* "Mastering CMake Textbook" &mdash; an open source version is available at this [link](https://cmake.org/cmake/help/book/mastering-cmake/)
* Online resources on shared libraries can be found at this [link](https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html )
