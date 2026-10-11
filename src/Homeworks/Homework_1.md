# Homework 1: Mastering regular expressions (1/2)

**Last update:** 20261011-1



**Hint #1:** To facilitate solving some of the challenges below, on a local computer, first find the directory holding files that act as local dictionaries. On Ubuntu, such a directory is "/usr/share/dict", and inside one finds the dictionary files:

```bash
$ ls "/usr/share/dict"
american-english  ngerman                 swiss
british-english   ogerman                 words
cracklib-small    README.select-wordlist  words.pre-dictionaries-common
```

For instance, the file "/usr/share/dict/american-english" has more that 100K words sorted alphabetically in one column:

```bash
$ wc -l /usr/share/dict/american-english
104334 /usr/share/dict/american-english
```



**Hint #2:** If writing a single regex is too difficult or cumbersome to accommodate the logical ```AND``` operation, decompose the problem into several steps and use the shell's pipes to combine them, e.g. 

```bash
$ egrep "regex-1" someFile | egrep "regex-2" | egrep "regex-3" ...
```

or use built-in support for logical ```&&``` in some core Linux utilities, e.g. in **awk** using the following syntax:

```bash
$ awk '/regex-1/ && /regex-2/ && /regex-3/ ...' someFile
```

**Remark:** For the latter to work, make sure you use the GNU version of **awk** (i.e. **gawk**), as some other **awk** implementations (e.g. **mawk**) treat some metacharacters in their own non-standard way.



**Challenge #1**: Write down a regex that matches all 5-character words that do NOT have the character “c” at the 1st, 2nd or 3rd place. 



**Challenge #2:** Write down a regex which extracts only the words whose length is exactly 7 characters, do not contain apostrophe ```'``` (i.e. filter out trivial examples like "alien's", "camel's", etc.), and do not contain one or more capital letters (i.e. filter out personal names and abbreviations, etc.). 



**Challenge #3:** Write down a regex which matches all words which have two or more occurrences of character “o”, in any order.



**Challenge #4:** Write down a regex that checks if the string content can be interpreted as:

* valid integer (e.g. ```123```, ```-4568```, ```+569```, but NOT ```0123```, ```-0004568```, ```+0000569```, because integers padded with 0's are evaluated in octal basis);
* valid integer in the interval 0 to 100 (frequently used when we expect the result as a percentage).



**Challenge #5:** Write a regex that matches timestamps written in one of the following 3 formats:

```bash
DD-MM-YYYY
DD/MM/YYYY
DD.MM.YYYY
```

Valid formats include both ```01-01-2001``` and ```1-1-2001```, but not ```01-1-2001``` or ```1-01-2001``` (zero-padding must be internally consistent). The years span the interval ```1000..9999```. For simplicity, assume that all months have the same number of days (30), and ignore subtleties related to the existence of leap years, etc. Is the solution the same in BRE and in ERE (test your solution using **grep** and **egrep**, respectively)?
