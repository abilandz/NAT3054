<img src="make_cmake.png" alt="drawing" width="600"/>

# make & cmake

**Last update**: 20250915-2


### Table of Contents

1. [Introduction](#introduction)
2. [Makefile](#makefile)
3. [References](#references)





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








### 3. References <a name="references"></a>
* _"UNIX A History and a Memoir"_, Brian Kernighan
  * Section TBI 20250909: Regular expressions 
