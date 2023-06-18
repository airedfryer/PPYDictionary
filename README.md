# Dictionary Application
This is a simple dictionary application implemented using the tkinter library in Python, made as a project for PPY. It allows users to add, load, and delete word definitions from a CSV file. The application provides an interactive GUI interface, which allows the user to display and manage dictionary entries.

## Functionality
+ Previewing words and all their definitions: Like most online dictionaries, this dictionary allows the user to see the different attributes associated with a word: what part-of-speech it is, its definition, and synonyms and antonyms if there are any. The user should select a word from the dropdown and click the "Load Into Listbox" button. This will allow the user to see different definitons of the word at once.
+ Adding new words: To add a new word, the user should enter the word, select its part of speech, provide a definition, and optionally add synonyms and antonyms. Clicking the green "Add Word" button adds the word and its information to the CSV file.
+ Loading existing records: To load in an existing record, the user should select the word from the dropdown and load in the realted information. The user then should input the number related to the record and click the "Load record" button. This allows the user to create a new definition for the word, as well as delete an existing one (discussed below).
+ Deleting existing words and definitions: To delete a definition, the user should select the word from the dropdown and load in the realted information. The user then should input the number related to the record and click the "Load record" button. This will load in the necessary information into the textboxes. The user should then click the red "Delete Definition" button. The selected definition is then removed from the CSV file. If this is the only definition associated with the word, the word will be deleted altogether.
+ Editing existing records: To edit a definition, the user should load in an existing record. Then, the user should change relevant data in the entry fields and confirm changes using the "Edit Entry" button. The old record will be updated with the new data.
+ Checking pronunciations of words: For this, both a masculine and feminine voice are available (masculine is selectad by default). These can be chosen with the radio buttons on the right hand side of the application. To check the prononciation of a word, the user should select the word from the dropdown. There is no need to load the word into the listbox. Then, the user should press the blue "Pronounce Word" button.

## Data Storage
The dictionary application uses a semicolon-delineated CSV file (dictionary.csv) to store word data. The CSV file has the following structure:

| Word | Part-of-Speech | Definition | Synonyms | Antonyms |
|-----|-----|-----|-----|-----:|
|word1|p-o-s1|definition1|synonyms1|antonyms1|
|word2|p-o-s2|definition2|synonyms2|antonyms2|
|...|...|...|...|...|

Each row represents a word, with columns for the word, part-of-speech, definition, synonyms, and antonyms.

## Dependencies
The dictionary application requires the following dependencies:
+ Python 3.x
+ Tkinter: Standard GUI library for Python.
+ csv module: Allows for file handling.
+ pyttsx3: Allows for text-to-speech. Does not require Internet connection.

Make sure you have these dependencies installed before running the application.
