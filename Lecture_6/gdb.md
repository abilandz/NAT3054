# gdb: The GNU Debugger

**Last update**: 20260203-1

<img src="gdb_logo.png" alt="drawing" width="600"/>

### Table of Contents

1. [Introduction](#introduction)
2. [A bit of history](#history)
3. [Example debugging session](#example.debugging.session)
4. [References](#references)





### 1. Introduction <a name="introduction"></a>

The main advantage of **gdb** (The GNU Debugger) over Valgrind is that it enables interactive modifications of program execution at run time:	

* calling interactively functions against their normal call sequence in the programme;
* program can be halted at execution, and content of variables at that point in the execution can be printed;
* modifying interactively content of variables at run time;
* stepping through the code.

Supported programming languages &mdash; **gdb** works with programs written in many programming language, with a full support for (in alpabetical order) Ada, Assembly, C, C++, D, Fortran, Go, Objective-C, OpenCL, Modula-2, Pascal, and Rust.






### 2. A bit of history <a name="history"></a>

The original author of **gdb** is Richard Stallman, and it was first written in 1986 as a part of GNU collection of free software. It was heavily inspired by the "DBX debugger" developed for "Berkeley Unix" (officially, Berkeley Software Distribution (BSD)") by Mark Linton in the period 1981-1984.

**gdb** was originally written in C, but latest releases are written in C++17 standard &mdash; its online source code repository can be found at this [link](https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git). As of December 20th, 2025, the latest stable release is version ```17.1```.





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
    printf("\n Calling all functions for var = %f\n", var);
    fun_1();
    fun_2(var);
  }

  return 0;

}
```

The code is compiled using the **gcc** compiler (or **g++**, if functionalities from the ```C++``` programming language are used) in the following way:

```bash
$ gcc -g -o example example.c
```

The executable has to be compiled only for debugging purposes with the `-g` option, which instructs the **gcc** compiler to embed debugging symbols inside the executable, which is essential piece of information for the **gdb** during debugging. After debugging is over, the final executable needs to be recompiled without the  ```-g``` option, so that compiler can optimize the final executable in the best possible way.

The above code is very simple and it does the following:

1. it takes arguments from the command line;
2. for each argument, it calls two functions, **fun_1()** and **fun_2(float var)**;
3. the function **fun_1()** prints always the same message, while the function **fun_2(float var)** prints back the message with the supplied variable.

For instance, at command line it can be executed by supplying two arguments "10" and "20" as follows:

```bash
$ ./example 10 20

 Calling all functions for var = 10.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 10.000000 


 Calling all functions for var = 20.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 20.000000 

```

We can now examine the above executable with the **gdb** debugger. Since the executable takes arguments, the **gdb** is started as follows:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) 
```

If the executable doesn't take any arguments, the option ```--args``` can be omitted. To suppress the default printout of **gdb**, the flag ```-q``` (or equivalently ```--quiet``` or ```--silent```) can be used. That default printout are plain introductory and copyright messages, which can quickly become annoying:

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
```

After executing **gdb** in the terminal, we have started the **gdb** session, as it is indicated by the **gdb**'s prompt ```(gdb)```. To exit **gdb** and get back to the shell, we can execute in **gdb**:

```bash
$ gdb
(gdb) quit
$ 
```

The most frequently used **gdb** internal commands have always the single- or two-character shortcut version; **quit** that shortcut version is **q**:

```bash
$ gdb
(gdb) q
$ 
```

The synonym command to terminate the **gdb** session is **exit** (but there is no corresponding short version **e**), or a standard keyboard shortcut ```Ctrl+d```.

To get the list of all available internal commands in **gdb**, one can press two times TAB:

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

Documentation of each command can be requested with **help _commandName_**, for instance for the command **next**:

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

The **gdb** debugger does not re-implement the standard shell commands and Linux core utilities, because they can be transparently executed in a **gdb** session by using the command **shell** (or equivalently, its synonym shortcut version **!**). For instance, to execute the Linux **date** command within the **gdb** session, one can proceed as follows:

```bash 
(gdb) shell date
Di 3. Feb 13:18:14 CET 2026
(gdb) !date
Di 3. Feb 13:18:30 CET 2026
```

No space is needed between shortcut version **!** and command input. When executing shell commands, the **gdb** uses the shell which is specified in the environment variable ```SHELL```. If that variable is empty, **gdb** will use the default shell (which on most Linux distributions will be the old Bourne shell ```/bin/sh```).  

To run in the **gdb** debugging session the above example executable, we proceed as follows:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling all functions for var = 10.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 10.000000 


 Calling all functions for var = 20.000000
 ... hello from fun_1 
 ... hello from fun_2, var = 20.000000 

[Inferior 1 (process 1646995) exited normally]
```

The program runs smoothly until the end, since in this simple example there are no errors in the code. Nevertheless, we can still use it to illustrate several general aspects of **gdb**. In the source code of "example.c", we focus on the lines:

```
    22	    fun_1();
    23	    fun_2(var);
```

At line 22 in the **main()** function there is a call to the function **fun_1()**, and in the next line the call to **fun_2()** function. If we suspect that program is having an error in the execution of the function **fun_2()**, we can halt the program execution at runtime at the previous line. This can be achieved by using _breakpoints_ with the **gdb** command **break** (or **b** for short):

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) break example.c:22
Breakpoint 1 at 0x125b: file example.c, line 22.
```

If we proceed now with program execution, it will halt when we reach that breakpoint:

```bash
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling all functions for var = 10.000000

Breakpoint 1, main (argc=3, argv=0x7fffffffde98) at example.c:22
22	    fun_1();
```

We can now interactively inspect what each function is doing irrespectively of the main program execution, by using the command **call** directly for each function:

```bash
(gdb) call fun_1()
 ... hello from fun_1
(gdb) call fun_2(123)
 ... hello from fun_2, var = 123.000000 
(gdb) call fun_2(-456)
 ... hello from fun_2, var = -456.000000
```

The command **call** invokes both library and user written functions. 

If we forgot the content of the source code in which we have introduced the breakpoint, we can use **list** (or **l** for short) command, to display surrounding 10 lines (by default) from the code:

```bash
# The breakpoint was introduced at line 22, print surrounding 10 lines of code:
(gdb) list 22
17	  }
18	
19	  for(int arg = 1; arg < argc; arg++) {
20	    double var = atof(argv[arg]);
21	    printf("\n Calling all functions for var = %f\n", var);
22	    fun_1();
23	    fun_2(var);
24	  }
25	
26	  return 0;
```

Or specify the arbitrary range this way:

```bash
(gdb) l 13,28
13	
14	  if(argc <= 1) {
15	    printf("\n Provide some arguments.\n\n");
16	    return 1;
17	  }
18	
19	  for(int arg = 1; arg < argc; arg++) {
20	    double var = atof(argv[arg]);
21	    printf("\n Calling all functions for var = %f\n", var);
22	    fun_1();
23	    fun_2(var);
24	  }
25	
26	  return 0;
27	
28	}

```

After inspecting function calls this way interactively, we can continue the halted program execution with the **continue** (or **c** for short):

```bash
(gdb) c
Continuing.
 ... hello from fun_1 
 ... hello from fun_2, var = 20.000000 

[Inferior 1 (process 1647610) exited normally]
```

If the program is rerun within **gdb** in the same session, it will be halted at the already set breakpoint(s). To remove all breakpoints, one can use the command **disable** without arguments:

```bash
(gdb) disable
```

To remove differentially specific breakpoints, e.g. the first set breakpoint:

```bash
(gdb) disable 1
```

It is even possible to re-enable the accidentally disabled breakpoint with the command **enable**:

```bash
(gdb) break example.c:22
Breakpoint 1 at 0x55555555525b: file example.c, line 22.
(gdb) disable 1
(gdb) enable 1
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling all functions for var = 10.000000

Breakpoint 1, main (argc=3, argv=0x7fffffffde98) at example.c:22
22	    fun_1();
```

Alternatively, and in some cases more conveniently, breakpoints can be defined using the function names, instead the line code numbers. For instance, we know there is a function named **fun_1()** in the file "example.c", and we can use its name to set the breakpoint in the following way:

```bash 
(gdb) break example.c:fun_1
Breakpoint 1 at 0x1191: file example.c, line 5.
```

Indeed, at line 5 in the source code we have (with default printout of surrounding 10 lines in both directions using the **list** command) :

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

In the same spirit, we can set several breakpoints, and continue interactively program execution from one breakpoint to another:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) break example.c:22
Breakpoint 1 at 0x125b: file example.c, line 22.
(gdb) break example.c:23
Breakpoint 2 at 0x1260: file example.c, line 23.
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling all functions for var = 10.000000

Breakpoint 1, main (argc=3, argv=0x7fffffffde98) at example.c:22
22	    fun_1();
(gdb) continue
Continuing.
 ... hello from fun_1 

Breakpoint 2, main (argc=3, argv=0x7fffffffde98) at example.c:23
23	    fun_2(var);
(gdb)
```

Interactively, we can also inspect the value of variables at program execution using the command **print** (or **p** for short). Literally, the program can be halted at execution, and content of variables at that point in the execution can be printed, as the following example demonstrates:

```bash
$ gdb -q --args ./example 10 20
Reading symbols from ./example...
(gdb) break example.c:fun_2
Breakpoint 1 at 0x11b4: file example.c, line 9.
(gdb) run
Starting program: /home/abilandz/gdb/example 10 20
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 Calling all functions for var = 10.000000
 ... hello from fun_1 

Breakpoint 1, fun_2 (var=10) at example.c:9
9	  printf(" ... hello from fun_2, var = %f \n\n", var);
(gdb) print var
$1 = 10
```





TBC 20260203



* **attaching**

And alternative way to start **gdb** is to attach to an already running process ... 



* **gdb scripts**
  * `gdb` executes local file `.gdbinit` after running.  + check this SO https://stackoverflow.com/questions/10748501/what-are-the-best-ways-to-automate-a-gdb-debugging-session
    * Command definitions placed in the local file **.gdbinit** are automatically loaded at the beginning of the gdb session. Command definitions can also be saved in ordinary files and loaded using the **source** command.
  * `gdb` executes file `.gdbinit` after running.



* commands:
  * **backtrace** (or **bt** for short) &mdash; request backtrace if program crashed
  * We can use the  command (which can also be spelled bt), to see where we are in the stack as a whole: the
    backtrace command displays a stack frame for each active subroutine.

* **next _n_**
  * command n (next) to advance execution to the next line of the current
    function.
* **step** (or **s** for short)  -- does it take argument
  * step goes to the next line to be executed in any subroutine
* **skip _n_**
* **jump _location_**








### 4. References <a name="references"></a>

* **gdb** website: [https://www.sourceware.org/gdb/documentation/](https://www.sourceware.org/gdb/documentation/) (manuals in [html](https://sourceware.org/gdb/current/onlinedocs/gdb) and [pdf](https://sourceware.org/gdb/current/onlinedocs/gdb.pdf))
* **gdb** source code repository: [https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git]()
* Wikipedia: [https://en.wikipedia.org/wiki/GNU_Debugger](https://en.wikipedia.org/wiki/GNU_Debugger)
