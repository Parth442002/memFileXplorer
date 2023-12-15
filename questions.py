questions = [
    {
        "type": "confirm",
        "message": "Do you want to load an existing terminal session?",
        "name": "load_session",
        "default": False,
    },
    {
        "type": "input",
        "message": "Enter the path of the existing session.json:",
        "name": "session_path",
        "when": lambda answers: answers["load_session"],
    },
]

exitQuestions = [
    {
        "type": "confirm",
        "message": "Do you want to save this terminal session?",
        "name": "save_session",
        "default": False,
    },
    {
        "type": "input",
        "message": "Enter the path to save this session.json:",
        "name": "session_path",
        "when": lambda answers: answers["save_session"],
    },
]
