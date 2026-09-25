def on_config(config):
    print("\n\n========== HOOK IS RUNNINGG ==========")
    print(f"Theme name: {config.theme.name}")
    print("=====================================\n\n")

    theme = config.theme.name

    if theme == "mkdocs": # Navigation for "Material" theme (default)  "bootstrap"
        print(f"Theme name: {config.theme.name}")
        config.nav = [
            {"Home44": "index.md"}, # this file "index.md" must be in docs/
            {"Home33": "index-33.md"}, # this file "index.md" must be in docs/
        ]
    return config
