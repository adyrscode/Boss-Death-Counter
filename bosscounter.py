import keyboard
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
if len(bosses) == (0):
    selected_boss = None
else:
    selected_boss = data["saved_boss"]

if selected_boss == None:
    print_selected_boss = "selected boss"
else:
    print_selected_boss = selected_boss

print(f"""Current boss selected: {print_selected_boss}
Press 1 to add death to {print_selected_boss}.
Press 2 to remove death from {print_selected_boss}
Press 3 to add a new boss.
Press 4 to display bosses.
Press Ctrl + Shift + Left/Right arrow key to switch selected boss.
Press Delete to delete {print_selected_boss}""")

def save_file():
    with open(filename, "w") as file: # saves the file
        json.dump(data, file)

def plus_death(event): # event_object is passed by keyboard to this function
    if selected_boss == None:
        print("Please select a boss or add a new one.")
    else:
        bosses[selected_boss] = bosses[selected_boss] + 1
        save_file()
        print(f"+1 death to {selected_boss}. Total deaths: {bosses[selected_boss]}")

def min_death(event):
    if event.name == ('down'): # safeguard to prevent arrow keys triggering functions
        return
    
    if selected_boss == None:
        print("Please select a boss or add a new one.")

    else:
        bosses[selected_boss] = bosses[selected_boss] - 1
        save_file()
        print(f"-1 death from {selected_boss}")

def switch_boss(operator):
    global selected_boss
    if selected_boss == None:
        print("You don't have any bosses to switch to yet.")
        return
    boss_index = 0
    for boss in bosses:
        if boss == selected_boss:
            break
        else:
            boss_index += 1

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

def add_boss(event):    
    global listening
    listening = False
    keyboard.send('backspace')
    new_boss = input(f"Please enter a boss name (enter {"cancel"} to cancel): ")

    if new_boss == "" or new_boss == "cancel":
        listening = True
        print("Boss not added.")
        return
    
    elif new_boss in bosses:
        listening = True
        print("Boss already exists.")
        return
    
    else:
        listening = True
        bosses[new_boss] = 0
        save_file()
        global selected_boss
        selected_boss = new_boss
        print(new_boss, "added and selected.")
        return

def display_boss(event):
    if event.name == ('left'): # arrow keys trigger 2, 4, 6 and 8 as well.
            return
    
    if len(bosses) == 0:
        print("You don't have any bosses added yet.")
        return
    
    for boss in bosses:
        print(f"{boss}{":"} {bosses[boss]} deaths.")

def delete_boss(event):
    global selected_boss
    if selected_boss == None:
        print("Please select a boss to delete.")
        return
    confirmation = input(f"Are you sure you want to delete {selected_boss}? Type {"delete"} to confirm. ")

    if confirmation != "delete":
        print(f"{selected_boss} was not deleted.")
        return
    
    else:
        bosses.pop(selected_boss)
        if data["saved_boss"] == selected_boss:
            data["saved_boss"] = None
        save_file()
        selected_boss = None

# while listening:
keyboard.on_press_key('1', plus_death)
keyboard.on_press_key('2', min_death)
keyboard.add_hotkey('ctrl+shift+left', switch_boss, args=["-"])
keyboard.add_hotkey('ctrl+shift+right', switch_boss, args=["+"])
# keyboard.on_press_key('3', switch_boss)
keyboard.on_press_key('3', add_boss)
keyboard.on_press_key('4', display_boss)
keyboard.on_press_key('delete', delete_boss)

def exit():
    print("Saving...")
    data["saved_boss"] = selected_boss
    save_file()

atexit.register(exit) 
keyboard.wait('F12') # keeps the program running & listening