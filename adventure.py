'''
Week 4 coding assignment: The Inventory and the Dungeon of Choices

This module simulates a simple text-based adventure game where the
character encounters monsters, finds potions, and navigates
based on user input.

Submitted by Braden Mills
'''

import random

def acquire_item(inventory, item):
    """ Adds an item to the inventory """
    inventory.append(item) # First time using a list/tuple operation (append)
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """ Displays the player's inventory """
    num = 1
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("\nYour inventory:")
        for item in inventory: # Second time using a list/tuple operation (in)
            print(f"{num}. {item}")
            num += 1

def display_player_status(player_health):
    """ Displays current health of player """
    print("Your current health:", player_health)

def handle_path_choice(player_health):
    """ Updates the player's path choice and health accordingly """
    updated_player_health = player_health
    path = random.choice(["left", "right"])
    if path == "left":
        print("\nYou encounter a friendly gnome who heals you for 10 health points.")
        player_health += 10
        player_health = min(player_health, 100)
        updated_player_health = player_health
    elif path == "right":
        print("\nYou fall into a pit and lose 15 health points.")
        player_health -= 15
        if player_health < 0:
            player_health = 0
            print("You are barely alive!")
        updated_player_health = player_health
    return updated_player_health

def player_attack(monster_health):
    """ Updates monster's health after the player attacks """
    print("You strike the monster for 15 damage!")
    updated_monster_health = monster_health - 15
    return updated_monster_health

def monster_attack(player_health):
    """ Updates player's health after the monster attacks """
    critical = random.random() < 0.5
    if critical:
        print("The monster lands a critical hit for 20 damage!")
        updated_player_health = player_health - 20
    else:
        print("The monster hits you for 10 damage!")
        updated_player_health = player_health - 10
    return updated_player_health

def combat_encounter(player_health, monster_health, has_treasure):
    """ Controls the combat between monster and player """
    treasure_found_and_won = True
    while player_health > 0 and monster_health > 0:
        monster_health = player_attack(monster_health)
        player_health = monster_attack(player_health)
        display_player_status(player_health)
    if monster_health <= 0:
        print("You defeated the monster!")
        treasure_found_and_won = has_treasure
    if player_health <= 0:
        print("Game Over!")
        treasure_found_and_won = False
    return treasure_found_and_won # boolean

def check_for_treasure(has_treasure):
    """ Checks whether the monster has treasure after being defeated """
    if has_treasure:
        print("You found the hidden treasure!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def enter_dungeon(player_health, inventory, dungeon_rooms):
    """ Determines the dungeon rooms, items, and involves user input """
    for room in dungeon_rooms: # Third time using a list/tuple operation (in)
        room_description, item, challenge_type, challenge_outcome = room
        print(room_description)
        if item:
            print(f"You found a {item} in the room.")
            inventory = acquire_item(inventory, item)
        if challenge_type == "puzzle":
            print("You encounter a puzzle!")
            choice = input("Do you want to solve or skip the puzzle? ").lower()
            if choice == "solve":
                success = random.choice([True, False])
                print(challenge_outcome[0] if success else challenge_outcome[1])
                player_health += challenge_outcome[2]

        elif challenge_type == "trap":
            print("You see a potential trap!")
            choice = input("Do you want to disarm or bypass the trap? ").lower()
            if choice == "disarm":
                success = random.choice([True, False])
                if success:
                    print(challenge_outcome[0])
                else:
                    print(challenge_outcome[1])
                    player_health += challenge_outcome[2]
        elif challenge_type == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")
        if player_health < 0:
            player_health = 0
            print("You are barely alive!")
        display_inventory(inventory)
    print("You have explored all of the dungeon.")
    display_player_status(player_health)
    return player_health, inventory

def main():
    """ Main function """
    player_health = 100
    monster_health = 70 # Example hardcoded value
    has_treasure = False
    inventory = [] # Empty list to store values in the future

    dungeon_rooms = [
        ("A dusty old library", "key", "puzzle",
        ("You solved the puzzle!", "The puzzle remains unsolved.", -5)),
        ("A narrow passage with a creaky floor", None, "trap",
        ("You skillfully avoid the trap!", "You triggered a trap!", -10)),
        ("A grand hall with a shimmering pool", "healing potion", "none", None),
        ("A small room with a locked chest", "treasure", "puzzle",
        ("You cracked the code!", "The chest remains stubbornly locked.", -5))
    ]

    has_treasure = random.choice([True, False]) # Randomly assign treasure

    player_health = handle_path_choice(player_health)

    treasure_obtained_in_combat = combat_encounter(player_health, monster_health, has_treasure)

    check_for_treasure(treasure_obtained_in_combat) # Or has_treasure, depending on logic

    if player_health > 0:
        print("\nYou stumble into a dungeon.")
        player_health, inventory = enter_dungeon(player_health, inventory, dungeon_rooms)

if __name__ == "__main__":
    main()
