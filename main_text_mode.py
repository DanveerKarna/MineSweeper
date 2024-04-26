"""
Author: DanveerKarna
© 2024
"""

import tkinter as tk
import numpy as np
import random
from pygame import mixer

# Handling the flags

def on_right_click(root, btnVal, buttons, row, col, flagged, rows=8, cols=8, mines=16):

    flag_cnt = 0
    
    if(buttons[row][col].cget("state") != "disabled" and flagged[row][col] != 0):
        buttons[row][col].config(text = "")
        play_sound("unflag.wav")
        flagged[row][col] = 0
    elif(buttons[row][col].cget("state") != "disabled" and flagged[row][col] == 0):
        for r in range(rows):
            for c in range(cols):
                if(flagged[r][c] == 1):
                    flag_cnt += 1
                if(flag_cnt == round(mines*(rows*cols)/100)):
                    flag_out_of_stock_popup(root)
                    return
        buttons[row][col].config(text = "\U0001F6A9")
        play_sound("flag.wav")
        flagged[row][col] = 1
        
# Sound section

def play_sound(fileName):
    mixer.init()
    mixer.music.load(fileName)
    mixer.music.play()

def play_sound_infinite(fileName):
    mixer.init()  # Initialize the mixer
    mixer.music.load(fileName)  # Load the sound file
    mixer.music.play(-1) # Play the sound in an infinite loop

def play_sound_nonzero(fileName):
    mixer.music.load(fileName)
    mixer.music.play()

def play_sound_zero(fileName):
    mixer.music.load(fileName)
    mixer.music.play()

# Functions for different levels

def level8(init, root):
    timer_label.destroy()
    for widget in root.grid_slaves():
        widget.grid_forget()
    init(root, 1, 8, 8)
    
def level16(init, root):
    timer_label.destroy()
    for widget in root.grid_slaves():
        widget.grid_forget()
    init(root, 1, 16, 16)
    
def level24(init, root):
    timer_label.destroy()
    for widget in root.grid_slaves():
        widget.grid_forget()
    init(root, 1, 24, 24)

def level_custom(init, root, popup, rows, cols, mines):
    close_popup(popup)
    timer_label.destroy()
    for widget in root.grid_slaves():
        widget.grid_forget()
    init(root, 1, rows, cols, mines)    

def new(init, root, rows, cols, mines):
    timer_label.destroy()
    for widget in root.grid_slaves():
        widget.grid_forget()
    init(root, 1, rows, cols, mines) 

# Handling the popups

def close_popup_with_music(popup):
    popup.destroy()
    mixer.music.stop()  # Stop playing the sound when the window is closed

def close_popup(popup):
    popup.destroy()

def close_gamewon_popup(popup, Name, rows, cols, mines):
    popup.destroy()
    mixer.music.stop()  # Stop playing the sound when the window is closed
    with open(str(rows)+"x"+str(cols)+"_"+str(round(mines*(rows*cols)/100))+".csv", "a+") as History:
        History.write(Name + "," + timer_label.cget("text")[4:len(timer_label.cget("text"))].split(":")[0].strip() + " m" + " " + timer_label.cget("text")[4:len(timer_label.cget("text"))].split(":")[1].strip() + " s"  + "\n")


def close_about_popup(popup, buttons, rows, cols):
    popup.destroy()
    mixer.music.stop()
    for r in range(rows):
        for c in range(cols):
            if(buttons[r][c].cget("state") != "disabled"):
                play_sound_infinite("music.ogg")

def open_about_popup(root, buttons, rows, cols):
    popup = tk.Toplevel(root)
    
    # Calculate the position to center the popup window with respect to the root window
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()
    x = root_x + (root_width - popup_width) // 2
    y = root_y + (root_height - popup_height) // 2
    
    popup.geometry(f"+{x}+{y}")
    popup.configure(bg="#98FB98")
    popup.overrideredirect(True)
    label = tk.Label(popup, text="\u00A9 2024 \n Author: DanveerKarna", font=12, fg="White", bg="Black")
    label.pack(padx=20, pady=25)

    close_button = tk.Button(popup, text="X", command=lambda rows=rows, cols=cols: close_about_popup(popup, buttons, rows, cols), font = 12, fg="White", bg="Black")
    close_button.pack(pady=15)    

def open_history_popup(root, rows, cols, mines):
    popup = tk.Toplevel(root)
    # Calculate the position to center the popup window with respect to the root window
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()
    x = root_x + (root_width - popup_width) // 2
    y = root_y + (root_height - popup_height) // 2
    
    popup.geometry(f"+{x}+{y}")
    popup.overrideredirect(True)
    play_sound("winners.ogg")
    
    Display = "\n"
    Ranking = []
    try:
        with open(str(rows)+"x"+str(cols)+"_"+str(round(mines*(rows*cols)/100))+".csv", "r") as History:
            content = History.readlines()
            for row in content:
                x = row.split(",")[1].strip().split(" m")[0]
                y = row.split(",")[1].strip().split(" m")[1].strip(" s")
                if x == "" and y != "":
                    s = 0 + int(row.split(",")[1].strip().split(" m")[1].strip(" s"))
                elif x != "" and y == "":
                    s = int(row.split(",")[1].strip().split(" m")[0])*60
                elif x == "" and y == "":
                    s = 0
                else:
                    s = int(row.split(",")[1].strip().split(" m")[0])*60 + int(row.split(",")[1].strip().split(" m")[1].strip(" s"))
                Ranking.append((s, row.split(",")[0].strip()))
            Ranking.sort()
        
            cnt = 0
        
            medals = ["\U0001F947", "\U0001F948", "\U0001F949"]
            for r in Ranking:
                if(cnt > 2):
                    break
                Display += (medals[cnt] + "  " + r[1] + "    " + (str(r[0]//60) + "m ")  + str(r[0]%60) + "s" + " " + "\n") if (int(str(r[0]//60)) != 0) else (medals[cnt] + "  " + r[1] + "    " + str(r[0]%60) + "s" + " " + "\n")
                cnt += 1
        label = tk.Label(popup, text=Display, font=16, bg="Black", fg="White")
    except:
        label = tk.Label(popup, text="No winners yet", font=16, bg="Black", fg="White")
    label.pack(padx=10, pady=5)

    close_button = tk.Button(popup, text="X", command=lambda: close_about_popup(popup, buttons, rows, cols), font = 12, fg="White", bg="Black")
    close_button.pack(pady=5)    


def custom_popup(init, root):

    popup = tk.Toplevel(root)
    popup.configure(bg="#98FB98")
    popup.overrideredirect(True)
    
    # Function to update the mines value
    def update_mines_value():
        mines_value.set(mines_spinbox.get())

    # Function to update the rows value
    def update_rows_value():
        rows_value.set(rows_spinbox.get())

    # Function to update the columns value
    def update_cols_value():
        cols_value.set(cols_spinbox.get())

    # Create and position the input fields and labels
    tk.Label(popup, text="Height", font=("Helvetica", 12), bg="#98FB98").grid(row=0, column=0, padx=10, pady=5)
    rows_value = tk.StringVar()
    rows_value.set("8")  # Default value for rows
    rows_spinbox = tk.Spinbox(popup, from_=4, to=25, increment=1, width=10, font=("Helvetica", 12), textvariable=rows_value)
    rows_spinbox.grid(row=1, column=0, padx=10, pady=5)

    tk.Label(popup, text="Width", font=("Helvetica", 12), bg="#98FB98").grid(row=2, column=0, padx=10, pady=5)
    cols_value = tk.StringVar()
    cols_value.set("8")  # Default value for columns
    cols_spinbox = tk.Spinbox(popup, from_=4, to=25, increment=1, width=10, font=("Helvetica", 12), textvariable=cols_value)
    cols_spinbox.grid(row=3, column=0, padx=10, pady=5)

    tk.Label(popup, text="% Mines", font=("Helvetica", 12), bg="#98FB98").grid(row=4, column=0, padx=10, pady=5)
    mines_value = tk.StringVar()
    mines_value.set("16")  # Default value for mines
    mines_spinbox = tk.Spinbox(popup, from_=16, to=75, increment=1, width=10, font=("Helvetica", 12), textvariable=mines_value)
    mines_spinbox.grid(row=5, column=0, padx=10, pady=5)

    # Create and position the play button
    play_button = tk.Button(popup, text="\u25B6", command=lambda: level_custom(init, root, popup, int(rows_value.get()), int(cols_value.get()), int(mines_value.get())), font=("Helvetica", 12), bg="#FFD700", bd=2)
    play_button.grid(row=6, column=0, padx=10, pady=5)

    close_button = tk.Button(popup, text="X", command=lambda: popup.destroy(), font=("Helvetica", 12), bg="Black", bd=2, fg="White")
    close_button.grid(row=7, column=0, padx=10, pady=5)

    # Center-align all widgets
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=1)
    popup.grid_rowconfigure(3, weight=1)
    popup.grid_rowconfigure(4, weight=1)
    popup.grid_rowconfigure(5, weight=1)
    popup.grid_rowconfigure(6, weight=1)
    popup.grid_columnconfigure(0, weight=1)

    # Calculate the position to center the popup window with respect to the root window
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()
    x = root_x + (root_width - popup_width) // 2
    y = root_y + (root_height - popup_height) // 2
    popup.geometry(f"+{x}+{y}")

    # Focus on the mines Spinbox initially
    mines_spinbox.focus_set()

    
def flag_out_of_stock_popup(root):

    popup = tk.Toplevel(root)
    
    # Calculate the position to center the popup window with respect to the root window
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()
    x = root_x + (root_width - popup_width) // 2
    y = root_y + (root_height - popup_height) // 2
    
    popup.geometry(f"+{x}+{y}")    
    popup.configure(bg="#FF2400")
    popup.overrideredirect(True)
    play_sound("wrong.wav")
    label = tk.Label(popup, text="\U0001F6A9 \n Out of stock !", font=12, fg="White", bg="Black")
    label.pack(padx=20, pady=25)

    close_button = tk.Button(popup, text="X", command=lambda: close_popup_with_music(popup), font = 12, fg="White", bg="Black")
    close_button.pack(pady=15)

def open_gameover_popup(root):

    popup = tk.Toplevel(root)
    
    # Calculate the position to center the popup window with respect to the root window
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()
    x = root_x + (root_width - popup_width) // 2
    y = root_y + (root_height - popup_height) // 2
    
    popup.geometry(f"+{x}+{y}")
    popup.configure(bg="#FF2400")
    popup.overrideredirect(True)
    play_sound("gameOver.wav")
    label = tk.Label(popup, text="\U0001F480 \n Game over !", font=12, fg="White", bg="Black")
    label.pack(padx=20, pady=25)

    close_button = tk.Button(popup, text="X", command=lambda: close_popup_with_music(popup), font = 12, fg="White", bg="Black")
    close_button.pack(pady=15)

def open_gamewon_popup(root, rows, cols, mines):

    popup = tk.Toplevel(root)
    
    # Calculate the position to center the popup window with respect to the root window
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()
    x = root_x + (root_width - popup_width) // 2
    y = root_y + (root_height - popup_height) // 2
    
    popup.geometry(f"+{x}+{y}")
    popup.configure(bg="#32CD32")
    popup.overrideredirect(True)
    play_sound("gameWin.wav")
        
    label = tk.Label(popup, text=timer_label.cget("text")+"\n 🏆 \n You won !", font=12, fg="White", bg="#FF8C00")
    label.pack(padx=20, pady=25)
    Name = tk.Entry(popup)
    Name.pack(pady=15)
    close_button = tk.Button(popup, text="X", command=lambda: close_gamewon_popup(popup, Name.get(), rows, cols, mines), font = 12, fg="White", bg="#FF8C00")
    close_button.pack(pady=15)

def start_timer():
    global timer_seconds, timer_label
    timer_seconds = 0
    update_timer()

def update_timer():
    global timer_seconds, timer_label, timer_paused
    if not timer_paused:
        timer_label.config(text="⏲   "+"{}".format(timer_seconds//60)+" : "+"{}".format(timer_seconds%60))
        timer_seconds += 1
        timer_label.after(1000, update_timer)

def pause_timer():
    global timer_paused
    timer_paused = True

def resume_timer():
    global timer_paused
    timer_paused = False
    update_timer()

# Handling the random generation of the bombs

def generate_random_tuple(row=8, col=8):
    x = random.randint(1, row)
    y = random.randint(1, col)
    return (x, y)

# Unlocking the cells when a Zero cell is clicked

def open_help(visited, btnVal, buttons, row, col, flagged, rows=8, cols=8):

    stack = [(row, col)]  # Initialize a stack with the starting cell

    while stack:
        r, c = stack.pop()  # Pop the top cell from the stack

        if btnVal[r][c] == "*":
            continue  # Skip coloring cells adjacent to bombs

        # List to store the coordinates of adjacent cells
        adjacent_cells = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
                          (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]

        for nr, nc in adjacent_cells:
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                visited[nr][nc] = 1
                if btnVal[nr][nc] == 0:
                    buttons[nr][nc].config(bg="#32CD32", text="", state="disabled")
                    stack.append((nr, nc))  # Add the adjacent cell to the stack for further exploration
                elif btnVal[nr][nc] != "*":
                    buttons[nr][nc].config(bg="#FFD700", text=str(btnVal[nr][nc]), state="disabled")
                if flagged[nr][nc] == 1:
                    flagged[nr][nc] = 0  # Clear flag if present

# Handling the left-click

def button_click(root, cnt, visited, btnVal, buttons,row, col, flagged, rows=8, cols=8, mines=16):
    global timer_started
    if not timer_started:
        start_timer()
        timer_started = True
    if(buttons[row][col].cget("text") == "\U0001F6A9"):
        return

    if(btnVal[row][col] == "*"):
        buttons[row][col].config(bg = "#FF2400", text="💣")
        for r in range(rows):
            for c in range(cols):
                if(btnVal[r][c] == "*"):
                    if(flagged[r][c] == 1):
                        buttons[r][c].config(bg = "#FF2400")
                    else:
                        buttons[r][c].config(text="💣")
                buttons[r][c].config(state="disabled")
        pause_timer()
        open_gameover_popup(root)
    elif(btnVal[row][col] == 0):
        play_sound_zero("unlock.mp3")
        visited[row][col] = 1
        buttons[row][col].config(bg = "#32CD32", text = "", state = "disabled")
        open_help(visited, btnVal, buttons, row, col, flagged, rows, cols)
    else:
        play_sound_nonzero("click.wav")
        buttons[row][col].config(bg = "#FFD700", text = str(btnVal[row][col]))
        visited[row][col] = 1
        buttons[row][col].config(state="disabled")
    for i in range(rows):
        for j in range(cols):
            if visited[i][j] == 1:
                cnt += 1
    if((rows*cols)-cnt == round(mines*(rows*cols)/100)):
        for r in range(rows):
            for c in range(cols):
                if(btnVal[r][c] == "*"):
                    if(flagged[r][c] == 1):
                        buttons[r][c].config(bg = "#FF2400")
                    else:
                        buttons[r][c].config(text="💣")
                buttons[r][c].config(state="disabled")
        pause_timer()
        open_gamewon_popup(root, rows, cols, mines)

# Creating the grid

class Grid:

    def create_grid(root, bombs, buttons, cnt, flagged, visited, btnVal, rows=8, cols=8, mines=16):
        #buttons = []  # Two-dimensional list to store buttons
        for row in range(rows):
            button_row = []  # List to store buttons in each row
            for col in range(cols):
                button = tk.Button(root, text="", command=lambda visited=visited, row=row, col=col: button_click(root, cnt, visited, btnVal, buttons,row, col, flagged, rows, cols, mines), width=BUTTON_SIZE, height=BUTTON_SIZE)
                button.grid(row=row+1, column=col)
                button_row.append(button)
            buttons.append(button_row)

        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(0)
            flagged.append(row)
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(0)
            btnVal.append(row)
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(0)
            visited.append(row)

        for r in range(rows):
            for c in range(cols):
                if(bombs[r][c] == 1):
                    btnVal[r][c] = "*"
                buttons[r][c].bind("<Button-3>", lambda event, btnVal=btnVal, buttons=buttons, row=r, col=c, flagged=flagged: on_right_click(root, btnVal, buttons, row, col, flagged, rows, cols, mines))
        for r in range(rows):
            for c in range(cols):
                if(btnVal[r][c] != "*"):
                    if(c-1 >= 0):
                        if(btnVal[r][c-1] == "*"):
                            btnVal[r][c] += 1
                    if(c+1 < cols):
                        if(btnVal[r][c+1] == "*"):
                            btnVal[r][c] += 1                
                    if(r-1 >=0):
                        if(btnVal[r-1][c] == "*"):
                            btnVal[r][c] += 1
                        if(c-1 >=0):
                            if(btnVal[r-1][c-1] == "*"):
                                btnVal[r][c] += 1
                        if(c+1 < cols):
                            if(btnVal[r-1][c+1] == "*"):
                                btnVal[r][c] += 1
                    if(r+1 < rows):
                        if(btnVal[r+1][c] == "*"):
                            btnVal[r][c] += 1
                        if(c-1 >=0):
                            if(btnVal[r+1][c-1] == "*"):
                                btnVal[r][c] += 1
                        if(c+1 < cols):
                            if(btnVal[r+1][c+1] == "*"):
                                btnVal[r][c] += 1
        return buttons

def initialize(root, BtnSize=1, rows=8, cols=8, mines=16):

    global timer_label
    global timer_started, timer_paused
    
    # Initialize timer label

    timer_started = False
    timer_paused = False
    timer_seconds = 0
    timer_label = None

    global cnt, BUTTON_SIZE, flagged, visited, btnVal, buttons
    
    BUTTON_SIZE = BtnSize
    cnt = 0
    flagged = []
    visited = []
    btnVal = []
    buttons = []

    timer_label = tk.Label(root, text="⏲   0 : 0", bg="Black", fg="Red", padx=20)
    timer_label.grid(row=0, column=0, columnspan=cols)

    arr = np.zeros([rows,cols])
    store = []
    while(len(store) != round(mines*(rows*cols)/100)):
        x,y = generate_random_tuple(rows, cols)
        if (x,y) not in store:
            store.append((x,y))
        arr[x-1,y-1] = 1
    buttons = Grid.create_grid(root, arr, buttons, cnt, flagged, visited, btnVal, rows, cols)
    play_sound_infinite("music.ogg")

    load(buttons, rows, cols, mines)


def load(buttons, rows, cols , mines):

    # Create a menu bar
    menubar = tk.Menu(root)
    # Create File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    # Create Sub-menu under Level menu
    sub_menu = tk.Menu(file_menu, tearoff=False)
    file_menu.add_command(label="\U0001F501 Replay", command=lambda rows=rows, cols=cols, mines=mines: new(initialize, root, rows, cols, mines))
    sub_menu.add_command(label="\U0001F530 Beginner", command=lambda: level8(initialize, root))
    sub_menu.add_command(label="\U00002B50 Intermediate", command=lambda: level16(initialize, root))
    sub_menu.add_command(label="\U0001F525 Expert", command=lambda: level24(initialize, root))
    sub_menu.add_separator()
    sub_menu.add_command(label="🛠️ Custom", command=lambda: custom_popup(initialize, root))
    file_menu.add_cascade(label="\U0001FA9C Level", menu=sub_menu)    
    file_menu.add_command(label="\U0001F3C6 Winners", command=lambda rows=rows, cols=cols, mines=mines: open_history_popup(root, rows, cols, mines))
    file_menu.add_command(label="\U0001F4DC About", command=lambda rows=rows, cols=cols, mines=mines: open_about_popup(root, buttons, rows, cols))     
    file_menu.add_separator()
    file_menu.add_command(label="\U0001F6AA Exit", command=lambda buttons=buttons: root.destroy()) 
    menubar.add_cascade(label=" \u2630 ", menu=file_menu)
    root.resizable(False, False)
    root.title("🎮 MineSweeper")
    root.config(menu=menubar)
    
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    initialize(root)
