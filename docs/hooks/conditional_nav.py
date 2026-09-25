def on_config(config):
    """
    Conditionally change the navigation depending on the theme.
    Remark: Each time I change something here, I have to restart: mkdocs serve (it won't update automatically)
    """
    theme_name = config.theme.name

    if theme_name == "mkdocs": # Navigation for "bootstrap" theme (the default theme, but I have to use "mkdocs", not "bootstrap" as the name here)
        config.nav = [
            {"Introduction": "index.md"}, # this file "index.md" must be in docs/
            {"Lectures": [  
                {"Lecture 1: Regular Expressions": "regex.md"},
                {"Lecture 2: Git": "git.md"},
                {"Lecture 3: make & cmake": "make.md"},
                {"Lecture 4: Working remotely": "remote.md"},
                {"Lecture 5: Valgrind": "valgrind.md"},
                {"Lecture 6: gdb: The GNU Debugger": "gdb.md"},
            ]},
            {"Homeworks": [  
                {"Scoresheet": "Homeworks/Scoresheet.md"},
                {"Homework 1: TBI" : "Homeworks/Homework_1.md"},
            ]},
        ]

    elif theme_name == "material": # Navigation for "Material" theme
        config.nav = [
            {"Introduction": "index.md"}, # this file "index.md" must be in docs/
            {"Lectures": [  
                {"1. Regular Expressions": "regex.md"},
                {"2. Git": "git.md"},
                {"3. make & cmake": "make.md"},
                {"4. Working remotely": "remote.md"},
                {"5. Valgrind": "valgrind.md"},
                {"6. gdb: The GNU Debugger": "gdb.md"},
            ]},
            {"Homeworks": [  
                {"Scoresheet": "Homeworks/Scoresheet.md"},
                {"Homework 1: TBI" : "Homeworks/Homework_1.md"},
            ]},
        ]

    elif theme_name == "readthedocs": # Different structure for "ReadTheDocs" theme
        config.nav = [
            {"Introduction": "index.md"}, # this file "index.md" must be in docs/
            {"Lectures": [  
                {"Lecture 1: Regular Expressions": "regex.md"},
                {"Lecture 2: Git": "git.md"},
                {"Lecture 3: make & cmake": "make.md"},
                {"Lecture 4: Working remotely": "remote.md"},
                {"Lecture 5: Valgrind": "valgrind.md"},
                {"Lecture 6: gdb: The GNU Debugger": "gdb.md"},
            ]},
            {"Homeworks": [  
                {"Scoresheet": "Homeworks/Scoresheet.md"},
                {"Homework 1: TBI" : "Homeworks/Homework_1.md"},
            ]},
        ]

    else: # Optional: fallback for unknown themes
        config.nav = [
            {"Home": "index.md"},
        ]

    return config
