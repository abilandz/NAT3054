# gdb: The GNU Debugger

**Last update**: 20260204-3

<img src="gdb_logo.png" alt="drawing" width="600"/>

### Table of Contents

1. [Introduction](#introduction)
2. [A bit of history](#history)
3. [Example debugging session](#example.debugging.session)
4. [References](#references)





### 1. Introduction <a name="introduction"></a>

The main advantage of **gdb** (The GNU Debugger) over Valgrind is that it enables interactive modifications of program execution at run time, including:

* calling interactively functions against their normal call sequence in the programme, or by supplying interactively different arguments;
* the program can be halted at execution, and the content of variables at that point in the execution can be printed;
* modifying the content of variables interactively at run time;
* stepping through the code by skipping the execution of the problematic part of the code.

Supported programming languages &mdash; **gdb** works with programs written in many programming languages, with full support for (in alphabetical order) Ada, Assembly, C, C++, D, Fortran, Go, Objective-C, OpenCL, Modula-2, Pascal, and Rust.








### 2. A bit of history <a name="history"></a>

The original author of **gdb** is Richard Stallman, and it was first written in 1986 as a part of the GNU collection of free software. It was heavily inspired by the "DBX debugger" developed for "Berkeley Unix" (officially, Berkeley Software Distribution (BSD)") by Mark Linton in the period 1981-1984.

**gdb** was originally written in C, but the latest releases are written in C++17 standard &mdash; its online source code repository can be found at this [link](https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git). As of December 20th, 2025, the latest stable release is version ```17.1```.







### 3. Example debugging session <a name="example.debugging.session"></a>

The basic functionalities of **gdb** are demonstrated with the following simple code snippet written in the ```C``` programming language, and saved in the file "example.c":

```C
#include <stdio.h>
#include <stdlib.h>

void fun_1(void) {
  printf(" ... hello from fun_1 \n");
}

void fun_2(float var) {
  printf(" ... hello from fun_2, var = %f \n\n", var);
}

int main(int argc, char **argv) {

  if(argc <= 1) {
    printf("\n Provide some arguments.\n\n");
    return 1;
  }

  for(int arg = 1; arg < argc; arg++) {
    double var = atof(argv[arg]);
    printf("\n Calling functions for var = %f\n", var);
    fun_1();
    fun_2(var);
  }

  return 0;

}
```

The code is compiled using the **gcc** compiler (or its frontend **g++**, if functionalities from the ```C++``` programming language are used) in the following way:

```bash
$ gcc -g -o example example.c
```

The executable has to be compiled only for debugging purposes with the `-g` option, which instructs the **gcc** compiler to embed debugging symbols inside the executable, which is an essential piece of information for **gdb** during debugging. After debugging is over, the final executable needs to be recompiled without the  ```-g``` option, so the compiler can optimize it in the best possible way.

The above code is very simple, and it does the following:

1. it takes arguments from the command line;
2. for each argument, it calls two functions, **fun_1()** and **fun_2(float var)**;
3. the function **fun_1()** always prints the same message, while the function **fun_2(float var)** prints back the message with the supplied variable.

For instance, at the command line it can be executed by supplying two arguments "10" and "20" as follows:

```bash
$ ./example 10 20

 Calling functions for var = 10.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 10.000000 


 Calling functions for var = 20.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 20.000000 

```

We can now examine the above executable with the **gdb** debugger. Since the executable takes arguments, **gdb** is started with an option ```--args``` as follows:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) 
```

If the executable takes no arguments, the option ```--args``` can be omitted. To suppress the default printout from **gdb**, the flag ```-q``` (or equivalently ```--quiet``` or ```--silent```) can be used. That default printout is plain introductory and copyright messages, which can quickly become annoying:

```bash
$ gdb
GNU gdb (Ubuntu 12.1-0ubuntu1~22.04.2) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word".
(gdb)
```

After executing **gdb** in the terminal, we have started the **gdb** session, as indicated by **gdb**'s prompt ```(gdb)```. To exit **gdb** and get back to the shell, one can execute in **gdb**:

```bash
$ gdb --quiet
(gdb) quit
$ 
```

The most frequently used **gdb** internal commands always have a single- or two-character shortcut version; for the command **quit**, that shortcut version is **q**:

```bash
$ gdb -q
(gdb) q
$ 
```

The synonym command to terminate the **gdb** session is **exit** (but there is no corresponding short version **e**), or a standard keyboard shortcut ```Ctrl+d```.

To get the list of all available internal commands in **gdb**, one can press TAB twice:

```bash
(gdb) TAB+TAB
Display all 196 possibilities? (y or n)
!                                focus                            reverse-search
+                                forward-search                   reverse-step
-                                frame                            reverse-stepi
<                                fs                               rni
>                                ftrace                           rsi
actions                          function                         run
add-auto-load-safe-path          generate-core-file               rwatch
add-auto-load-scripts-directory  goto-bookmark                    save
add-inferior                     guile                            search
add-symbol-file                  guile-repl                       section
add-symbol-file-from-memory      handle                           select-frame
advance                          hbreak                           set
agent-printf                     help                             sharedlibrary
alias                            if                               shell

... many more commands ...
```

Documentation of each command can be requested in **gdb** session with the **help _commandName_**, for instance for the command **next**:

```bash 
(gdb) help next
next, n
Step program, proceeding through subroutine calls.
Usage: next [N]
Unlike "step", if the current source line calls a subroutine,
this command does not enter the subroutine, but instead steps over
the call, in effect treating it as a single source line.

```

The executive summary for all commands can be obtained with:

```bash
(gdb) help all
... many more lines ...

Command class: breakpoints

awatch -- Set an access watchpoint for EXPRESSION.
break, brea, bre, br, b -- Set breakpoint at specified location.
break-range -- Set a breakpoint for an address range.
catch -- Set catchpoints to catch events.

... many more lines ...
```

The **gdb** debugger does not re-implement the standard shell commands and Linux core utilities, because they can be transparently executed in a **gdb** session using the internal command **shell** (or equivalently, its synonym shortcut version **!**). For instance, to execute the Linux **date** command within the **gdb** session, one can proceed as follows:

```bash 
(gdb) shell date
Di 3. Feb 13:18:14 CET 2026
(gdb) !date
Di 3. Feb 13:18:30 CET 2026
```

No space is needed between the shortcut version **!** and command input. When executing shell commands, **gdb** uses the shell specified by the environment variable ```SHELL```. If that variable is empty, **gdb** will use the default shell (which, on most Linux distributions, is the old Bourne shell ```/bin/sh```).  

To run a debugging session using **gdb** for the above executable **example**, we can use the command **run** (or **r** for short) and proceed as follows:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling functions for var = 10.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 10.000000 


 Calling functions for var = 20.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 20.000000 

[Inferior 1 (process 1646995) exited normally]
```

The program runs smoothly until the end, since in this simple example, there are no errors in the code. Nevertheless, we use this example to illustrate several general functionalities of **gdb**. In the source code of "example.c", we focus on the lines:

```
    22	    fun_1();
    23	    fun_2(var);
```

At line 22 in the source code, within the **main()** function, there is a call to the function **fun_1()**, and in the next line a call to the **fun_2(...)** function. If we suspect that the program is having an error in the execution of the function **fun_2(...)**, we can halt the program execution at runtime at the previous line. This can be achieved by using _breakpoints_ with the **gdb** command **break** (or **b** for short):

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) break example.c:22
Breakpoint 1 at 0x125b: file example.c, line 22.
```

If we proceed now with the program execution, it will halt when we reach that breakpoint:

```bash
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling functions for var = 10.000000

Breakpoint 1, main (argc=3, argv=0x7fffffffde98) at example.c:22
22	    fun_1();
```

We can now interactively inspect what each function is doing, irrespectively of the main program execution, by using the command **call** directly for each function:

```bash
(gdb) call fun_1()
 ... hello from fun_1
(gdb) call fun_2(123)
 ... hello from fun_2, var = 123.000000 
(gdb) call fun_2(-4567)
 ... hello from fun_2, var = -4567.000000
```

In addition, we could modify interactively at run time the value of the variable supplied to the function, which is particularly handy when the problem in function execution occurs only for specific values. The **gdb**'s command **call** can be used to invoke both library and user written functions. 

If we forgot the content of the source code in which we have introduced the breakpoint, we can use the **list** (or **l** for short) command, to display enumerated the surrounding 10 lines (by default) from the code:

```bash
# The breakpoint was introduced at line 22, print surrounding 10 lines of code:
(gdb) list 22
17	  }
18	
19	  for(int arg = 1; arg < argc; arg++) {
20	    double var = atof(argv[arg]);
21	    printf("\n Calling functions for var = %f\n", var);
22	    fun_1();
23	    fun_2(var);
24	  }
25	
26	  return 0;
(gdb)
```

Or we can specify the arbitrary range in the printout of the **list** command this way:

```bash
(gdb) l 14,28
14	  if(argc <= 1) {
15	    printf("\n Provide some arguments.\n\n");
16	    return 1;
17	  }
18	
19	  for(int arg = 1; arg < argc; arg++) {
20	    double var = atof(argv[arg]);
21	    printf("\n Calling functions for var = %f\n", var);
22	    fun_1();
23	    fun_2(var);
24	  }
25	
26	  return 0;
27	
28	}
(gdb)
```

After inspecting function calls this way interactively, we can continue the halted program execution until the next breakpoint if it exists, or until the end otherwise, with the **continue** (or **c** for short):

```bash
(gdb) c
Continuing.
 ... hello from fun_1 
 ... hello from fun_2, var = 20.000000 

[Inferior 1 (process 1647610) exited normally]
```

If the program is rerun in **gdb** within the same session, it will be halted at the already set breakpoint(s). To disable temporarily or delete permanently all breakpoints, one can use either the commands **disable** (or **dis** for short), or **delete** (or **d** for short), without any arguments:

```bash
(gdb) disable
Delete all breakpoints? (y or n)
```

To disable differentially specific breakpoints, e.g. the first set breakpoint:

```bash
(gdb) disable 1
```

It is possible to re-enable the disabled breakpoint with the command **enable**:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) break example.c:22
Breakpoint 1 at 0x55555555525b: file example.c, line 22.
(gdb) disable 1
(gdb) enable 1
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling functions for var = 10.000000

Breakpoint 1, main (argc=3, argv=0x7fffffffde98) at example.c:22
22	    fun_1();
```

Alternatively, and in some cases more conveniently, breakpoints can be defined using function names, instead of line code numbers. For instance, we know there is a function named **fun_1()** in the file "example.c", and we can use its name to set the breakpoint in the following way:

```bash 
(gdb) break example.c:fun_1
Breakpoint 1 at 0x1191: file example.c, line 5.
```

Indeed, at line 5 in the source code we have (with default printout of surrounding 10 lines using the **list** command):

```bash
(gdb) list 5
1	#include <stdio.h>
2	#include <stdlib.h>
3	
4	void fun_1(void) {
5	  printf(" ... hello from fun_1 \n");
6	}
7	
8	void fun_2(float var) {
9	  printf(" ... hello from fun_2, var = %f \n\n", var);
10	}
```

In the same spirit, we can set several breakpoints, and continue interactively program execution by stepping from one breakpoint to another. At any point, we can list all set breakpoints with the command **info break** (or **i b** for short):

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...

(gdb) break example.c:22
Breakpoint 1 at 0x125b: file example.c, line 22.

(gdb) break example.c:23
Breakpoint 2 at 0x1260: file example.c, line 23.

(gdb) info break
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x000000000000125b in main at example.c:22
2       breakpoint     keep y   0x0000000000001260 in main at example.c:23

(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling functions for var = 10.000000

Breakpoint 1, main (argc=3, argv=0x7fffffffde98) at example.c:22
22	    fun_1();

(gdb) continue
Continuing.
 ... hello from fun_1 

Breakpoint 2, main (argc=3, argv=0x7fffffffde98) at example.c:23
23	    fun_2(var);
(gdb)
```

We can also inspect variable values at program execution interactively using the **print** (or **p** for short) command. Literally, the program can be halted at execution, and the content of variables at that point in the execution can be printed, as the following example demonstrates:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...

(gdb) break example.c:fun_2
Breakpoint 1 at 0x11b4: file example.c, line 9.

(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling functions for var = 10.000000
 ... hello from fun_1 

Breakpoint 1, fun_2 (var=10) at example.c:9
9	  printf(" ... hello from fun_2, var = %f \n\n", var);

(gdb) print var
$1 = 10
```

Instead of setting manually several breakpoints and continue interactively program execution by stepping from one breakpoint to another, it is also possible to set only the first breakpoint, and then afterward continue to the next source line in the code by using commands **next** (or **n** for short) and **step** (or **s** for short). This is illustrated with the following example, in which the breakpoint is set at the beginning of the **main()** function, and afterward execution if the program is advanced line-by-line by using the **next** command:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...

(gdb) break main
Breakpoint 1 at 0x11f1: file example.c, line 14.

(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, main (argc=3, argv=0x7fffffffde78) at example.c:14
14	  if(argc <= 1) {

(gdb) next
19	  for(int arg = 1; arg < argc; arg++) {

(gdb) next
20	    double var = atof(argv[arg]);

(gdb) next
21	    printf("\n Calling functions for var = %f\n", var);

(gdb) next

 Calling functions for var = 10.000000
22	    fun_1();

(gdb) next
 ... hello from fun_1 
23	    fun_2(var);

(gdb) next
 ... hello from fun_2, var = 10.000000 

19	  for(int arg = 1; arg < argc; arg++) {
```

The code execution doesn't have to be advanced line-by-line &mdash; we can use **next _someInteger_** to advance the code execution by _someInteger_ lines in the source code. When the command **next** is used, function calls that appear within the line of code are executed without stopping. Related command is **step**, which enters a function and performs stopping inside the code of that function:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...

(gdb) break main
Breakpoint 1 at 0x11f1: file example.c, line 14.

(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, main (argc=3, argv=0x7fffffffde78) at example.c:14
14	  if(argc <= 1) {

(gdb) step
19	  for(int arg = 1; arg < argc; arg++) {

(gdb) step
20	    double var = atof(argv[arg]);

(gdb) step
atof (nptr=0x7fffffffe248 "10") at ./stdlib/atof.c:26
26	./stdlib/atof.c: No such file or directory.

(gdb) step
27	in ./stdlib/atof.c

(gdb) step
__GI_strtod (nptr=0x7fffffffe248 "10", endptr=0x0) at ./stdlib/strtod.c:81
81	./stdlib/strtod.c: No such file or directory.
```

As the above example demonstrates, the command **step** also enters the source code of functions from standard libraries. Therefore, in practice one uses **next** and **step** interchangeably during debugging, the latter only when the user-defined function is encountered in the source code. 

This section is concluded by examining with **gdb** the faulty code in which the same memory is deallocated multiple times. The following code snippet written in the ```C++``` programming language is saved in the file named _doubleFree.C_:

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

The source code is compiled as follows, without any errors detected by the compiler:

```bash
$ g++ -g -o doubleFree doubleFree.C 
```

However, at execution, the code crashes:

```bash
$ ./doubleFree 
free(): double free detected in tcache 2
Aborted (core dumped)
```

We now inspect with **gdb** what is causing the above failure:

```bash
$ gdb -q ./doubleFree 
Reading symbols from ./doubleFree...

(gdb) run
Starting program: /home/abilandz/gdb/doubleFree 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
free(): double free detected in tcache 2

Program received signal SIGABRT, Aborted.
__pthread_kill_implementation (no_tid=0, signo=6, threadid=140737352672192) at ./nptl/pthread_kill.c:44
44	./nptl/pthread_kill.c: No such file or directory.
```

This is not very informative either, but we can request within the **gdb** session the backtrace of program execution with the command **backtrace** (or **bt** for short):

```bash
(gdb) backtrace
#0  __pthread_kill_implementation (no_tid=0, signo=6, threadid=140737352672192) at ./nptl/pthread_kill.c:44
#1  __pthread_kill_internal (signo=6, threadid=140737352672192) at ./nptl/pthread_kill.c:78
#2  __GI___pthread_kill (threadid=140737352672192, signo=signo@entry=6) at ./nptl/pthread_kill.c:89
#3  0x00007ffff7842476 in __GI_raise (sig=sig@entry=6) at ../sysdeps/posix/raise.c:26
#4  0x00007ffff78287f3 in __GI_abort () at ./stdlib/abort.c:79
#5  0x00007ffff7889677 in __libc_message (action=action@entry=do_abort, fmt=fmt@entry=0x7ffff79dbb77 "%s\n") at ../sysdeps/posix/libc_fatal.c:156
#6  0x00007ffff78a0cfc in malloc_printerr (str=str@entry=0x7ffff79de6f0 "free(): double free detected in tcache 2") at ./malloc/malloc.c:5664
#7  0x00007ffff78a30ab in _int_free (av=0x7ffff7a1ac80 <main_arena>, p=0x55555556aea0, have_lock=0) at ./malloc/malloc.c:4473
#8  0x00007ffff78a5453 in __GI___libc_free (mem=<optimized out>) at ./malloc/malloc.c:3391
#9  0x00005555555551c8 in main () at doubleFree.C:8
```

From the above printout, the crucial piece of information is in the last line, namely:

```bash 
#9  0x00005555555551c8 in main () at doubleFree.C:8
```

We see that the problem originated in the file _doubleFree.C_, at its 8th line:

```bash
(gdb) ! cat -n doubleFree.C
     1	int main(void)
     2	{
     3	  float *arr = new float[2]{1.23, -44.}; // array is declared and initialized
     4	
     5	  // ... do something with this array ...
     6	
     7	  delete [] arr; // deallocate memory back
     8	  delete [] arr; // deallocate memory back again
     9	
    10	  return 0;
    11	}
```

Indeed, at the 8th line of the source code, the same memory was freed for the 2nd time.






### 4. References <a name="references"></a>

* **gdb** website: [https://www.sourceware.org/gdb/documentation/](https://www.sourceware.org/gdb/documentation/) (manuals in [html](https://sourceware.org/gdb/current/onlinedocs/gdb) and [pdf](https://sourceware.org/gdb/current/onlinedocs/gdb.pdf))
* **gdb** source code repository: [https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git]()
* Wikipedia: [https://en.wikipedia.org/wiki/GNU_Debugger](https://en.wikipedia.org/wiki/GNU_Debugger)
