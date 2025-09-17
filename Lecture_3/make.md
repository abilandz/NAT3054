<img src="make_cmake.png" alt="drawing" width="600"/>

# make & cmake

**Last update**: 20250917


### Table of Contents

1. [Introduction](#introduction)
2. [Makefile](#makefile)
3. [Shared libraries](#shared.libraries)
4. [References](#references)





### 1. Introduction <a name="introduction"></a>
The command-line utility **make** is used in the development of large-scale projects consisting of multiple source files, which have to be compiled and linked together to make one common executable file. 

**TBI 20250909 mention here real-life physics examples, e.g. aliroot, cbmroot, O2Physics, etc.**

One can see immediately one caveat — do we have to re-compile all source files, if there was a change in only one of them? This would lead to the tremendous loss of efficiency during the code development, because re-compiling from scratch a large-scale project typically takes several hours, even on very powerful computers.
- Obvious solution (existed already in the 1970s): **linker** ⇒ recompile only changed files, and link with previously compiled files
- TBI 20250906 add an example for this
    - However, this is not perfect either: What if one changed several sources files, and forgot to recompiled only one of them? ⇒ **make**
    - History note: the first version of ‘make’ was developed by Stuart Feldman in April 1976, in the C programming language, after he and one of his colleagues spent hours debugging the correct source code, by simply forgetting to recompile the code after the bug was fixed.
- v1 : implemented over the weekend with infamous “tab-in-column-1” syntax
- v2 : rewritten from scratch next weekend, but already 10+ people picked up the idea and started using ‘v1’ of ‘make’ during the week, and “tab-in-column-1” syntax remained also in v2, so that backward compatibility is maintained
- There are several major implementations of ‘make’ nowadays
    - GNU ‘make’ ⇒ used in this lecture
    - BSD ‘make’
    - Microsoft ‘nmake’
    - The key idea: automate checking of ‘mtime’ metadata flag (’gives the time when the file was last changed’)
- TBI 20250906 add some example with ‘stat’ + remark that ‘atime’ flag is not reliable (I have the paragraph below)
    - The key benefits of ‘make’
- Compilation is as efficient as possible — only changes are re-compiled
- Trivial errors of forgetting to recompile the changed code with fixed bugs, is completely eliminated
    - How does ‘make’ work?
- declarative specification language written in the ‘makefile’




### 2. Makefile <a name="makefile"></a>

**TBI 20250909 I forgot from where I took this text**
Makefiles compare the mtimes of two files against each other.  Source and target.  If the source's mtime is greater than the target's mtime, then the target needs to be rebuilt. Most Linux distributions these days are disabling or half-disabling the atime field at the file system mount-option level, because of the tremendous inefficiency and wear on disks that it creates.



Example from my local Tutorials:

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



hit make + TAB + TAB ⇒ I get a list of all actions defined in the makefile in PWD ⇒ !! BEAUTIFULL !!

TBI 20250909 unify notation below with the one I used in "history" section of PH8124 

```bash
$ make + TAB +TAB
all    clean  run    test1  test2
```



### 3. Shared libraries <a name="shared.libraries"></a>

Libraries are pre-existing code that is compiled and ready to use. When a logically distinct set of functions is available, it is helpful to build a library from that set of functions so that the same source code doesn't have to be copied in the current project and recompiled all the time. If a bug fix or new feature has to be implemented in a given function, this has to be done only in one place. There are two types of libraries:

- _static_ &mdash; the actual library is placed in the final program during compilation;
- _shared_ &mdash; only a reference to the library is placed inside the final program (i.e. program is _linked_ with a library).

A static library is commonly stored in a file with an extension ```.a```, while a shared library is in a file with ```.so``` extension. The main disadvantage of static libraries is the code bloat and the resulting waste of disk space, because the very same code with compiled functions appears in different programs. In addition, if a change is introduced in a static library, all programs using that library must be recompiled. On the other hand, programs linked with shared libraries do not need to be recompiled when changes are introduced in those libraries &mdash; only the libraries need to be recompiled. When it comes to performance, programs using static libraries will run slightly faster, because all the symbols in the library are already resolved at compile time (with shared libraries, they need to be resolved at run time). Once compiled, programs using static libraries no longer depend on those libraries, which removes the external dependency on library version (this is particularly relevant when a major upgrade of the underlying operating system is performed, during which most libraries are updated to a newer version). In what follows next, we focus on shared libraries, using as an example code written in C/C++ programming language, and compiled via the open-source **gcc** compiler (originally, _GNU C Compiler_, lated renamed into _GNU Compiler Collection_).

The stages needed in the project development utilizing shared libraries can be delineated as follows:

1. _Source code_ &mdash; the standard code development from scratch.
2. _Preprocessor_ &mdash; this stage deals with all the preprocessor directives, to programmatically modify the source code and make it ready for compilation. For instance, in the C/C++ programming language, this step amounts to processing all lines in the source code that start with a ```#```, such as ```#define```, ```#include```, etc. If in the source code there is a line in the preamble ```#include <someHeaderFile.h>```, the preprocessor will literally inline the content of the header file ```someHeaderFile.h``` into that source code. No code compilation occurs at this stage, only programmatic manipulation of source code via the preprocessor. 
3. _Compilation_ &mdash; once the source file has been preprocessed, the compilation takes place over the modified source code. In the C/C++ programming language, at this stage, the **gcc** compiler turns the source code from ```.c``` or ```.cxx``` files into an ```.o``` (object) files. An object file contains machine code specific to the underlying hardware, and it's ready to be included via linking in a final executable (but typically cannot be executed directly).
4. _Linking_ &mdash; at this stage all of the object files and shared libraries are linked together to make the final executable, that is ready to run. The executable can be started in the terminal from the shell, and is then handed off to the loader.
5. _Loading_ &mdash; this stage happens when the program starts up. The program is scanned for references to shared libraries, and any references found are resolved and the shared libraries are mapped into the program. This way, only at runtime, different programs re-use exactly the same pre-compiled code stored in the shared libraries. TBI 20250916 improve the wording further here
6. _Build_ &mdash; All stages above put together.

All steps above are now illustrated with a simple example, in which a shared library is made for some functions, and then used afterward in a program. TBI 20250916 improve the wording further here



**Step 1: Source code**

First, we place all function declarations in the header file ```functions.h```, with the following content:

```C
void Hello();
void Hallo();
```

For each function declared in the header file, we provide the implementation in the corresponding file ```functions.cxx```:

```c
#include <stdio.h>
#include "functions.h"

void Hello()
{
 printf("\nHello, how is life?\n\n");
}
void Hallo()
{
 printf("\nHallo, wie geht's dir Heute?\n\n");
}
```

We had to add a line ```#include <stdio.h>```, so that we can use a function **printf** from the standard library ```stdio.h```. Finally, the main program (executable) is in the file ```test.C```, and it is implemented as follows:

```c
#include <stdio.h>
#include "functions.h"

int main()
{
 puts("This is a shared library test...");
 Hallo();
 return 0;
}
```



**Step 2: Compilation**

For compilation of the source code, we use **gcc** compiler, and we compile with position independent code (TBI 20250917 clarify), as follows:

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

The compilation step produced a new object file _functions.o_, which contains the machine code, and whose content cannot be inspected with standard editors (if curious, try nevertheless **cat functions.o** &mdash; you will get only incomprehensible sequence of non-printable characters on the screen).



**Step 3: Creating a shared library from an object file**

TBI 20250917 add intro sentence here

```bash
$ gcc -shared -o libfunctions.so functions.o
$ ls
functions.cxx  functions.h  functions.o  libfunctions.so
```

This step produced a shared library in the file _libfunctions.so_, which also contains the machine code (or binary code).

  

**Step 4: Linking with a shared library**

Let us compile our main program written in the file _test.C_ and link it with shared library in the file _libfunctions.so_. We will call our final executable **test**. 

```bash
# Compile and link:
$ gcc -Wall -o test test.C -l functions
/usr/bin/ld: cannot find -l functions
collect2: error: ld returned 1 exit status
```

Note that the **-l functions** option is not looking for a file _functions.o_, but for _libfunctions.so_. Namely, **gcc** assumes that all libraries start with prefix ```lib``` and end with a file extension ```.so``` (for shared libraries) or ```.a``` (for static libraries). That being written, the option **-l functions.so** would also lead to an error, because **gcc** will be looking for shared library in a file _libfunctions.so.so_. 

However, we got an error. The linker **ld** does not know where to find the shared library _libfunctions.so_ (Remark: **gcc** merely acts as a front-end to **ld** at link time). The **gcc** has a list of places it looks by default for the libraries, but our current working directory is not in that list. By default, **gcc** searches for libraries first in ```/usr/local/lib```, and then in ```/usr/lib``` (but this may vary from one system to another). After that, it searches for libraries in the directories specified by the -L option, in the order specified on the command line. 

```bash
# Compile and link, telling gcc that the shared library "libfunctions.so" is in PWD:
gcc -L $PWD -Wall -o test test.C -l functions
```

We have now successfully linked our executable **test** with the pre-compiled shared library _libfunctions.so_.

TBI 20250917 Use still somewhere in this section here this:

```bash
 -l LIBNAME, --library LIBNAME
               Search for library LIBNAME

 -L DIRECTORY, --library-path DIRECTORY
               Add DIRECTORY to library search path
```



**Step 5: Loading the shared library at runtime and executing the main programme**

However, if we attempt after compilation and linking to execute **test**, we get a new error:

```bash
$ ./test
./test: error while loading shared libraries: libfunctions.so: cannot open shared object file: No such file or directory
```

Now the loader cannot find the shared library. Again, the problem is that the shared library is not in any of the standard locations, so we need to give the loader a custom location of directory. The easiest it to use the environment variable **LD_LIBRARY_PATH**, for instance:

```bash
# add new location, in this example PWD, to LD_LIBRARY_PATH:
export LD_LIBRARY_PATH=${PWD}:${LD_LIBRARY_PATH}
```

**Remark: It has to be exported!!** TBI 20250917 clarify perhaps why

**LD_LIBRARY_PATH** is great for quick tests and for systems on which you do not have admin privileges. As a downside, however, exporting the **LD_LIBRARY_PATH** variable means it may cause problems with other programs you run that also rely on **LD_LIBRARY_PATH** if you do not reset it to its previous state when you are done.

TBI 20250917 an alternative is to use **rpath** => do I want to add that as well? On Ubuntu, I do not have it installed by default, so most likely not.

Finally, we are ready to run:

```bash
# Start the main programme:
$ ./test
This is a shared library test...

Hallo, wie geht's dir Heute?
```



**Step 6: Introduce a change in the shared library**

```c
#include <stdio.h>
#include "functions.h"

void Hello()
{
 printf("\nHello, how is life?\n\n");
}
void Hallo()
{
 printf("\nHallo, wie geht's dir Heute? TBI\n\n");
}
```

Recompile again object file + shared library TBI 20250917 improve the wording

Finally, the main point &mdash; execute the main programme WITHOUT recompiling:

```bash
$ ./test
This is a shared library test...

Hallo, wie geht's dir Heute? TBI
```

TBI 20250917 improve the wording here and there.

TBI 20250917 shall I also add the section for static libraries?





### 4. References <a name="references"></a>
* _"UNIX A History and a Memoir"_, Brian Kernighan
  * Section TBI 20250909: Regular expressions 
* Online resource on shared libraries: https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html  TBI 20250519 improve this link
