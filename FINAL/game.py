#!/usr/bin/python3

from map import rooms
from player import *
from items import *
from text_parser import *
from enemies import *

import random
random.seed()


def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:

    >>> list_of_items([item_pen, item_handbook])
    'a pen, a student handbook'

    >>> list_of_items([item_id])
    'id card'

    >>> list_of_items([])
    ''

    >>> list_of_items([item_money, item_handbook, item_laptop])
    'money, a student handbook, laptop'

    """

    return_string = ""
    
    for part in items:
        return_string = return_string + part["name"] + ", "

    return_string = return_string[:len(return_string)-2]

    return return_string


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:

    >>> print_room_items(rooms["Reception"])
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room_items(rooms["Office"])
    There is a pen here.
    <BLANKLINE>

    >>> print_room_items(rooms["Robs"])

    (no output)

    Note: <BLANKLINE> here means that doctest should expect a blank line.

    """
    if room["items"] != []: 
        print("There is " + list_of_items(room["items"]) + " here.")
        print("")


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:

    >>> print_inventory_items(inventory)
    You have id card, laptop, money.
    <BLANKLINE>

    """

    if len(items) > 0:
        print("You have " + list_of_items(items) + ".")
        print("")


def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:

    >>> print_room(rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>

    >>> print_room(rooms["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room(rooms["Robs"])
    <BLANKLINE>
    ROBS' ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Rob Evans and Rob Davies. They
    ignore you. To the north is the reception.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    # Display room name
    print()
    print(room["name"].upper())
    print()
    # Display room description
    print(room["description"])
    print()
    # Display room items
    print_room_items(room)


def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:

    >>> exit_leads_to(rooms["Reception"]["exits"], "south")
    "Robs' room"
    >>> exit_leads_to(rooms["Reception"]["exits"], "east")
    "your personal tutor's office"
    >>> exit_leads_to(rooms["Tutor"]["exits"], "west")
    'Reception'
    """
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
    >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
    >>> print_exit("south", "Robs' room")
    GO SOUTH to Robs' room.
    """
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items, room_enemies):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."

    For example, the menu of actions available at the Reception may look like this:

    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to Robs' room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?

    """
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    # Iterate over room items
    for part in room_items:
        print("TAKE " + str(part["id"]).upper() + " to take " + part["name"] + ".")

    # Iterate over inventory items
    for part in inv_items:
        print("DROP " + str(part["id"]).upper() + " to drop " + part["name"] + ".")

    #Iterate over room enemies.
    for part in room_enemies:
        print("ATTACK " + str(part["id"]).upper() + " to attack the " + part["name"] + ".")
    
    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

    >>> is_valid_exit(rooms["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(rooms["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room
    if is_valid_exit(current_room["exits"], direction) and len(current_room["enemies"]) == 0:
        print("Moving to " + exit_leads_to(current_room["exits"], direction) + "...")
        current_room = move(current_room["exits"], direction) 
    elif len(current_room["enemies"]) != 0:
        print("You cannot move when there are enemies nearby!")
    else:
        print("You cannot go there.")


def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """

    global current_room
    global inventory
    item_found = False
    for item in current_room["items"]:
        if item_id == item["id"]:
            item_found = True
            if len(inventory) < 3:
                inventory.append(item)
                current_room["items"].remove(item)
                print("You take " + item["name"] + ".")
                break
            else:
                print("You can only carry up to 3 items at a time.")
                break

    if item_found:
        return True
    else:
        print("You cannot take that.")
        return False
    

def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """

    global current_room
    global inventory
    item_found = False
    for item in inventory:
        if item_id == item["id"]:
            item_found = True
            current_room["items"].append(item)
            inventory.remove(item)
            print("You drop " + item["name"] + ".")
            break

    if item_found:
        return True
    else:
        print("You cannot drop that.")
        return False


def execute_examine(item_id):
    """This function is used to display the description of the item or enemy 
    specified by item_id. If the item does not exist in the player's inventory,
    or the enemy specified then this is not present in the room, this function
    prints "You cannot examine that.".
    """

    global current_room
    global inventory
    item_found = False
    for item in inventory:
        if item_id == item["id"]:
            item_found = True
            current_room["items"].append(item)
            inventory.remove(item)
            print("You drop " + item["name"] + ".")
            break

    if item_found:
        return True
    else:
        print("You cannot drop that.")
        return False


def execute_swap(item1_id, item2_id):
    """This function is used to swap an item from the player's inventory
    with an item in the current room. It uses the previously defined 
    execute_drop and execute_take to do this. This function will print
    "Swap succeeded." if the function is carried out correctly, or "Swap
    failed." if the function fails.
    """

    if execute_drop(item2_id):
        if execute_take(item1_id):
            print("Swap succeeded.")
        else:
            print("Swap failed. Second item was dropped.")
    else:
        print("Swap failed. No change made.")


def execute_help():
    """This function is used to print a list of available commands based
    on the help.txt file. 
    """

    file_help = open("help.txt", "r")
    for line in file_help:
        print(line)
    file_help.close()


def execute_save():
    """This function is used to store the player's progress in the game
    in a text file called "save.txt". This will allow the player to load 
    their progress and return to the point they saved at, even if they 
    close the game between saving and loading.
    """

    # Calls all releveant pieces of data as globals.
    global current_room
    global rooms
    global inventory
    global health

    # Initialises an error flag.
    error = False
    
    # Opens the file for writing.
    file_save = open("save.txt", "w")

    # Begins writing to the file.

    # Writes the ids of all of the items and the room they are in.
    file_save.write("##Room Items\n")
    for room in rooms:
        if len(rooms[room]["items"]) > 0:
            file_save.write("#" + room + "\n")
            for item in rooms[room]["items"]:
                file_save.write(item["id"] + "\n")

    # Writes the ids of all of the items and the room they are in.
    file_save.write("##Room Enemies\n")
    for room in rooms:
        if len(rooms[room]["enemies"]) > 0:
            file_save.write("#" + room + "\n")
            for enemy in rooms[room]["enemies"]:
                file_save.write(enemy["id"] + "\n")
                file_save.write(enemy["health"] + "\n")

    # Writes the ids of all of the items in the player's inventory.
    file_save.write("##Inventory Items\n")
    if len(inventory) > 0:
        for item in inventory: 
            file_save.write(str(item["id"]) + "\n")

    # Writes the id of the room the player is currently in.
    file_save.write("##Current Room\n")   
    file_save.write(str(current_room["id"]) + "\n")

    # Writes the player's health to the file.
    file_save.write("##Current Health\n")   
    file_save.write(str(current_room["id"]) + "\n")

    # Closes the file.
    file_save.close()

    # Returns a response depending on the status of the error flag.
    if error == False:
        print("Save successful!")
    else:
        print("There was an error while saving. It is recommended")
        print("to not load from this file. Please try saving again.")


def execute_load():
    """This function is used to load the player in at the point in the 
    game they last saved at. The function does this by opening the file
    "save.txt" and placing the data from the file into the appropriate
    data structures.
    """

    # Calls all releveant pieces of data as globals.
    global current_room
    global rooms
    global inventory
    global items

    # Initialises an error flag.
    error = False

    # Initialises lists/strings for storing data from file.
    data_list = []
    data_rooms = {}
    data_items = []
    data_enemies = []
    data_inventory = []
    data_current_room = ""
    data_health = ""
    data_room_selected = ""

    # Initialises variable for tracking data processing stage.
    data_stage = 0

    # Opens the file for reading.
    file_load = open("save.txt", "r")

    # Loads data from file into the storage list.
    for string in file_load:
        data_list.append(string[:len(string)-1])

    # Closes the file.
    file_load.close()

    # Splits main list up into 3 smaller lists/strings, by checking
    # for "##" markers, which separate the sections of the file.
    for data in data_list:
        if data[0:2] == "##":
            data_stage += 1
        else:
            if data_stage == 1:
                data_items.append(data)
            elif data_stage == 2:
                data_inventory.append(data)
            elif data_stage == 3:
                data_current_room = data
                break

    # Clears out old data from the room dictionary.
    for room in rooms:
        rooms[room]["items"] = []

    # Adds items in data_rooms to their locations in the game.    
    for data in data_rooms:
        if data[0:1] == "#":
            data_room_selected = data[1:]
            print(data_room_selected)
        else:
            rooms[data_room_selected]["items"].append(items[data])

    # Adds items in data_inventory to the player's inventory.
    inventory = []
    for data in data_inventory:
        inventory.append(items[data])

    # Sets the player's location to the one stored in data_current_room.
    current_room = rooms[data_current_room]

    # Returns a response depending on the status of the error flag.
    if error == False:
        print("Load successful!")
    else:
        print("There was an error while loading. It is recommended")
        print("to not save from this point onward. Enjoy the errors")
        print("this issue may create.")


def execute_attack(enemy_id):
    """This function is used to attack an enemy in the same room as the
    player. It deals a random amout of damage between 0 and 8 (inclusive), 
    and has a small chance of dealing 3 times that damage as a 'critical
    hit'. This function will also print the amount of damage done to the 
    enemy.
    """

    global current_room
    enemy_found = False
    for enemy in current_room["enemies"]:
        if enemy_id == enemy["id"]:
            enemy_found = True
            damage = randint(0,6)
            critical = randint(0,20)
            if critical >= 18:
                print("Critical hit! Damage x 3!")
                damage = damage * 3
            print("You deal " + str(damage) + " damage to the " + enemy["id"])
            enemy["health"] = str(val(enemy["health"]) - damage)
            break

    if item_found:
        return True
    else:
        print("You cannot attack that.")
        return False


def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes the appropriate function
    for that action, supplying the second word as the argument.
    """
    if command != []:
        # "Go" command handler
        if command[0] == "go" or command[0] == "move":
            if len(command) > 1:
                execute_go(command[1])
            else:
                print("Go where?")

        # "Take" command handler
        elif command[0] == "take":
            if len(command) > 1:
                execute_take(command[1])
            else:
                print("Take what?")

        # "Drop" command handler
        elif command[0] == "drop":
            if len(command) > 1:
                execute_drop(command[1])
            else:
                print("Drop what?")

        # "Examine" command handler
        elif command[0] == "examine":
            if len(command) > 1:
                execute_examine(command[1])
            else:
                print("Examine what?")

        # "Swap" command handler
        elif command[0] == "swap":
            if len(command) > 2:
                execute_swap(command[1], command[2])
            else:
                print("Examine what?")

        # "Help" command handler
        elif command[0] == "help":
            execute_help()
            pass

        # "Save" command handler
        elif command[0] == "save":
            response = input("Are you sure you want to save? Type 'Y' to save.  > ")
            if response == "Y":
                execute_save()

        # "Load" command handler
        elif command[0] == "load":
            response = input("Are you sure you want to load? Type 'Y' to load.  > ")
            if response == "Y":
                execute_load()

        # "Attack" command handler
        elif command[0] == "attack":
            if len(command) > 1:
                execute_attack(command[1])
            else:
                print("Attack what?")

        # "Quit" command handler
        elif command[0] == "quit":
            response = input("Are you sure you want to quit? Type 'Y' to quit.  > ")
            if response == "Y":
                print("Thanks for playing!")
                quit()

        # No command handler
        else:
            print("I don't know how to " + command[0])
    else:
        print("Invalid command.")


def run_check_victory(room):
    """This function will check if the player has fulfilled the conditions
    to beat the game. It returns either True of False depending on if the
    conditions have been met or not.
    """

    if len(room["items"]) > 5 and room == rooms["Reception"]:
        return True


def run_check_death_player():
    """This function will check if the player has run out of health and
    has failed to complete the game. It returns True if the player is
    on zero health, or False otherwise.
    """

    global health
    if health <= 0:
        return True


def run_check_death_enemy(enemy):
    """This function will check if an enemy has run out of health and
    will remove the enemy from the room. It returns True if the enemy is
    on zero health, or False otherwise.
    """

    if enemy["health"] <= 0:
        return True


def run_checks(room):
    """This function is used to check to see if the player has fulfilled the
    conditions for any events to be activated, such as beating the game,
    giving an item to a person, etc. This function runs every time the game 
    loop runs.
    """

    # Runs the "Game Victory" check.
    if run_check_victory(room):
        print("=================================================")
        print("VICTORY")
        print("")
        print("Congratulations! You have defeated the evil items")
        print("by sealing them away in the Reception. The Queen's")
        print("Buildings are safe once again!")
        print("")
        print("Thanks for playing!")
        print("=================================================")
        quit()

    # Runs the "Player Death" check.
    if run_check_death_player():
        print("=================================================")
        print("DEFEAT")
        print("")
        print("You have died.")
        print("")
        print("Thanks for playing!")
        print("=================================================")
        quit()

    # Runs the "Enemy Death" check.
    for enemy in current_room["enemies"]:
        if run_check_death_enemy(enemy):
            print("The " + enemy["name"] + " was defeated!")
            current_room["enemies"].remove(enemy)


def menu(exits, room_items, inv_items, room_enemies):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.
    """

    # Display menu
    print_menu(exits, room_items, inv_items, room_enemies)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:

    >>> move(rooms["Reception"]["exits"], "south") == rooms["Robs"]
    True
    >>> move(rooms["Reception"]["exits"], "east") == rooms["Tutor"]
    True
    >>> move(rooms["Reception"]["exits"], "west") == rooms["Office"]
    False
    """

    # Next room to go to
    return rooms[exits[direction]]


def main():

    # Main game loop
    while True:
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory, current_room["enemies"])

        # Execute the player's command
        execute_command(command)

        # Checks to see if conditions for in game events are met
        run_checks(current_room)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

