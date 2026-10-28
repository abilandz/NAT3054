# Homework 2: Mastering regular expressions (2/2)

**Last update:** 20261028-1



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



**Challenge #1:** Write down a regex which matches all words containing all 5 vowels "a", "e", "i", "o", "u", where each vowel must occur at least once, and multiple occurrences are:

* allowed;
* not allowed.



**Challenge #2**: Cracking the web-based word game [Wordle](https://www.nytimes.com/games/wordle/index.html). Write a regex that helps resolve the following unrelated cases encountered in the word game [Wordle](https://www.nytimes.com/games/wordle/index.html):  

+ find all 5-character words which begin with “w”, end with “h”, and somewhere in places 2, 3 or 4 there is exactly one occurrence of “t”;
+ find all 5-character words which begin with “ma”, do not contain vowels "e", "i", "u", and somewhere in positions 3, 4 and 5 there is one occurrence of "o" and one occurrence of "r".



**Challenge #3:** Write a regex that matches the format of ORCID ("Open Researcher and Contributor ID"), which is an alphanumeric code used to uniquely identify authors of scientific publications. In particular, ORCID use 16-characters identifiers, consisting of four group of digits 0-9, where each group is separated by a hyphen "-". The allowed range is from 0000-0001-5000-0007 to 0000-0003-5000-0001 (the boundaries should NOT be interpreted field-by-field). Only the final character may be a letter "X" (the final character serves as a checksum, but let's put that aside in this exercise). For instance, example ORCID identifiers are:

```bash
0000-0002-1825-0097
0000-0002-9079-593X
```

You can create for free your ORCID ID at this [link](https://orcid.org/). 



**Challenge #4:** Write down a regex which checks if a string can be interpreted as a float. Possible valid formats include:

```bash
8.54585
+8.54585
-8.54585
0.54585
.54585
+.54585
-.54585
8.54585e-2
8.54585e+2
8.54585e2
```

Both the number and the exponent part can be padded with any number of 0's, e.g. ```08.54585```, ```008.54585```, ```8.54585e+02```, ```8.54585e+002```, ```008.54585e-002```, etc.



