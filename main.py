import random
import time

class Player:
    def __init__(self):
        self.name = ""
        self.health = 150  
        self.max_health = 150
        self.weapon = "Laser Pistol"
        self.weapon_power = 25  
        self.inventory = []
        self.total_weight = 0
        self.weight_limit = 50
    
    def examine_item(self, item):
        print(f"\nItem: {item['name']}")
        if item['name'] == 'Healing Potion':
            print("Effect: Heals 30 health points.")
        elif item['name'] == 'Energy Shield':
            print("Effect: Reduces damage from the next boss fight by 5.")
        elif item['name'] == 'Strength Booster':
            print("Effect: Increases your weapon attack power by 10.")
        elif item['name'] == 'Alien Core':
            print("Effect: Upgrades your weapon to a more powerful model.")
        elif item['name'] == 'Max HP Booster':
            print("Effect: Increases your maximum health by 20.")
        else:
            print("Effect: Unknown.")

    def upgrade_weapon(self):
        if self.weapon == "Laser Pistol":
            self.weapon = "Plasma Rifle"
            self.weapon_power = 50
            print("Your weapon has been upgraded to a Plasma Rifle!")
        elif self.weapon == "Plasma Rifle":
            self.weapon = "Quantum Blaster"
            self.weapon_power = 80
            print("Your weapon has been upgraded to a Quantum Blaster!")
        else:
            print("Your weapon is already at its maximum level.")
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
        print(f"You took {amount} damage. Current health: {self.health}")
        
    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"You healed {amount} health. Current health: {self.health}")
        
    def attack(self):
        print(f"You attack with your {self.weapon} for {self.weapon_power} damage!")
        return self.weapon_power

    def add_to_inventory(self, item):
        if self.total_weight + item['weight'] <= self.weight_limit:
            self.inventory.append(item)
            self.total_weight += item['weight']
            print(f"You added {item['name']} to your inventory.")
        else:
            print(f"Your inventory is full! You can't carry {item['name']}.")

    def use_item(self, item):
        if item['name'] == 'Healing Potion':
            self.heal(50)  
            self.inventory.remove(item)
            self.total_weight -= item['weight']
        elif item['name'] == 'Energy Shield':
            print(f"You used the {item['name']}! Your damage from the next boss fight will be reduced by 10.")
            self.inventory.remove(item)
            self.total_weight -= item['weight']
            return 'Energy Shield'
        elif item['name'] == 'Strength Booster':
            self.weapon_power += 15  
            print(f"You used the {item['name']}! Your attack power has increased by 15.")
            self.inventory.remove(item)
            self.total_weight -= item['weight']
        elif item['name'] == 'Alien Core':
            self.upgrade_weapon()
            self.inventory.remove(item)
            self.total_weight -= item['weight']
        elif item['name'] == 'Max HP Booster':
            self.max_health += 30
            self.health = self.max_health
            self.inventory.remove(item)
            self.total_weight -= item['weight']
            print(f"You used the {item['name']}! Your max health has increased by 30.")
        elif item['name'] == 'Data Chip':
            self.inventory.remove(item)
            self.total_weight -= item['weight']
            dodge_chance = random.random() 
            if dodge_chance < 0.5:  
                print(f"\nYou ate the {item['name']}! You feel a surge of energy. You have a chance to dodge the next attack!")
                return 'Data Chip'
            else:
                print(f"\nYou ate the {item['name']} but it didn't work as expected. No dodge this time.")
                return None

class Enemy:
    def __init__(self, name, health, attack, is_boss=False, voice_lines=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.is_boss = is_boss
        self.voice_lines = voice_lines if voice_lines else []

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0

    def speak(self):
        if self.voice_lines:
            print(f"\n{self.name}: {random.choice(self.voice_lines)}")

class Place:
    def __init__(self, name, description, enemies):
        self.name = name
        self.description = description
        self.enemies = enemies
        self.exploration_count = 0  

    def explore(self, player):
        if self.exploration_count < 3:
            self.exploration_count += 1
            print(f"\nYou are now in the {self.name}.")
            time.sleep(1)
            print(self.description)
            action = input(f"Do you want to explore the area or move forward? (explore/move): ").lower()
            if action == "explore":
                print(f"\nYou explore the {self.name} and find something...")
                item1 = discover_item()
                item2 = discover_item()
                print(f"You found a {item1['name']} weighing {item1['weight']} kg!")
                print(f"You found a {item2['name']} weighing {item2['weight']} kg!")
                player.add_to_inventory(item1)
                player.add_to_inventory(item2)
            elif action == "move":
                print(f"\nYou move on to the next enemy.")
            else:
                print("Invalid action.")

def discover_item():
    items = [
        {'name': 'Healing Potion', 'weight': 3},  
        {'name': 'Energy Shield', 'weight': 5},
        {'name': 'Strength Booster', 'weight': 4},
        {'name': 'Alien Core', 'weight': 6},
        {'name': 'Max HP Booster', 'weight': 3},  
        {'name': 'Plasma Grenade', 'weight': 7},
        {'name': 'Data Chip', 'weight': 5},
        {'name': 'Artifact Of Power', 'weight': 1}
    ]
    return random.choice(items)

def fight(enemy, player, shield_active):
    print(f"\nA wild {enemy.name} appears!")
    time.sleep(1)
    dodged_attack = False
    while enemy.health > 0 and player.health > 0:
        enemy.speak()

        print("\nIt's your turn! What would you like to do?")
        print("1. Attack")
        print("2. Use Item")
        action = input("Choose an action (1/2): ").strip()

        if action == "1":
            damage = player.attack()
            enemy.take_damage(damage)
            print(f"\n{enemy.name} has {enemy.health} health left.")
        elif action == "2":
            print("\nYour inventory:")
            for j, item in enumerate(player.inventory):
                print(f"{j + 1}. {item['name']}")
            item_choice = int(input("\nWhich item would you like to use? (Enter the number): ")) - 1
            if 0 <= item_choice < len(player.inventory):
                item = player.inventory[item_choice]

                examine_choice = input(f"Do you want to examine the {item['name']} before using it? (yes/no): ").lower()
                if examine_choice == "yes":
                    player.examine_item(item)

                shield_active = player.use_item(item) == 'Energy Shield'
                dodge_active = player.use_item(item) == 'Data Chip'
                if dodge_active:
                    dodged_attack = True
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")
            continue

        if enemy.health <= 0:
            print(f"You defeated the {enemy.name}!")
            return True
        
        print(f"\n{enemy.name} attacks you!")
        damage_taken = enemy.attack
        if enemy.is_boss:
            damage_taken = max(0, damage_taken - 5)  
        else:
            damage_taken = max(0, damage_taken // 2) 

        if shield_active:
            damage_taken -= 10  
            if damage_taken < 0:
                damage_taken = 0
            print("The Energy Shield absorbed some of the damage!")

        player.take_damage(damage_taken)
        if player.health <= 0:
            print("You have been defeated. Game over.")
            return False

    return False

def manage_inventory(player):
    if player.total_weight > player.weight_limit:
        print(f"\nYour inventory weight exceeds the limit ({player.total_weight}/{player.weight_limit}). You need to drop an item.")
        for i, item in enumerate(player.inventory):
            print(f"{i + 1}. {item['name']} - {item['weight']} kg")

        drop_choice = int(input("\nWhich item would you like to drop? (Enter the number): ")) - 1
        if 0 <= drop_choice < len(player.inventory):
            player.drop_item(player.inventory[drop_choice])
        else:
            print("Invalid choice.")

def intro():
    print("Welcome to universe 340392-gyyt")
    time.sleep(1)
    print("\nIn a distant future, a lost alien artifact holds the key to unimaginable power. The artifact is heavily guarded by robotic overlords and alien creatures.")
    time.sleep(2)
    print("\nYour mission: retrieve the artifact and defeat the Gaper Bingzoid to prevent the universe from falling into chaos.")
    name = input("\nEnter your name, adventurer: ")

    difficulty = input("\nChoose your difficulty level (easy/medium/hard): ").lower()
    while difficulty not in ['easy', 'medium', 'hard']:
        print("Invalid choice. Please choose from 'easy', 'medium', or 'hard'.")
        difficulty = input("\nChoose your difficulty level (easy/medium/hard): ").lower()

    player = Player()
    player.name = name
    print(f"\nHello, {name}. Your journey begins now...\n")
    return player, difficulty

def main():
    player, difficulty = intro()

    areas = [
        Place("Black Hole", "A massive, swirling black hole in the center of the galaxy.", [
            Enemy("Swirling Void", 50, 5, voice_lines=["You dare challenge me?", "I am the void... nothing can escape."]),
            Enemy("Gravity Beast", 80, 10, voice_lines=["You can't escape my pull.", "Your end is inevitable."]),
            Enemy("Satan", 200, 20, is_boss=True, voice_lines=["I am the embodiment of chaos.", "Your soul will be mine!"])
        ]),
        Place("Flat Earth", "You find yourself on a flat world, surrounded by bizarre, unexplainable phenomena.", [
            Enemy("Flat Earth Guardian", 70, 8, voice_lines=["You are not welcome here."]),
            Enemy("Cosmic Serpent", 75, 9, voice_lines=["The serpent does not forget."]),
            Enemy("Flat Earth Overlord", 180, 25, is_boss=True, voice_lines=["The world bends to my will."])
        ]),
        Place("Inside a Big Alien", "You are inside the body of a giant alien, with pulsating walls and strange organic lifeforms.", [
            Enemy("Alien Overlord", 120, 15, voice_lines=["You will never leave this place."]),
            Enemy("Bio-Terror", 100, 12, voice_lines=["My body is my weapon."]),
            Enemy("Giant Alien King", 250, 30, is_boss=True, voice_lines=["Kneel before your king!"])
        ]),
        Place("Jinkydinkyland", "A bizarre, colorful land where everything seems made out of candy and strange creatures wander.", [
            Enemy("Jinky Dinky", 60, 6, voice_lines=["I am sugar incarnate!"]),
            Enemy("Candy Horror", 90, 8, voice_lines=["This is your doom, candy hunter!"]),
            Enemy("Candy King", 220, 20, is_boss=True, voice_lines=["You cannot defeat me, mortal!"])
        ]),
        Place("Space Fortress", "A high-tech fortress, heavily guarded by robotic forces. The final challenge awaits.", [
            Enemy("Mecha Terror", 100, 15, voice_lines=["You cannot match my might!"]),
            Enemy("Cyber Warrior", 150, 20, voice_lines=["I am the future of warfare."]),
            Enemy("Gaper Bingzoid", 300, 40, is_boss=True, voice_lines=["The universe will crumble before me!"])
        ]),
    ]

    shield_active = False
    for area in areas:
        print(f"\nEntering {area.name}...\n")
        for i, enemy in enumerate(area.enemies):
            if i < 2:  
                area.explore(player)
                manage_inventory(player)

            use_item_choice = input("Do you want to use any item from your inventory? (yes/no): ").lower()
            if use_item_choice == "yes":
                print("\nYour inventory:")
                for idx, item in enumerate(player.inventory):
                    print(f"{idx + 1}. {item['name']}")
                item_choice = int(input("\nWhich item would you like to use? (Enter the number): ")) - 1
                if 0 <= item_choice < len(player.inventory):
                    item = player.inventory[item_choice]

                    examine_choice = input(f"Do you want to examine the {item['name']} before using it? (yes/no): ").lower()
                    if examine_choice == "yes":
                        player.examine_item(item)

                    shield_active = player.use_item(item) == 'Energy Shield'

            if not fight(enemy, player, shield_active):
                print("You failed your quest. It is all OVER and YOU MESSED UP")
                break

    print("\nYou have defeated Gaper Bingzoid and saved the universe!")
    if 'Artifact of Power' in [item['name'] for item in player.inventory]:
        use_artifact = input("Do you want to use the Artifact of Power to reshape the universe? (yes/no): ").lower()
        if use_artifact == "yes":
            print("\nGood Ending: You used the Artifact of Power to bring peace to the galaxy and unlock limitless possibilities!")
        else:
            print("\nBad Ending: You chose not to use the Artifact of Power. The universe remains in turmoil, and the potential for greatness is lost.")
    else:
        print("\nYou didn't find the Artifact of Power. The universe's fate is uncertain.")

if __name__ == "__main__":
    main()
