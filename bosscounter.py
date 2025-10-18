import keyboard # YOU MUST INSTALL KEYBOARD MODULE FOR THIS CODE TO WORK
import json
import os
import atexit

listening = True

filename = "bossdata.json"
if not os.path.exists(filename): # if it doesn't already exist, create it and add list
    data = {"bosses": {}, "saved_boss": None}
    with open(filename,"w") as file: # saves the file
        json.dump(data, file)
else: # else read existing file
    with open(filename, "r") as file:
        data = json.load(file)

bosses = data["bosses"]

# who is our selected boss on startup?
if len(bosses) == (0):
    selected_boss = None
else:
    if data["saved_boss"] == None:
        selected_boss = list(bosses)[0]
    else:
        for boss in bosses:
            if boss == data["saved_boss"]:
                selected_boss = data["saved_boss"]
                break
            else:
                selected_boss = selected_boss = list(bosses)[0]

# how to print
if selected_boss == None:
    print_selected_boss = "selected boss"
else:
    print_selected_boss = selected_boss

# tutorial msg
print(f"""Current boss selected: {selected_boss}
Press 1 to add death to {print_selected_boss}.
Press 2 to remove death from {print_selected_boss}
Press 3 to add a new boss.
Press 4 to rename {print_selected_boss}.
Press 5 to display bosses.
Press Ctrl + Alt + Left/Right arrow key to switch selected boss.
Press Delete to delete {print_selected_boss}""")

def save_file():
    with open(filename, "w") as file:
        json.dump(data, file)

# + 1
def plus_death(event):  
    if selected_boss == None:
        print("Please select a boss or add a new one.")
        return
    
    else:
        bosses[selected_boss] = bosses[selected_boss] + 1
        save_file()
        print(f"+1 death to {selected_boss}. Total deaths: {bosses[selected_boss]}")

# - 1
def min_death(event):
    if event.name == ('down'): # safeguard to prevent arrow keys triggering functions
        return
    
    if selected_boss == None:
        print("Please select a boss or add a new one.")
        return

    else:
        bosses[selected_boss] = bosses[selected_boss] - 1
        save_file()
        print(f"-1 death from {selected_boss}. Total deaths: {bosses[selected_boss]}")

# cycle through bosses
def switch_boss(operator):
    global selected_boss
    if len(bosses) == 0:
        print("You don't have any bosses to switch to. Press 3 to add a boss")
        return
    
    if selected_boss == None: # if no boss selected just select the first one in the list
        selected_boss = list(bosses)[0]
        data["saved_boss"] = selected_boss
        save_file()
        print(f"Selected {selected_boss}. Deaths: {bosses[selected_boss]}")
        return
    
    boss_index = boss_indexer()

    if operator == "+": # don't fucking question this code, it works
        if boss_index + 1 == len(bosses):
            selected_boss = list(bosses)[0]
        else:
            selected_boss = list(bosses)[boss_index + 1]

    elif operator == "-":
        if boss_index - 1 < 0:
            selected_boss = list(bosses)[len(bosses) - 1]
        else:
            selected_boss = list(bosses)[boss_index - 1]

    print(f"Selected {selected_boss}. Deaths: {bosses[selected_boss]}")
    data["saved_boss"] = selected_boss
    save_file()

# add new boss
def add_boss(event):
    keyboard.unhook_key('3')    
    keyboard.send('backspace')
    new_boss = input(f"Please enter a boss name (enter cancel to cancel): ")

    if new_boss == "" or new_boss == "cancel":
        print("Boss not added.")
        keyboard.on_press_key('3', add_boss)
        return
    
    elif new_boss in bosses:
        print(f"{new_boss} already exists. Please enter another boss name.")
        keyboard.on_press_key('3', add_boss)
        return
    
    else:
        bosses[new_boss] = 0
        global selected_boss
        selected_boss = new_boss
        print(new_boss, "added and selected.")
        data["saved_boss"] = selected_boss
        save_file()
        keyboard.on_press_key('3', add_boss)
        return

# list all bosses
def display_boss(event):
    if len(bosses) == 0:
        print("You don't have any bosses added yet.")
        return
    
    print("----------List of Bosses----------")
    for boss in bosses:
        print(f"{boss}: {bosses[boss]} deaths.")
    print("----------------------------------")

def rename_boss(event):
    if event.name == ('left'): # arrow keys trigger 2, 4, 6 and 8 as well.
        return
    
    keyboard.unhook_key('3')
    global selected_boss
    if len(bosses) == 0:
        print("You don't have any bosses to rename.")
        keyboard.on_press_key('4', rename_boss)
        return
    
    elif selected_boss == None:
        print("Please select a boss to rename.")
        keyboard.on_press_key('4', rename_boss)
        return
    
    new_name = input(f"Enter new boss name for {selected_boss} (enter cancel to cancel): ")

    if new_name == "cancel":
        print(f"{selected_boss} not renamed.")
        keyboard.on_press_key('4', rename_boss)
        return
    
    elif new_name in bosses:
        print(f"{new_name} already exists. Please enter another boss name")
        keyboard.on_press_key('4', rename_boss)
        return
    
    else:
        boss_deaths = bosses[selected_boss]
        bosses.pop(selected_boss)
        bosses[new_name] = boss_deaths
        print(f"{selected_boss} renamed to {new_name}.")
        selected_boss = new_name
        data["saved_boss"] = selected_boss
        keyboard.on_press_key('4', rename_boss)
        save_file()

# delete boss
def delete_boss(event):
    global selected_boss
    if len(bosses) == 0:
        print("You don't have any bosses to delete.")
        return

    if selected_boss == None:
        print("Please select a boss to delete.")
        return
    confirmation = input(f"Are you sure you want to delete {selected_boss}? Type delete to confirm. ")

    if confirmation != "delete":
        print(f"{selected_boss} was not deleted.")
        return
    
    else:
        print(f"{selected_boss} has been deleted.")
        bosses.pop(selected_boss)
        if data["saved_boss"] == selected_boss:
            data["saved_boss"] = None
        save_file()
        selected_boss = None

# get boss index
def boss_indexer():
    boss_index = 0
    for boss in bosses:
        if boss == selected_boss:
            return boss_index
        else:
            boss_index += 1

# while listening:
keyboard.on_press_key('1', plus_death)
keyboard.on_press_key('2', min_death)
keyboard.add_hotkey('ctrl+alt+left', switch_boss, args=["-"])
keyboard.add_hotkey('ctrl+alt+right', switch_boss, args=["+"])
keyboard.on_press_key('3', add_boss)
keyboard.on_press_key('4', rename_boss)
keyboard.on_press_key('5', display_boss)
keyboard.on_press_key('delete', delete_boss)

def exit():
    print("Saving...")
    data["saved_boss"] = selected_boss
    save_file()

atexit.register(exit) 
keyboard.wait('F12') # keeps the program running & listening