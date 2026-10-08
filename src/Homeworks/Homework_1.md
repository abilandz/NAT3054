# Homework 1: Mastery of regular expressions

**Last update:** 20261008-1

**Challenge #1**: Write down a regex that matches all 5-character words that do NOT have the character “c” at the 1st, 2nd or 3rd place. 



**Challenge #2**: Write down a regex that checks if the string content is:

* valid integer (e,g. 123, -4567, +567, but NOT 0123, -000234, +00002454)
* valid integer in the interval 0 to 100 (frequently used when we expect result as percentage)



**Challenge #3:** Write a regex which matches timestamps written in one of the following 3 formats:

```bash
DD-MM-YYYY
DD/MM/YYYY
DD.MM.YYYY
```

Possible valid formats include both ```01-01-2001``` and ```1-1-2001```, but not ```01-1-2001``` or ```1-01-2001``` (zero-padding has to be internally consistent). The  years span the interval ```1000..9999```. For simplicity, assume that all months have the same number of days (30), and ignore subtleties related to the existence of step years, etc. Is solution the same in BRE (test your solution using **grep**) and in ERE (test your solution using **egrep**)? 



**Challenge #4:** Write a regex that matches the format of ORCID ("Open Researcher and Contributor ID"), which is an alphanumeric code used to uniquely identify authors of scientific publications. In particular, ORCID use 16-characters identifiers, consisting of four group of digits 0-9, where each group is separated by a hyphen "-". The allowed range is from 0000-0001-5000-0007 to 0000-0003-5000-0001. Only the final character may be a letter "X" (the final character serves as a checksum, but let's put that aside in this exercise). For instance, example ORCID identifiers are:

```bash
0000-0002-1825-0097
0000-0002-9079-593X
```



**Challenge #5:**  Write down a regex which checks if integer is written in scientific notation. Possible formatting includes:

```bash
8.54585e+09
-8.54585e+09
8.54585E+09
-8.54585E+09
```

Note that ```8.54585e+09``` is a valid integer, but ```8.54585e+02``` is not!



**Challenge #6:** On a local computer, find a file holding the English dictionary (on Ubuntu, such dictionary is in the file "/etc/dictionaries-common/words"). Write down a regex which extracts only the words whose length is exactly 7 characters, do not contain apostrophe ```'``` (i.e. filter out trivial examples like "alien's", "camel's", etc.), and do not contain one or more capital letters (i.e. filter out personal names and abbreviations, etc.). 
