import json
import tkinter as tk
import random

# load json file and randomize word sequence #
with open('common.json') as file:
    words = json.load(file)['commonWords']

random.shuffle(words)

# declaring constants #
DISPLAY_WORD_COUNT = 7

# declaring variables #
input_buffer = ''
correct_words = 0
counter = 60
first_char = True


def on_key_press(key):

    # declare globals
    global words, input_buffer, correct_words, first_char

    # when backspace reset its color and remove last character else add to buffer
    if key.char == '\b':
        i = input_buffer.index(input_buffer[-1])
        text_widget.tag_config(f'{i}', foreground="black")

        input_buffer = input_buffer[:-1]
    else:
        input_buffer += key.char

    # update the displayed text to the input buffer
    display_text.configure(text=input_buffer)

    # if is alphabetical character check if it corresponds with the same letter in the word, and change color correctly
    if key.char.isalpha():

        for n in range(len(input_buffer)):
            try:
                if input_buffer[n] == words[0][n]:  # if char from buffer is equal to char in word make char green = true
                    text_widget.tag_add(f'{n}', f"1.{n}", f"1.{n + 1}")
                    text_widget.tag_config(f'{n}', foreground="green")
                else:  # else make char red = false
                    text_widget.tag_add(f'{n}', f"1.{n}", f"1.{n + 1}")
                    text_widget.tag_config(f'{n}', foreground="red")
            except IndexError:
                continue

    # check if space pressed
    if key.char == ' ':

        if input_buffer[:-1] == words[0]:  # check if word was correctly typed (remove last char, bc last char is space)
            correct_words += 1

        # remove word and reset input buffer
        words.pop(0)
        input_buffer = ''

        # update text label
        text_widget.configure(state='normal')  # make writeable
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, ' '.join(words[:DISPLAY_WORD_COUNT]))
        text_widget.configure(state='disabled')  # make readonly

    # if the first char typed start the counter
    if first_char:
        app.after(0, counting)
        first_char = False


def counting():
    global counter
    counter -= 1

    # display wpm, unbind Keypress event and return (end counting), if counter hits 0
    if counter == 0:
        text_widget.destroy()
        display_text.destroy()
        counter_label.destroy()
        tk.Label(app, text=f'WPM: {correct_words}', font=('Helvetica', 15, 'bold')).pack()

        app.unbind('<KeyPress>')

        return

    counter_label.configure(text=f'{counter}')

    app.after(1000, counting)


# UI #
app = tk.Tk()
app.wm_title('TypeSpeed Tester')
app.geometry('500x200')
app.wm_resizable(False, False)
app.bind('<KeyPress>', on_key_press)  # binding keypress event

counter_label = tk.Label(app, text='60')
counter_label.pack()

display_text = tk.Label(app, text='')
display_text.pack()

text_widget = tk.Text(app, font=('Helvetica', 15, 'bold'))
text_widget.pack()
text_widget.insert(1.0, ' '.join(words[:DISPLAY_WORD_COUNT]))
text_widget.configure(state='disabled')  # make readonly

app.mainloop()
