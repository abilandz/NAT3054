<img src="make_cmake.png" alt="drawing" width="600"/>

# make & cmake

**Last update**: 20251010-2


### Table of Contents

1. [Introduction](#introduction)
2. [Makefile](#makefile)
3. [Shared libraries](#shared.libraries)
4. [References](#references)





### 1. Introduction <a name="introduction"></a>
The command-line utility **make** is used in the development of large-scale projects consisting of multiple source files, which must be compiled and linked together to create a single executable file. One finds such a modus operandi, for instance, in major collaborations at the Large Hadron Collider, where several hundred developers concurrently develop the analysis framework for a given experiment. 

One can see immediately one potential caveat — would it be necessary to recompile all source files, if there was a change in only one of them? This would lead to a tremendous loss of efficiency during code development, as recompiling a large-scale project from scratch typically takes several hours, even on very powerful computers. An obvious solution (that existed already in the 1970s) would be to use a **linker**: recompile only changed files, and link with previously compiled files. However, in practice, this approach is error-prone, because if several source files were modified, frequently one forgets to recompile at least one of them, which leads either to compilation errors, or pointless debugging sessions (a bug was fixed, but the code wasn't recompiled). In the past, solving this problem was accomplished with carefully written shell scripts, always specific to the project in question. Since this problem was reoccuring all large-scale projects, there was a need for a general solution. This is precisely how the command-line utility **make** originated. 

**Historical note**

The first version of **make** was developed by Stuart Feldman in April 1976, in the C programming language, after he and one of his colleagues at Bell Labs (New Jersey, US) spent several hours in the same week debugging the correct source code, by simply forgetting to recompile it after the bug was fixed. Motivated by endless frustration, Stuart Feldman immediately implemented the first version of **make** over the weekend, with infamous "tab-in-column-1" syntax (more on this below!). The very next weekend, the second version of **make** was rewritten from scratch. However, by then, 10+ collaborators at Bell Labs had already picked up the idea and started using the first version of **make** during the week &mdash; "tab-in-column-1" syntax remained in the code, ensuring backward compatibility was not broken.

There are several major implementations of **make** nowadays:
- GNU **make** &mdash; used in this lecture
- BSD **make**
- Microsoft **nmake**

While all implementations of **make** share the same basic ideas and goals, their syntax is frequently incompatible.

**The key idea behind 'make'**

Automatic detection of source files that have been modified can be accomplished from the file's metadata, in particular from the file's _mtime_ flag. File metadata refers to any file-related information beyond its content. There are three _timestamps_ as a part of the file's metadata, with the following meaning:  

* **Access (atime)** : last time a file was accessed (opened) and read without any modification   
* **Modify (mtime)** : last time a file was modified (i.e. its content has been edited)
* **Change (ctime)** : last time a file's metadata was changed (e.g. permissions)  

These three timestamps are not overkill, in fact, they enable a lot of compelling features. For each file, its metadata can be displayed with the **stat** command:

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
# Print time of last data modification, human-readable format:
$ stat -c %y Lecture_2.md
2020-04-28 11:44:53.454187100 +0200

# Print time of last data modification, in seconds since Unix epoch:
$ stat -c %Y Lecture_2.md
1588067093
```

These flags are instantly updated for each file by the underlying operating system. This can cause a lot of stress on the system, however, and to improve overall performance and to prevent disk wear, most Linux distributions disable the _atime_ ('Access') flag from being regularly updated.

The key benefits of **make**:

- Compilation is as efficient as possible — only modified source files are recompiled;
- Trivial errors of forgetting to recompile the modified source file, with important bugs fixed, is completely eliminated;
- Solution for automation is general and it can be used for any programming language whose compiler can be run with a shell command (or more generically, for any project where some files must be updated automatically from others whenever the others change);
- Declarative specification language written in the so-called _makefiles_.










### 2. Makefile <a name="makefile"></a>

Before using **make**, one must write a file called *makefile* that describes the relationships among files in your project and provides commands for updating each file. Once the _makefile_ is written, **make** uses that information and compares the _mtime_ flags of two files against each other. In **make**'s parlance, these two files are called _source_ and _target_.  If the source's _mtime_ flag is greater than the target's _mtime_ flag, then the target needs to be rebuilt. 

The content of the _makefile_ may look as follows:

```makefile
target ... : prerequisites ...
             recipe
             ...
             ...
```

or as follows:

```makefile
target : source1 source2 ...
	commands to make target
```

This syntax essentially says: For *target* to be up to date, it must be newer than all of the sources. If it's not, run the commands to bring it up to date. The commands are on one or more lines that must start with TABs, and NOT with equivalent number of spaces. 



TBI 20251010 Comment that make is checking only the timestamp difference between _target_ and _source_, i.e. ``touch sourceFile`` will trigger the default action, even if the file content is the same.

TBI 20251010 make make silent: running make in ```--silent``` mode will do it, as will prefixing every command with ```@```  + add example from SO how to use .SILENT in _makefile_

TBI 20251010 finalize this part (to I have to use TAB syntax also in this generic example?)



TBI 20251010 improve and embellish this example:

Content of _test1.C_:

```c
#include <stdio.h>
int main()
{
 printf("\nHi thereeee, from test1, again, again! Compilation time was: on %s at %s\n\n",__DATE__,__TIME__);
 return 0; 
}
```

Content of _test2.C_:

```c
#include "stdio.h"
int main()
{
 printf("\nHi there, from test2, again!\n\n");
 return 0; 
}
```

Content of _makefile_:

```makefile
all : test1 test2
test1 : test1.C
	@gcc test1.C -o test1 && echo compilation succeeded || echo compilation failed
	@ls -alt test1
test2 : test2.C
	gcc test2.C -o test2
run :
	./test1 && ./test2
clean :
	rm test1 test2
```



hit make + TAB + TAB ⇒ I get a list of all actions defined in the makefile in PWD

TBI 20250909 unify notation below with the one I used in "history" section of PH8124 

```bash
$ make + TAB +TAB
all    clean  run    test1  test2
```







### 3. Shared libraries <a name="shared.libraries"></a>

Libraries are pre-existing code that is compiled and ready to use. When a logically distinct set of functions is available, it is helpful to build a library from that set of functions so that the same source code doesn't have to be copied in the current project and recompiled all the time. If a bug fix or new feature has to be implemented in a given function, this has to be done only in one place. There are two types of libraries:

- _static_ &mdash; the actual library is placed in the final program during compilation;
- _shared_ &mdash; only a reference to the library is placed inside the final program (i.e. program is _linked_ with a library).

A static library is commonly stored in a file with an extension ```.a```, while a shared library in a file with ```.so``` extension. The main disadvantage of static libraries is the code bloat and the resulting waste of disk space, because the very same code with pre-compiled functions appears in different programs. In addition, if a change is introduced in a static library, all programs using that library must be recompiled. On the other hand, programs linked with shared libraries do not need to be recompiled when changes are introduced in those libraries &mdash; only the libraries need to be recompiled. When it comes to performance, programs using static libraries will run slightly faster, because all the symbols in the library are already resolved at compile time (with shared libraries, they need to be resolved at run time). Once compiled, programs using static libraries no longer depend on those libraries, which removes the external dependency on library version (this is particularly relevant when a major upgrade of the underlying operating system is performed, during which most libraries are updated to a newer version). In what follows next, we focus on shared libraries, using as an example code written in C/C++ programming language, and compiled via the open-source **gcc** compiler (originally, _GNU C Compiler_, lated renamed into _GNU Compiler Collection_).

The stages needed in the project development utilizing shared libraries can be delineated as follows:

1. _Source code_ &mdash; the standard code development from scratch.
2. _Preprocessor_ &mdash; this stage deals with all the preprocessor directives, to programmatically modify the source code and make it ready for compilation. For instance, in the C/C++ programming language, this step amounts to processing all lines in the source code that start with a ```#```, such as ```#define```, ```#include```, etc. If in the source code there is a line in the preamble ```#include <someHeaderFile.h>```, the preprocessor will literally inline the content of the header file ```someHeaderFile.h``` into that source code. No code compilation occurs at this stage, only programmatic manipulation of source code via the preprocessor. 
3. _Compilation_ &mdash; once the source file has been preprocessed, the compilation takes place over the modified source code. In the C/C++ programming language, at this stage, the **gcc** compiler turns the source code from ```.c``` or ```.cxx``` files into an ```.o``` (object) files. An object file contains machine code specific to the underlying hardware, and it's ready to be included via linking in a final executable (but typically cannot be executed directly).
4. _Linking_ &mdash; at this stage all of the object files and shared libraries are linked together to make the final executable, that is ready to run. The executable can be started in the terminal from the shell, and is then handed off to the loader.
5. _Loading_ &mdash; this stage happens when the program starts up. The program is scanned for references to shared libraries, and any references found are resolved and the shared libraries are mapped into the program. This way, only at runtime, different programs re-use exactly the same pre-compiled code stored in the shared libraries. TBI 20250916 improve the wording further here
6. _Build_ &mdash; All stages above put together.

All stages above are now illustrated with a simple example, in which a shared library is made for some functions, and then used afterward in a program. TBI 20250916 improve the wording further here



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

We had to add a line ```#include <stdio.h>```, so that we can use a function **printf** from the standard library ```stdio.h```. With the notation ```< ... >``` we indicate that this header will be taken from one of the standard locations in the filesystem where header files are stored (typically, ```/usr/include```). On the other hand, with notation ```" ... "``` we indicate that the header file is taken from the current working directory. In case of a doubt, we can always specify instead in the source code the full path to the header file. 

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

In this exercise, we will make a library for functions implemented in ```functions.cxx```, and demonstrate how to use that library in the executable **test** obtained after compiling ```test.cxx```. TBI 20251009 shall I move this sentence before the code block?



**Step 2: Compilation**

For compilation of the source code, we use the **gcc** compiler, and we have to compile using the flag ```-fpic``` to create position independent code (this flag is mandatory for shared libraries, because the generated machine code will not be dependent on a specific address in memory, which is important when several shared libraries are loaded simultaneously in the memory):

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

The compilation step produced a new object file named _functions.o_, which contains the machine (or binary) code, and whose content cannot be inspected with the standard editors (if curious, try nevertheless **cat functions.o** &mdash; you will get mostly incomprehensible sequence of non-printable characters on the screen).



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
# Compile and link, telling gcc that the shared library "libfunctions.so" is in PWD:
gcc -L $PWD -Wall -o test test.cxx -l functions
```

We have now successfully linked our executable **test** with the pre-compiled shared library _libfunctions.so.



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

This becomes particularly beneficial if we have compiled our main programme against several hundreds external shared libraries. TBI 20250918 Add some more text here in conclusion









### 4. References <a name="references"></a>
* _"UNIX A History and a Memoir"_, Brian Kernighan
  * Section TBI 20250909:
* "GNU make" Manual is available at this [link](https://www.gnu.org/software/make/)
* Online resources on shared libraries can be found at this [link](https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html )
