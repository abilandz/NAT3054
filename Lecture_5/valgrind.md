<img src="Valgrind_logo.png" alt="drawing" width="600"/>

# Valgrind

**Last update**: 20260119


### Table of Contents

1. [Introduction](#introduction)
2. [A bit of history](#history)
3. [Installation](#installation)
4. [Memory management: **Memcheck**](#memcheck)
5. [Heap profiling: **Massif**](#massif)
6. [References](#references)





### 1. Introduction <a name="introduction"></a>

Valgrind is an advanced programming tool for debugging, memory management, memory-leak detection, and profiling of Linux programs. Its primary use case is to detect any sort of memory-related problems, but it also can be used to optimize and speed up program execution by determining bottlenecks at runtime. 

Valgrind uses the _dynamic binary instrumentation (DBI)_ technique, meaning that any executable can be inspected with Valgrind as it is (i.e. no code modification or recompilation is necessary). This particularly means that Valgrind can also be used for proprietary programs for which we do not have access to the source code at all. This comes with a price, however: when a program is examined by Valgrind, it will run slower by a factor of 5-100, depending which Valgrind tool is used. Nevertheless, this still pays off compared to endless manual debugging sessions ("guess and try recompilation", etc.).

A few additional remarks:

- **Supported programming languages** &mdash; Valgrind works with programs written in any programming language (compiled, just-in-time compiled, or interpreted), because its starting point are program binaries. In practice, however, it is mostly used for programs written in C and C++.

* **Supported platforms** &mdash; Primarily Unix descendants, including Linux, BSD, MacOS, Android, Solaris, etc., as supported operating systems by Valgrind (see the full list at this [link](https://valgrind.org/info/platforms.html)). Windows OS is not supported because porting the existing code to it is neither easy nor straightforward.

* **Tools** &mdash; The most important Valgrind tools are **Memcheck**, **Cachegrind**, **Callgrind**, and **Massif**, but many others are available (see the full list at this [link](https://valgrind.org/info/tools.html)). For instance, memory-management problems (e.g. memory leaks) can be detected with the **Memcheck** tool, and it can be used within Valgrind with the following example syntax:

  ```bash
  $ valgrind --tool=memcheck someExecutable
  ```

  On the other hand, to detect with **Massif** which parts of the program are responsible for the most memory allocation (so-called _heap profiling_), one can use the following syntax:

  ```bash
  $ valgrind --tool=massif someExecutable
  ```

  and so on for other tools. In this lecture, Valgrind will primarily be demonstrated through **Memcheck** and **Massif**.





### 2. A bit of history <a name="history"></a>

The original author of Valgrind is Julian Seward, and the initial release appeared in 2002. The name is pronounced as "val-grinned" and originates in Nordic mythology: Valgrind is the name of the main entrance to Valhalla (the Hall of the Chosen Slain in Asgard, "grind" means "gate" in Norwegian). Contrary to frequent misconception, the name Valgrind is not short for "value grinder" (even though one can see it that way...).

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

However, there are cases when the custom **valgrind** version needs to be compiled from source (e.g. when a newer version is required than the one currently shipped by default on a given Linux distribution). The list of available **valgrind** versions and the latest releases can be obtained from the following [link](https://valgrind.org/downloads/) on the Valgrind official website, or from the Valgrind [online](https://sourceware.org/git/?p=valgrind.git;a=summary) source code repository.

For instance, to compile the custom **valgrind** 3.26.0 from source, one proceeds as illustrated below, depending on whether one has admin privileges.

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

* shadow memory -- a replica of the application's memory space, typically defined with a mapping function from application memory addresses to shadow memory addresses.
  * It contains metadata for every byte of the application's addressable memory, encoding information about the initialization state and accessibility permissions of the corresponding application's data

* Each byte of the application's memory is associated with two main pieces of information:
  * _addressability tag_ &mdash; allocated, freed, unavailable, etc.
  * _definedness tag_ &mdash; initialized or uninitialized.

* **Memcheck** stores for each byte of the application's memory its addressability and definedness tags into the shadow memory, using its own representation. This is achieved by intercepting every memory read and write instruction of the application and using the DBI technique to dynamically translate and rewrite the executing program into shadow memory. During this process, additional code may be injected into the shadow memory. 
* Schematically, each memory access instruction of the application maps corresponds to the following action in the shadow memory:
  1. map the application memory address in the corresponding shadow memory address;
  2. for a **read** operation, load and verify addressability and definedness tags from shadow memory;
  3. for a **write** operation, mark the corresponding shadow memory byte as initialized and ensure it's addressable.

* The above causes a significant performance penalty. 

* For a **read** operation, the way **Memcheck** works by using the shadow memory can be represented with the following pseudo-code:

  ```C
  shadow_addr = map_to_shadow(addr);
  addressable = load_addressability_tag(shadow_addr);
  if (!addressable) {
  	report_error("Invalid read: memory not addressable!");    
  }
  defined = load_definedness_tag(shadow_addr);
  if (!defined) {
  	report_error("Use of unitialized memory!");    
  }
  load_real_memory(addr);
  ```

  and similarly for a **write** operation.
  
  

#### "Hello World!" example for Memcheck

First, the following perfectly regular code snippet is used

```C
#include <stdio.h>
int main() {
  printf("\n Hello World! \n\n");
  return 0;
}
```

The code is compiled into an executable **hello** in the standard way:

```bash
$ gcc -o hello hello.C
```

The executable produces the expected output:

```bash
$ ./hello

 Hello World!
 
```

We can now inspect the executable with **valgrind**'s tool **memcheck**:

```bash 
$ valgrind --tool=memcheck ./hello
==369== Memcheck, a memory error detector
==369== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==369== Using Valgrind-3.26.0 and LibVEX; rerun with -h for copyright info
==369== Command: ./hello
==369==

 Hello World!

==369==
==369== HEAP SUMMARY:
==369==     in use at exit: 0 bytes in 0 blocks
==369==   total heap usage: 1 allocs, 1 frees, 1,024 bytes allocated
==369==
==369== All heap blocks were freed -- no leaks are possible
==369==
==369== For lists of detected and suppressed errors, rerun with: -s
==369== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

We use this simple "Hello World!" example to make a few general statements:

1. If the flag ```--tool``` is not used to specify the tool explicitly, it defaults to **memcheck**, therefore executing bare **valgrind** or **valgrind --tool=memcheck** gives the same result.

2. The number "369" at the beginning of each line above indicates the PID of the process in which **valgrind** has run.

3. The performance penalty of executing **valgrind** can be demonstrated with the following comparison, using the built-in functionalities of **bash** shell:

    ```bash
    # measure the execution time of standalone executable:
    $ time for i in {1..100}; do ./hello &>/dev/null; done
    real    0m0.083s
    user    0m0.054s
    sys     0m0.028s
    
    # measure the execution time of standalone executable within valgrind:
    $ time for i in {1..100}; do valgrind ./hello &>/dev/null; done
    real    0m36.229s
    user    0m33.982s
    sys     0m2.203s
    ```

​	Several orders of magnitude, even for a simple executable like **hello**. TBI 20260117 finalize and embellish this comment

Since we used the canonical "Hello World!" example, **memcheck** found no errors.

Next, examples are provided of invalid memory accesses, i.e. of invalid read and write operations, which can be detected by the **memcheck** tool.

#### Out-of-bounds indexing

This error typically occurs when an array index is used beyond the array's boundaries, and if memory for that array was allocated on the heap (e.g. using the keyword **new** in ```C++```). For instance, in the following code snippet _outOfBound.C_:

```C  
int main() {

  float *arr = new float[2];
  arr[0] = 1.23;
  arr[1] = -1.44;
  arr[2] = 22.123; // out-of-bound indexing
  delete [] arr;

  return 0;
}
```

The above code snippet is compiled without any compilation error or warning into an executable in the following standard way: 

```bash
$ g++ -o outOfBound outOfBound.C
```

However, **memcheck** will report an error:

```bash
$ valgrind ./outOfBound
==8663== Memcheck, a memory error detector
==8663== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==8663== Using Valgrind-3.26.0 and LibVEX; rerun with -h for copyright info
==8663== Command: ./outOfBound
==8663==
==8663== Invalid write of size 4
==8663==    at 0x40011B7: main (in /home/abilandz/valgrind/examples/memcheck/outOfBound)
==8663==  Address 0x4de3c88 is 0 bytes after a block of size 8 alloc'd
==8663==    at 0x484F723: operator new[](unsigned long) (vg_replace_malloc.c:730)
==8663==    by 0x400117E: main (in /home/abilandz/valgrind/examples/memcheck/outOfBound)
==8663==
==8663==
==8663== HEAP SUMMARY:
==8663==     in use at exit: 0 bytes in 0 blocks
==8663==   total heap usage: 2 allocs, 2 frees, 72,712 bytes allocated
==8663==
==8663== All heap blocks were freed -- no leaks are possible
==8663==
==8663== For lists of detected and suppressed errors, rerun with: -s
==8663== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

Note, however, that **memcheck** doesn't check for out-of-bounds indexing of global arrays, or of array variables stored in a stack area:

```C
int globalArr[5];

int main(void)
{
  int stackArr[5];

  globalArr[5] = 0;
  stackArr[5] = 0;

  return 0;
}
```

If the above code snippet is saved in a file _globalArray.C_ and compiled, neither the **gcc** compiler nor **memcheck** finds any error:

```bash 
$ gcc -o globalArray globalArray.C
$ valgrind ./globalArray
==8577== Memcheck, a memory error detector
==8577== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==8577== Using Valgrind-3.26.0 and LibVEX; rerun with -h for copyright info
==8577== Command: ./globalArray
==8577==
==8577==
==8577== HEAP SUMMARY:
==8577==     in use at exit: 0 bytes in 0 blocks
==8577==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==8577==
==8577== All heap blocks were freed -- no leaks are possible
==8577==
==8577== For lists of detected and suppressed errors, rerun with: -s
==8577== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

There exists, however, a new experimental tool **exp-sgcheck**, for a stack and a global array overrun detector, which is still under development (see its official documentation at this [link](https://valgrind.org/docs/manual/sg-manual.html)).



#### Use after free and dangling pointers

This case happens when a pointer is referencing a memory which was already deallocated (i.e. freed). Such a pointer is called a _dangling pointer_. It can be illustrated with the following code snippet saved in the file _free.C_:

```C++
int main(void)
{
  float *arr = new float[2];
  arr[0] = 1.23; // ok  

  delete [] arr; // deallocate memory back
  arr[0] = 1.23; // use after free, this will work only accidentally, i.e.
                 // until the memory relased back in the previous line 
                 // wasn't overwritten by something else
  return 0;
}
```

The above code can be compiled and executed, but **memcheck** will spot and report the problem:

```bash
# No compilation error:
$ g++ -o free free.C

# No execution error (accidentally):
$ ./free 

# However, memcheck spots the problem:
$ valgrind ./free 
==1078954== Memcheck, a memory error detector
==1078954== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1078954== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1078954== Command: ./free
==1078954== 
==1078954== Invalid write of size 4
==1078954==    at 0x1091B2: main (in /home/abilandz/git/lectures/NAT3054/examples/free)
==1078954==  Address 0x4de6c80 is 0 bytes inside a block of size 8 free'd
==1078954==    at 0x484CA8F: operator delete[](void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1078954==    by 0x1091A5: main (in /home/abilandz/git/lectures/NAT3054/examples/free)
==1078954==  Block was alloc'd at
==1078954==    at 0x484A2F3: operator new[](unsigned long) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1078954==    by 0x10917E: main (in /home/abilandz/git/lectures/NAT3054/examples/free)
==1078954== 
==1078954== 
==1078954== HEAP SUMMARY:
==1078954==     in use at exit: 0 bytes in 0 blocks
==1078954==   total heap usage: 2 allocs, 2 frees, 72,712 bytes allocated
==1078954== 
==1078954== All heap blocks were freed -- no leaks are possible
==1078954== 
==1078954== For lists of detected and suppressed errors, rerun with: -s
==1078954== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

```

As a side remark, if an object which is deleted doesn't have a destructor (like built-in types), it's a good programming practice to set it to ```NULL``` explicitly, to force an execution error it if is used after it was deleted:

```C++
delete [] arr; // deallocate memory back    
arr = NULL;    // set pointer to NULL explicitly after 'delete'
```



#### Uninitialized memory access

This case happens when an object was declared but never initialized, and it used later in the code uninitialized. We first illustrate this case with the following correct code snippet saved in the file _initilized.C_:

```C++
#include <stdio.h>
int main(void)
{
  float *arr = new float[2]{1.23, -44.}; // array is declared and initialized 
  printf("\n %f ", arr[0]);  
  printf("\n %f \n\n", arr[1]);  

  delete [] arr; // deallocate memory back    
  arr = NULL;    // set pointer to NULL explicitly after 'delete'

  return 0;
}
```

This code snippet can be compiled and executed without any errors, and **memcheck** doesn't report any error either:

```bash
# No compilation error:
$ g++ -o initilized initilized.C

# No execution error:
$ ./initilized 

 1.230000 
 -44.000000 

# Finally, clearance from 'memcheck':
$ valgrind ./initilized 
==1080261== Memcheck, a memory error detector
==1080261== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1080261== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1080261== Command: ./initilized
==1080261== 

 1.230000 
 -44.000000 

==1080261== 
==1080261== HEAP SUMMARY:
==1080261==     in use at exit: 0 bytes in 0 blocks
==1080261==   total heap usage: 3 allocs, 3 frees, 73,736 bytes allocated
==1080261== 
==1080261== All heap blocks were freed -- no leaks are possible
==1080261== 
==1080261== For lists of detected and suppressed errors, rerun with: -s
==1080261== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

We now re-use the above example, only array is NOT initialized, and save in the file _uninitialized.C_ the following code snippet:

```C++
#include <stdio.h>
int main(void)
{
  float *arr = new float[2]; // array is declared, but NOT initialized 
  printf("\n %f ", arr[0]);  
  printf("\n %f \n\n", arr[1]);  

  delete [] arr; // deallocate memory back    
  arr = NULL;    // set pointer to NULL explicitly after 'delete'

  return 0;
}
```

This code snippet can be compiled without any errors. When executed, it doesn't produce any errors accidentally, because built-in types, like ```float``` in this example, can get initialized to 0.0 by a specific compiler, but in general this is an undefined behavior. But **memcheck** does report an error when declared and uninitialized objects are used:

```bash
# No compilation error:
$ g++ -o uninitilized uninitilized.C

# No execution error:
$ ./uninitilized 

 0.000000 
 0.000000 

# However, 'memcheck' is alert (and surprisingly verbose!):
$ valgrind ./uninitilized 
==1081158== Memcheck, a memory error detector
==1081158== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1081158== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1081158== Command: ./uninitilized
==1081158== 

==1081158== Conditional jump or move depends on uninitialised value(s)
==1081158==    at 0x4AFACB8: __printf_fp_l (printf_fp.c:396)
==1081158==    by 0x4B1692C: __printf_fp_spec (vfprintf-internal.c:354)
==1081158==    by 0x4B1692C: __vfprintf_internal (vfprintf-internal.c:1558)
==1081158==    by 0x4B0079E: printf (printf.c:33)
==1081158==    by 0x1091D0: main (in /home/abilandz/git/lectures/NAT3054/examples/uninitilized)

... many more lines ...

==1081158== Conditional jump or move depends on uninitialised value(s)
==1081158==    at 0x4AFBEFB: __printf_fp_l (printf_fp.c:1230)
==1081158==    by 0x4B1692C: __printf_fp_spec (vfprintf-internal.c:354)
==1081158==    by 0x4B1692C: __vfprintf_internal (vfprintf-internal.c:1558)
==1081158==    by 0x4B0079E: printf (printf.c:33)
==1081158==    by 0x109202: main (in /home/abilandz/git/lectures/NAT3054/examples/uninitilized)
==1081158== 
 0.000000 

==1081158== 
==1081158== HEAP SUMMARY:
==1081158==     in use at exit: 0 bytes in 0 blocks
==1081158==   total heap usage: 3 allocs, 3 frees, 73,736 bytes allocated
==1081158== 
==1081158== All heap blocks were freed -- no leaks are possible
==1081158== 
==1081158== Use --track-origins=yes to see where uninitialised values come from
==1081158== For lists of detected and suppressed errors, rerun with: -s
==1081158== ERROR SUMMARY: 58 errors from 22 contexts (suppressed: 0 from 0)
```



#### Double-free

This case corresponds to the situation when the same memory is deallocated two or more times. It can be illustrated with the following code snippet saved in the file _doubleFree.C_:

```C++
int main(void)
{
  float *arr = new float[2]{1.23, -44.}; // array is declared and initialized 

  // ... do something with this array ...
    
  delete [] arr; // deallocate memory back    
  delete [] arr; // deallocate memory back again    
    
  return 0;
}
```

The code can be compiled without any error, but we will get an error at execution, and when the code is checked with **memcheck**:

```bash
# No compilation error:
$ g++ -o doubleFree doubleFree.C 

# Execution error:
$ ./doubleFree 
free(): double free detected in tcache 2
Aborted (core dumped)

# Diagnosics from 'memcheck':
$ valgrind ./doubleFree 
==1082444== Memcheck, a memory error detector
==1082444== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1082444== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1082444== Command: ./doubleFree
==1082444== 
==1082444== Invalid free() / delete / delete[] / realloc()
==1082444==    at 0x484CA8F: operator delete[](void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1082444==    by 0x1091C7: main (in /home/abilandz/git/lectures/NAT3054/examples/doubleFree)
==1082444==  Address 0x4de6c80 is 0 bytes inside a block of size 8 free'd
==1082444==    at 0x484CA8F: operator delete[](void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1082444==    by 0x1091B4: main (in /home/abilandz/git/lectures/NAT3054/examples/doubleFree)
==1082444==  Block was alloc'd at
==1082444==    at 0x484A2F3: operator new[](unsigned long) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1082444==    by 0x10917E: main (in /home/abilandz/git/lectures/NAT3054/examples/doubleFree)
==1082444== 
==1082444== 
==1082444== HEAP SUMMARY:
==1082444==     in use at exit: 0 bytes in 0 blocks
==1082444==   total heap usage: 2 allocs, 3 frees, 72,712 bytes allocated
==1082444== 
==1082444== All heap blocks were freed -- no leaks are possible
==1082444== 
==1082444== For lists of detected and suppressed errors, rerun with: -s
==1082444== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```





#### Incorrect casting





#### Incorrect pointer arithmetic

### 5. Heap profiling: **Massif** <a name="massif"></a>

TBI 20260117 add a comment on installing visualizer

```bash
$ sudo apt install massif-visualizer
```





### TBI. References <a name="references"></a>

* "_Valgrind Unlocked: Hands‑On Memory Debugging and Performance Profiling for C and C++_", William E. Clark
  * This book was the main reference used in preparing the **valgrind** part of this lecture
* Valgrind website: https://valgrind.org/
* Valgrind repository: https://sourceware.org/git/valgrind.git
* Wikipedia: https://en.wikipedia.org/wiki/Valgrind