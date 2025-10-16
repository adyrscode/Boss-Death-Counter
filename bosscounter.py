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

print(f"""Current boss selected: {selected_boss}
Press 1 to add death to {selected_boss}.
Press 2 to remove death from {selected_boss}
Press 3 to select a different boss.
Press 4 to add a new boss.
Press 5 to display bosses.
Press Delete to delete {selected_boss}""")

def save_file():
    with open(filename, "w") as file: # saves the file
        json.dump(data, file)

def plus_death(event): # event_object is passed by keyboard to this function
    if selected_boss == None:
        print("Please select a boss or add a new one.")
    else:
        bosses[selected_boss] = bosses[selected_boss] + 1
        save_file()
        print(f"+1 death to {selected_boss}")

def min_death(event):
    if event.name == ('down'): # safeguard to prevent arrow keys triggering functions
        return
    
    if selected_boss == None:
        print("Please select a boss or add a new one.")

    else:
        bosses[selected_boss] = bosses[selected_boss] - 1
        save_file()
        print(f"-1 death from {selected_boss}")

def switch_boss(event):
    pass

def add_boss(event):
    if event.name == ('left'):
        return
    
    keyboard.remove_all_hotkeys()
    keyboard.send('backspace')
    new_boss = input("Please enter a boss name (press delete to cancel): ")

    if new_boss == "" or None:
        print("Boss not added.")
        listening = True
        return
    
    elif new_boss in bosses:
        print("Boss already exists.")
        listening = True
        return
    
    else:
        bosses[new_boss] = 0
        save_file()
        global selected_boss
        selected_boss = new_boss
        print(selected_boss, "added and selected.")
        listening = True
        return

def display_boss(event):
    for boss in bosses:
        print(f"{boss}{":"} {bosses[boss]} deaths.")

def delete_boss(event):
    global selected_boss
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

keyboard.on_press_key('1', plus_death)
keyboard.on_press_key('2', min_death)
keyboard.on_press_key('3', switch_boss)
keyboard.on_press_key('4', add_boss)
keyboard.on_press_key('5', display_boss)
keyboard.on_press_key('delete', delete_boss)

def exit():
    print("Saving...")
    data["saved_boss"] = selected_boss
    save_file()

atexit.register(exit) 
keyboard.wait('F12') # keeps the program running & listening