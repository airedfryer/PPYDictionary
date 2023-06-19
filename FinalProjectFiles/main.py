import tkinter as tk
from tkinter import messagebox
from tkinter import Scrollbar
import csv
import pyttsx3

engine = pyttsx3.init()


def select_voice():
    """
    Selects the voice for pronunciation based on the chosen option.

    Retrieves the selected voice option from the `voice_option` variable and sets the corresponding
    voice in the text-to-speech engine (`engine`). If "M" is selected, the first/masculine voice in the available
    voices list is used. If "F" is selected, the second/feminine voice is used.
    """
    voice = voice_option.get()
    if voice == "M":
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
    elif voice == "F":
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)


def pronounce_word():
    """
    Pronounces the selected word using the pyttsx3 TTS engine.

    Retrieves the selected word from the `word_dropdown` variable and checks if it is a valid word.
    If the word is valid, it is passed to the text-to-speech engine (`engine`) for pronunciation.
    """
    selected_word = word_dropdown.get().strip()
    if not selected_word or selected_word == "Select a word":
        messagebox.showerror("Invalid Word", "Please select a valid word.")
        return

    engine.say(selected_word)
    engine.runAndWait()


def add_word():
    """
    Adds a new word entry to the dictionary.

    This function retrieves the values entered in the word, part-of-speech, definition, synonyms, and antonyms
    fields. It performs validation to ensure that all required fields (word, p-o-s, definition) are filled.
    If the word entry is unique (not already existing in the dictionary), it appends the word and its details
    to the CSV file. Finally, it displays a success message, refreshes the word dropdown and listbox,
    and clears the input fields.
    """
    word = word_entry.get().strip()
    pos = pos_dropdown.get()
    definition = definition_entry.get().strip()
    synonyms = synonyms_entry.get().strip()
    antonyms = antonyms_entry.get().strip()

    if word and definition and pos != "Select a part-of-speech":
        with open('dictionary.csv', 'r') as f:
            rdr = csv.reader(f, delimiter=';')
            for row in rdr:
                if row[0].strip() == word and row[1].strip() == pos and row[2].strip() == definition:
                    messagebox.showwarning("Duplicate Entry", "The entry already exists.")
                    return

        with open('dictionary.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([word, pos, definition, synonyms, antonyms])

        messagebox.showinfo("Success", "Word added successfully.")
        refresh_dropdown()
        refresh_listbox()
        clear_fields()
    else:
        messagebox.showwarning("Missing Information", "Please enter a word, part-of-speech, and definition.")


def load_word():
    """
    Loads the details of a word from the dictionary file.

    Retrieves a word form the dropdown and searches for its details in the dictionary file. If the word is found,
    it retrieves the associated part-of-speech, definition, synonyms, and antonyms. The function then populates
    the listbox with the retrieved information.
    """
    selected_word = word_dropdown.get()
    listbox.delete(0, tk.END)
    count = 1

    with open('dictionary.csv', 'r') as f:
        rdr = csv.reader(f, delimiter=';')
        for row in rdr:
            if row[0] == selected_word:
                listbox.insert(tk.END, f"{count})")
                listbox.insert(tk.END, "Part-of-speech: " + row[1])
                listbox.insert(tk.END, "Definition: " + row[2])
                listbox.insert(tk.END, "Synonyms: " + row[3])
                listbox.insert(tk.END, "Antonyms: " + row[4])
                count += 1


def delete_record():
    """
    Deletes a word record from the dictionary file.

    Retrieves word, part-of-speech and definition from the entry box and deletes the corresponding word record
    from the dictionary file. The function removes the record from the file, refreshes the UI listbox, and displays
    a success message. It requires the user to load in the word instead of using the index as a security measure.
    """
    selected_word = word_entry.get().strip()
    selected_pos = pos_dropdown.get().strip()
    selected_definition = definition_entry.get().strip()

    if not selected_word or not selected_pos or not selected_definition:
        messagebox.showwarning("Incomplete Information", "Please provide the word, part of speech, and definition.")
        return

    with open('dictionary.csv', 'r') as f:
        rdr = csv.reader(f, delimiter=';')
        rows = list(rdr)

    deleted = False
    with open('dictionary.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        for row in rows:
            word = row[0].strip()
            pos = row[1].strip()
            definition = row[2].strip()
            if word == selected_word and pos == selected_pos and definition == selected_definition:
                deleted = True
                continue
            writer.writerow(row)

    if deleted:
        messagebox.showinfo("Success", "Record deleted successfully.")
        refresh_dropdown()
        refresh_listbox()
        clear_fields()
    else:
        messagebox.showwarning("No Matching Record", "No record found with the provided information.")


def clear_fields():
    """
    Clears the input fields for word, part-of-speech, definition, synonyms, and antonyms,
    resetting them to their default (empty) state.
    """
    word_entry.delete(0, tk.END)
    definition_entry.delete(0, tk.END)
    synonyms_entry.delete(0, tk.END)
    antonyms_entry.delete(0, tk.END)


def refresh_dropdown():
    """
    Refreshes the word dropdown with the updated list of words from the dictionary.

    Retrieves the list of words from the CSV file and populates the word dropdown (`word_dropdown`) with the
    updated set of unique words. It also sets the default selected option to "Select a word".
    """
    word_dropdown.set("Select a word")
    word_menu['menu'].delete(0, 'end')

    words_set = set()
    with open('dictionary.csv', 'r') as f:
        rdr = csv.reader(f, delimiter=';')
        for row in rdr:
            words_set.add(row[0])

    for word in words_set:
        word_menu['menu'].add_command(label=word, command=lambda value=word: word_dropdown.set(value))


def refresh_listbox():
    """
    Refreshes the word listbox with the updated list of words from the dictionary.

    Retrieves the list of words from the CSV file and populates the word listbox
    (`word_listbox`) with the updated list of words. It also configures the listbox to display the
    word entries in a scrollable manner.
    """
    selected_word = word_dropdown.get()
    listbox.delete(0, tk.END)

    with open('dictionary.csv', 'r') as f:
        rdr = csv.reader(f, delimiter=';')
        for row in rdr:
            if row[0] == selected_word:
                listbox.insert(tk.END, "Part-of-Speech: " + row[1])
                listbox.insert(tk.END, "Definition: " + row[2])
                listbox.insert(tk.END, "Synonyms: " + row[3])
                listbox.insert(tk.END, "Antonyms: " + row[4])
                listbox.insert(tk.END, "")


def load_record_by_index():
    """
    Loads a word record from the dictionary based on the provided index.

    Retrieves the word record at the specified index from the CSV file and updates the fields
    (word_entry, pos_dropdown, definition_entry, synonyms_entry, and antonyms_entry) with the loaded information.
    The record number can be found by examining the word values when loaded into the listbox.
    The first record has a value of 1, not 0.
    If the index is out of range or the CSV file cannot be read, an error message is displayed.
    If the index is valid, but the record is not found, the fields are cleared.
    """
    index = int(index_entry.get())

    word = word_dropdown.get().strip()

    if not word:
        messagebox.showerror("Empty Word", "Please enter a word.")
        return

    with open('dictionary.csv', 'r') as f:
        rdr = csv.reader(f, delimiter=';')
        count = 0

        for row in rdr:
            if row[0].strip() == word:
                count += 1
                if count == index:
                    selected_record = row
                    break
        else:
            messagebox.showerror("Word Not Found", "The word was not found in the dictionary.")
            return

    word = selected_record[0].strip()
    pos = selected_record[1].strip()
    definition = selected_record[2].strip()
    synonyms = selected_record[3].strip()
    antonyms = selected_record[4].strip()

    word_entry.delete(0, tk.END)
    word_entry.insert(0, word)
    pos_dropdown.set(pos)
    definition_entry.delete(0, tk.END)
    definition_entry.insert(0, definition)
    synonyms_entry.delete(0, tk.END)
    synonyms_entry.insert(0, synonyms)
    antonyms_entry.delete(0, tk.END)
    antonyms_entry.insert(0, antonyms)


def edit_entry():
    """
    Updates the details of a selected word in the dictionary.

    This function retrieves the selected word from the word listbox (`word_listbox`) and the updated details
    (part-of-speech, definition, synonyms, antonyms) entered in the update word form (`pos_entry`, `definition_entry`,
    `synonyms_entry`, `antonyms_entry`). It modifies the corresponding entry in the CSV file with the updated details,
    refreshes the word dropdown and listbox, and displays a success message.
    """
    index = int(index_entry.get())

    word = word_dropdown.get().strip()

    if not word or word == "Select a word":
        messagebox.showerror("Empty Word", "Please enter a word.")
        return

    with open('dictionary.csv', 'r') as f:
        rdr = csv.reader(f, delimiter=';')
        count = 0
        rows = list(rdr)

    edited = False
    with open('dictionary.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        for row in rows:
            if row[0].strip() == word:
                count += 1
                if count == index:
                    edited = True
                    writer.writerow([word_entry.get(),
                                     pos_dropdown.get(), definition_entry.get(),
                                     synonyms_entry.get(), antonyms_entry.get()])
                else:
                    writer.writerow(row)
            else:
                writer.writerow(row)

    if edited:
        messagebox.showinfo("Success", "Record edited successfully.")
        refresh_dropdown()
        refresh_listbox()
    else:
        messagebox.showwarning("No Matching Record", "No record found with the provided information.")


window = tk.Tk()
window.title("Dictionary")

word_label = tk.Label(window, text="Word:")
pos_label = tk.Label(window, text="Part-of-Speech:")
definition_label = tk.Label(window, text="Definition:")
synonyms_label = tk.Label(window, text="Synonyms:")
antonyms_label = tk.Label(window, text="Antonyms:")

word_entry = tk.Entry(window)
pos_dropdown = tk.StringVar(window)
pos_dropdown.set("Select a part-of-speech")
pos_menu = tk.OptionMenu(window, pos_dropdown, "noun", "verb", "adjective", "adverb", "other")
definition_entry = tk.Entry(window)
synonyms_entry = tk.Entry(window)
antonyms_entry = tk.Entry(window)

index_label = tk.Label(window, text="Record Index \n (in listbox):")
index_entry = tk.Entry(window)
index_button = tk.Button(window, text="Load Record", command=load_record_by_index, bg="#d0d0d0")

word_dropdown = tk.StringVar()
word_menu = tk.OptionMenu(window, word_dropdown, "Select a word")

scrollbar = Scrollbar(window)

listbox = tk.Listbox(window)

add_button = tk.Button(window, text="Add Word", command=add_word, bg="#2a4c29", fg="#f3f7d6")
edit_button = tk.Button(window, text="Edit Entry", command=edit_entry, bg="#f2f7ca")
load_button = tk.Button(window, text="Load Into Listbox", command=load_word, bg="#d0d0d0")
delete_button = tk.Button(window, text="Delete Definition", command=delete_record, bg="#731d1d", fg="#f3f7d6")
pronounce_button = tk.Button(window, text="Pronounce Word", command=pronounce_word, bg="#b2c9f2")

voice_option = tk.StringVar()
male_radio = tk.Radiobutton(window, text="M", variable=voice_option, value="M", command=select_voice)
female_radio = tk.Radiobutton(window, text="F", variable=voice_option, value="F", command=select_voice)
voice_option.set("M")

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

word_entry.config(width=20)
definition_entry.config(width=20)
synonyms_entry.config(width=20)
antonyms_entry.config(width=20)

listbox.config(width=40)
index_entry.config(width=5)

word_label.grid(row=0, column=0, sticky=tk.E)
word_entry.grid(row=0, column=1, sticky=tk.W)
pos_label.grid(row=1, column=0, sticky=tk.E)
pos_menu.grid(row=1, column=1, sticky=tk.W)
definition_label.grid(row=2, column=0, sticky=tk.E)
definition_entry.grid(row=2, column=1, sticky=tk.W)
synonyms_label.grid(row=3, column=0, sticky=tk.E)
synonyms_entry.grid(row=3, column=1, sticky=tk.W)
antonyms_label.grid(row=4, column=0, sticky=tk.E)
antonyms_entry.grid(row=4, column=1, sticky=tk.W)
word_menu.grid(row=1, column=2)
load_button.grid(row=2, column=2, pady=5)
pronounce_button.grid(row=0, column=2, sticky=tk.N, pady=5)
listbox.grid(row=3, column=2, rowspan=4, padx=10, pady=10)
scrollbar.grid(row=3, column=3, rowspan=4, sticky=tk.N + tk.S)
add_button.grid(row=5, column=1, sticky=tk.N + tk.W)
edit_button.grid(row=6, column=1, sticky=tk.N + tk.W)
delete_button.grid(row=7, column=1, sticky=tk.N + tk.W)
index_label.grid(row=8, column=2, sticky=tk.W)
index_entry.grid(row=8, column=2)
index_button.grid(row=9, column=2, pady=5)
male_radio.grid(row=0, column=4, sticky=tk.W)
female_radio.grid(row=1, column=4, sticky=tk.W)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

refresh_dropdown()

window.mainloop()
