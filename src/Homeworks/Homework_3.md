# Homework 3: Git (1/2)

**Last update:** 20261121-1

**Automatically building and hosting a static website on GitHub**

In this challenge, a step-by-step procedure is outlined that can be used to automatically build and host a static website on [GitHub](https://github.com), using one of the freely available static-site generators. Such static generators are particularly suitable to build a website hosting documentation, when dynamical interaction with the user is not needed. As a concrete example in this challenge, a very popular [MkDocs](https://www.mkdocs.org/) static-site generator is used to automatically generate the documentation website for the project written in the Markdown source code. The three predefined [MkDocs](https://www.mkdocs.org/) themes are tested, namely: "mkdocs", "material" (the recommended one), and "readthedocs".

1. Make a new public repository (it has to be public in this example!) on [GitHub](https://github.com), e.g. named "myWebsite" with a default "README.md" file (in this challenge, there will be no need for a predefined ".gitignore" template, or a specific license), and clone it locally, e.g.:

    ```bash
    $ git clone https://github.com/abilandz/myWebsite myWebsite 
    ```

    Do not forget above to replace "abilandz" with your account on [GitHub](https://github.com).

2. Install [MkDocs](https://www.mkdocs.org/) locally, and its very popular custom theme "material", using the following command:

    ```bash
    $ pip install mkdocs mkdocs-material
    ```

	In a rare case that **pip** is not already installed locally, it can for instance be installed on Linux Ubuntu using the **apt** package manager:

    ```bash
    $ sudo apt update
    $ sudo apt install python3-pip
    ```

	Similarly, on other Linux distributions it can be installed using their default package managers instead of Ubuntu's **apt** (for instance **pacman** on Arch Linux, etc.).

3. Initially, organize the local directory "myWebsite" and populate it with files as follows:

	```bash
    myWebsite/
    ├── README.md
    ├── .gitignore
    ├── mkdocs.yml
    └── docs/
        ├── index.md
        ├── figures/
        │   ├── favicon.png
        │	└── logo.png
        └── src/
            ├── welcome.md
            ├── section_1.md
            └── section_2.md
	```
	
4. The content of the file "README.md" is written using the Markdown syntax, and this content will be automatically displayed on the repository's main page on [GitHub](https://github.com). You can add for instance the following trivial content:

       ```markdown
       # My website
    
       On this website, I ...
       ```

	and then see later how the repository's page on [GitHub](https://github.com) looks like, when you make the commit locally with these changes, and push it to the online repository. 

5. In the file ".gitignore" add the following content initially:

       ```bash
       site/
       ```

	This is needed, so that all the generated site files, which are automatically created in this directory by [MkDocs](https://www.mkdocs.org/) and are getting updated at each build, are not unnecessarily added to the version control by Git. 

6. The file "mkdocs.yml" is the most important configuration file, and its syntax and internal structure are specific to the [MkDocs](https://www.mkdocs.org/) static-site generator. Other static-site generators use different syntax or even different language in the configuration files, but the overall idea is the same. The initial content of "mkdocs.yml" needs to resemble the above directory structure and could look as follows:

       ```yaml
       site_name: "This is my website"
       
       theme:
         name: material
         favicon: figures/favicon.png
         logo: figures/logo.png
            
       nav:
         - "Home": "index.md"
         - "Welcome": "src/welcome.md"
         - "Sections":
             - "Section 1": "src/section_1.md"
             - "Section 2": "src/section_2.md"     
       ```
	According to the internal YAML syntax, indentation is not fixed to some specific value, but once the starting indentation is set, it has to remain consistent throughout the document.
	
7. By default the custom theme ```material``` is used (it needs to be installed separately, see above), but one can always experiment with two built-in themes, for instance ```mkdocs``` and ```readthedocs``` (no separate installation is needed, they come with [MkDocs](https://www.mkdocs.org/) installation).

8. The website logo and favicon icon (the small icon in the tab when the website is open in a browser) can be specified separately with the corresponding fields in the "mkdocs.yml" configuration file. If this is not needed, these two fields can be commented out using the ```#``` symbol (similar to shell syntax):
    ```yaml
    # favicon: figures/favicon.png
    # logo: figures/logo.png
    ```

9. Next, one defines the files that hold the concrete website content, and how to navigate (the ```nav``` field in the above configuration file) from one file to another while browsing the site content online. For instance, one can start with the following trivial content of those files:

    ```Markdown title="File: docs/index.md"
    --8<-- "Homeworks/Homework_3/index.md"
    ```

	```Markdown title="File: docs/src/welcome.md"
    --8<-- "Homeworks/Homework_3/welcome.md"
    ```

	```Markdown title="File: docs/src/section_1.md"
    --8<-- "Homeworks/Homework_3/section_1.md"
    ```

	```Markdown title="File: docs/src/section_2.md"
    --8<-- "Homeworks/Homework_3/section_2.md"
    ```

10. Finally, one can build and preview the static site locally, by executing in the directory where the main configuration file "mkdocs.yml" is placed:
	```bash
	$ mkdocs serve
	... some additional info ...
	INFO    -  [12:21:02] Serving on http://127.0.0.1:8000/
	```
	It suffices now to open address "http://127.0.0.1:8000/" in a local browser, and the website will be displayed. If one runs the above command in a separate terminal, and keeps a local browser open with the address "http://127.0.0.1:8000/", then any change in the website source code will be automatically refreshed in the browser. 
    
11. When satisfied with the current status, one stages, commits and pushes to the online [GitHub](https://github.com) repository all changes in the standard way:
	```bash
	$ git add .
	$ git commit -m "first update"
	$ git push
	```
	After this step, all changes on the local "main" branch are merely propagated to the corresponding remote branch in the online [GitHub](https://github.com) repository. But to host the [MkDocs](https://www.mkdocs.org/)-based project on [GitHub](https://github.com), one has to go through a few more steps.
	
12. Deploy in addition the [MkDocs](https://www.mkdocs.org/)-based project via a separate branch in this repository. This step is completely automated, and one needs to execute only:
    ```bash
    $ mkdocs gh-deploy
    ... some additional info ...
    INFO    -  Your documentation should shortly be available at: https://abilandz.github.io/myWebsite/
    ```
    The above command **mkdocs gh-deploy** created a new branch automatically in a local Git repository, named "gh-pages", and even deployed that branch automatically to the online [GitHub](https://github.com) repository. One can select now on [GitHub](https://github.com) whether the project will be built and hosted from the "main" branch (using the default "GitHub Pages" theme and layout) or from "gh-pages" branch (using the specified [MkDocs](https://www.mkdocs.org/) theme in the configuration file "mkdocs.yml", which was "material" in the above example). In both cases, the project will be hosted at automatically generated URL (e.g. [https://abilandz.github.io/myWebsite/](https://abilandz.github.io/myWebsite/), replace "abilandz" your username).
    
13. Finally, one needs to configure on [GitHub](https://github.com) from which branch the project's static website will be built (this configuration needs to be performed only once):
	+ Go to the project repository on [GitHub](https://github.com), and navigate to "Settings";
	+ In the left menu, choose "Pages";
	+ Ensure that under "Build and deployment" the Git branch is set to "gh-pages" (if you want to use [MkDocs](https://www.mkdocs.org/) layout), or "main" (if you want to use the default "GitHub Pages" layout).

14. After the above initial setup, the normal development workflow is:
	+ Develop the site locally and preview all changes in a local browser with:
		```bash
        $ mkdocs serve
        ```
	+ Stage, commit, push and deploy all changes:
		```bash
        $ git add .
        $ git commit -m "some commit message"
        $ git push
        $ mkdocs gh-deploy
		```
		After this step, the website content will be automatically updated on [GitHub](https://github.com). 
		

**Challenge:** Send me the link to your example website for documentation hosted on [GitHub](https://github.com), which is built by using the "material" theme of [MkDocs](https://www.mkdocs.org/) (or one of the built-in themes "mkdocs" or "readthedocs").


**Remark #1**: The static-site generator [MkDocs](https://www.mkdocs.org/) offers a lot of additional built-in features, however they have to be enabled explicitly in the configuration file "mkdocs.yml" if necessary. For instance, if one wants to automatically generate the PDF version of the website and make it available for downloading, the PDF plugin (such as ```to-pdf``` or ```with-pdf```) can be used. In that case, the following lines need to be added to "mkdocs.yml":

```YAML
# download a site in PDF:
plugins:
  - to-pdf:
      output_path: docs/pdf/NAT3054.pdf
      cover: false
      cover_title: "some title"
```
In a similar fashion, one needs to enable explicitly the support for mathematical expressions, [Mermaid](https://mermaid.ai/) diagrams, etc.

**Remark #2**: There are plethora of other static-site generators besides [MkDocs](https://www.mkdocs.org/) and the default "GitHub Pages" offered by [GitHub](https://github.com), each of which comes with different features, configuration files, syntax and deployement procedure. You can find a good overview at [https://jamstack.org/generators/](https://jamstack.org/generators/).