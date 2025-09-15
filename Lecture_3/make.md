<img src="make_cmake.png" alt="drawing" width="600"/>

# make & cmake

**Last update**: 20250915-3


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



Libraries are pre-existing code that is compiled and ready to use. 

o use for later

o separate out the code for organizational purposes

When you have a reusable or logically distinct set of functions, it is helpful to build a library from it so that you do not have to copy the source code into your current project and recompile it all the time - and so you can keep different modules of your program disjoint and change one without affecting others. Once it is been written and tested, you can safely reuse it over and over again, saving the time and hassle of building it into your project every time.

o static and shared libraries: Note that for static libraries, the actual library is placed in your final program, while for shared libraries, only a reference to the library is placed inside.

o everything that happens from source code to running program:

1. C Preprocessor: This stage processes all the [preprocessor directives](https://www.cprogramming.com/tutorial/cpreprocessor.html). Basically, any line that starts with a #, such as #define and #include.
2. Compilation Proper: Once the source file has been preprocessed, the result is then compiled. Since many people refer to the [entire build process](https://www.cprogramming.com/compilingandlinking.html) as compilation, this stage is often referred to as compilation proper. This stage turns a .c file into an .o (object) file.
3. Linking: Here is where all of the object files and any libraries are linked together to make your final program. Note that for static libraries, the actual library is placed in your final program, while for shared libraries, only a reference to the library is placed inside. Now you have a complete program that is ready to run. You launch it from the shell, and the program is handed off to the loader.
4. Loading: This stage happens when your program starts up. Your program is scanned for references to shared libraries. Any references found are resolved and the libraries are mapped into your program.



Steps 3 and 4 are where the magic (and confusion) happens with shared libraries.

Let's make a shared library for some functions:

Step 1: implement some functions:

functions.h :

```C
void Hello();
void Hallo();
```

functions.cxx :

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

main.C

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



**Step 1: Compiling with Position Independent Code**

```bash
gcc -c -Wall -Werror -fpic functions.cxx
```

=> this step produced an object file **functions.o**

**Step 2: Creating a shared library from an object file**

```bash
gcc -shared -o libfunctions.so functions.o
```

**Step 3: Linking with a shared library**

Let us compile our main.C and link it with libfunctions. We will call our final program test. Note that the -**lfunctions** option is not looking for functions.o, but libfunctions.so. GCC assumes that all libraries start with lib and end with .so or .a (.so is for shared object or shared libraries, and .a is for archive, or statically linked libraries).

```bash
gcc -Wall -o test main.C -lfunctions
```

/usr/bin/ld: cannot find -lfunctions

collect2: error: ld returned 1 exit status

*** Telling GCC where to find the shared library***

The linker does not know where to find libfunctions. GCC has a list of places it looks by default, but our directory is not in that list.[2](https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html#fn:gcclist) We need to tell GCC where to find libfunctions.so. We will do that with the -L option. In this example, we will use the current directory /home/abilandz/Tutorials/sharedLibraries

```bash
gcc -L/home/abilandz/Tutorials/sharedLibraries -Wall -o test main.C -lfunctions
```



from ld man page: TBI 20250915 improve the spacing

```bash
 -l LIBNAME, --library LIBNAME
               Search for library LIBNAME

 -L DIRECTORY, --library-path DIRECTORY
               Add DIRECTORY to library search path
```



AB : Remark: -llibfunction.so doesn't work, it seems indeed that lib and .so are assumed



**Step 4: making the library available at runtime**

```bash
$ ./test
./test: error while loading shared libraries: libfunctions.so: cannot open shared object file: No such file or directory
```

The loader cannot find the shared library.[3](https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html#fn:loadorder) We did not install it in a standard location, so we need to give the loader a little help. We have a couple of options: we can use the environment variable LD_LIBRARY_PATH for this, or rpath.

a) **LD_LIBRARY_PATH**

**export LD_LIBRARY_PATH=/home/abilandz/Tutorials/sharedLibraries:${LD_LIBRARY_PATH}**

**Remark: It has to be exported!!**

./test

This is a shared library test...

Hallo, wie geht's dir Heute?

LD_LIBRARY_PATH is great for quick tests and for systems on which you do not have admin privileges. As a downside, however, exporting the LD_LIBRARY_PATH variable means it may cause problems with other programs you run that also rely on LD_LIBRARY_PATH if you do not reset it to its previous state when you are done.

**b) rpath TBI  20250915 do I need this? Check online reference below**



### 4. References <a name="references"></a>
* _"UNIX A History and a Memoir"_, Brian Kernighan
  * Section TBI 20250909: Regular expressions 
* Online resource on shared libraries: https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html  TBI 20250519 improve this link
