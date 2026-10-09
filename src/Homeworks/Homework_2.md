# Homework 2: Mastering regular expressions (2/2)

**Last update:** 20261009-1

To facilitate solving some of the challenges below, on a local computer, first find the directory holding files that act as local dictionaries. On Ubuntu, such a directory is "/usr/share/dict", and inside one finds the dictionary files:

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



**Challenge #1:** Write down a regex which matches all words containing all 5 vowels "a", "e", "i", "o", "u" (each vowel must occur at least once, multiple occurrences are allowed).



**Challenge #2**: Cracking the web-based word game [Wordle](https://www.nytimes.com/games/wordle/index.html). Write a regex that helps resolve the following unrelated cases encountered in the word game [Wordle](https://www.nytimes.com/games/wordle/index.html):  

+ find all 5-character words which begin with “w”, end with “h”, and somewhere in places 2, 3 or 4 there is exactly one occurrence of “t”;
+ find all 5-character words which begin with “ma”, do not contain vowels "e", "i", "u", and somewhere in positions 3, 4 and 5 there is one occurrence of "o" and one occurrence of "r".

**Hint:** If writing a single regex is too difficult or cumbersome, decompose the problem in several steps and use shell's pipes to combine them, e.g. 

```bash
$ egrep "regex-1" dictionary-file | egrep "regex-2" | egrep "regex-3" ...
```





**Challenge #3:** Write a regex that matches the format of ORCID ("Open Researcher and Contributor ID"), which is an alphanumeric code used to uniquely identify authors of scientific publications. In particular, ORCID use 16-characters identifiers, consisting of four group of digits 0-9, where each group is separated by a hyphen "-". The allowed range is from 0000-0001-5000-0007 to 0000-0003-5000-0001. Only the final character may be a letter "X" (the final character serves as a checksum, but let's put that aside in this exercise). For instance, example ORCID identifiers are:

```bash
0000-0002-1825-0097
0000-0002-9079-593X
```

You can create for free your ORCID ID at this [link](https://orcid.org/). 



**Challenge #4:** Write down a regex which checks if a string can be interpreted as a float.



**Challenge #5:** Write down a regex which checks if integer is written in scientific notation. Possible formatting includes:

```bash
8.54585e+09
+8.54585e+09
-8.54585e+09
8.54585E+09
+8.54585E+09
-8.54585E+09
```

Note that ```8.54585e+09``` is a valid integer, but ```8.54585e+02``` is not! This challenge is more tricky than it appears at first sight. 



