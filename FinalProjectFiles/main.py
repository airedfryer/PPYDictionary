import tkinter as tk
from tkinter import messagebox
from tkinter import Scrollbar
import csv


def add_word():
    """Adds a word entry to the dictionary.csv file."""
    word = word_entry.get()
    pos = pos_dropdown.get()
    definition = definition_entry.get()
    synonyms = synonyms_entry.get()
    antonyms = antonyms_entry.get()

    if word and definition:
        with open('dictionary.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([word, pos, definition, synonyms, antonyms])

        messagebox.showinfo("Success", "Word added successfully.")
        refresh_listbox()
        clear_fields()
    else:
        messagebox.showwarning("Missing Information", "Please enter a word and definition.")


def load_word():
    """Loads the information corresponding to the currently selected word into the listbox."""
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
    """Deletes a selected record from the dictionary.csv file."""
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
    else:
        messagebox.showwarning("No Matching Record", "No record found with the provided information.")


def clear_fields():
    """Clears the input fields."""
    word_entry.delete(0, tk.END)
    definition_entry.delete(0, tk.END)
    synonyms_entry.delete(0, tk.END)
    antonyms_entry.delete(0, tk.END)


def refresh_dropdown():
    """Refreshes the word dropdown menu based on the dictionary CSV file."""
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
    """Refreshes the listbox to display information for the selected word."""
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
    """Loads a record into the input fields based on the selected word and the index
    (displayed in the listbox when the word is chosen)."""
    index = int(index_entry.get())

    word = word_dropdown.get().strip()

    if not index:
        messagebox.showerror("Index not detected", "Please enter a value into the index textbox.")
        return

    if not word:
        messagebox.showerror("Word not detected", "Please enter a word.")
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

index_label = tk.Label(window, text="Record Index \n (matches listbox):")
index_entry = tk.Entry(window)
index_button = tk.Button(window, text="Load Record", command=load_record_by_index)

word_dropdown = tk.StringVar()
word_menu = tk.OptionMenu(window, word_dropdown, "Select a word")

scrollbar = Scrollbar(window)

listbox = tk.Listbox(window)

add_button = tk.Button(window, text="Add Word", command=add_word)
load_button = tk.Button(window, text="Load Into Listbox", command=load_word)
delete_button = tk.Button(window, text="Delete Definition", command=delete_record)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=2)

word_entry.config(width=20)
definition_entry.config(width=20)
synonyms_entry.config(width=20)
antonyms_entry.config(width=20)

listbox.config(width=40)

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
listbox.grid(row=2, column=2, rowspan=4, padx=10, pady=10)
scrollbar.grid(row=2, column=3, rowspan=4, sticky=tk.N + tk.S)
add_button.grid(row=5, column=0)
load_button.grid(row=0, column=2)
delete_button.grid(row=5, column=1)
index_label.grid(row=6, column=0, sticky=tk.E)
index_entry.grid(row=6, column=1, sticky=tk.W)
index_button.grid(row=7, column=1)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

refresh_dropdown()

window.mainloop()
