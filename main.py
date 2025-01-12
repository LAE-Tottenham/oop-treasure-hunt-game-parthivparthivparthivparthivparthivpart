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
        if item not in self.inventory: 
            print(f"{item['name']} is not in your inventory.")
            return None  
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
        return None

class Enemy:
    def __init__(self, name, health, attack, is_boss=False, voice_lines=None, key_item=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.is_boss = is_boss
        self.voice_lines = voice_lines if voice_lines else []
        self.key_item = key_item

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
        {'name': 'Artifact Of Power', 'weight': 1},
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
            if enemy.is_boss:
                if enemy.name == "Kanye West" and random.random() < 0.2: 
                    rare_item = "Carti's Album"
                    print(f"\nWow! Kanye West dropped a rare item: {rare_item}!")
                    player.add_to_inventory({'name': rare_item, 'weight': 1})
                
                    print("You feel the power of Carti's Album guiding you to a mysterious place...")
                    return "Carti's House"
                elif enemy.key_item:
                    print(f"You obtained the {enemy.key_item}!")
                    player.add_to_inventory({'name': enemy.key_item, 'weight': 1})
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

def post_boss_prompt(player, key_item_name, area):
    while True:
        print(f"\nYou have the {key_item_name}. What would you like to do?")
        print("1. Use the key to proceed to the next area.")
        print("2. Explore the current area one more time.")
        choice = input("Choose an action (1/2): ").strip()

        if choice == "1":
            print(f"You used the {key_item_name} to unlock the path to the next area.")
            return True  
        elif choice == "2":
            print(f"You decide to explore the {area.name} one more time.")
            area.explore(player)  
            manage_inventory(player)
        else:
            print("Invalid choice. Please try again.")

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
            Enemy("Satan", 200, 20, is_boss=True, voice_lines=["I am the embodiment of chaos.", "Your soul will be mine!"], key_item="Black Hole Core")
        ]),
        Place("The zongle centre", "After besting Satan, the black hole gets stronger, and in the process, it eats you, transporting you to a void inside if every black hole, the zongle centre", [
            Enemy("Dongles", 60, 7, voice_lines=["My dongle is all i nongle to tongle the longle", "All I nongle is just ONE dongle to kill your plongle"]),
            Enemy("Zonglite crystallians", 65, 8, voice_lines=[f"Do not come any closer {player.name}, the zongle centre is too strong for you", "These crystals of mine aren't their to look pretty"]),
            Enemy("The zongle centroid", 250, 15, is_boss=True, voice_lines=["vrmmmmnmnmm", "weeeaeeweeeweaa", "wowowowowowowo"], key_item="The zongle's dongle")
        ]),
        Place("quantum space", "You broke the zongle centroid, getting rid of every black hole in existence, but this imploded and in turn, made you so small you have transported to a miniature universe inside ours", [
            Enemy("Underling of this one guy", 80, 5, voice_lines=["You'll never guess who my boss is", "Anything for my boss!!!!"]),
            Enemy("Right-hand man of this one guy", 100, 5, voice_lines=["You have probably seen my boss before", "Yeah my boss had a tiny black-hole in his robots, and one did the same to him as it did to you"]),
            Enemy("Elon Musk", 300, 12, is_boss=True, voice_lines=["I hope nobody has bought X from me", "I really need to stare at my Donald Trump photo", "Don't make fun of me or I will ban you on X"], key_item="Twitter")
        ]),
        Place("Flat Earth", "You find yourself on a flat world, surrounded by bizarre, unexplainable phenomena, after touching a device elon had named 'Do not touch' .", [
            Enemy("Flat Earth Guardian", 70, 8, voice_lines=["You are not welcome here."]),
            Enemy("Cosmic Serpent", 75, 9, voice_lines=["The serpent does not forget."]),
            Enemy("Flat Earth Overlord", 180, 25, is_boss=True, voice_lines=["The world bends to my will."], key_item="Flat Earth undoing")
        ]),
        Place("Elon's big tesla spaceship he made in secret", "Yeah he made a big spaceship to kill anyone that kills him", [
            Enemy("Tesla bot 1", 90, 10, voice_lines=["Why did you kill him", "Going on auto-drive (And I won't drive into anyone by mistake)", "Making new useless features a car never needed now. . ."]),
            Enemy("SpaceX new CEO", 95, 11, voice_lines=["My life could've been easy but I was forced to become CEO", "Why kill Elon, now everything is messed up"]),
            Enemy("spaceship autopilot", 200, 30, is_boss=True, voice_lines=["EVIL autopilot activated", "EVIL spotify premium activated", "Nobody can make me new features WHY did YOU kill ELon"], key_item="Spaceship driver key")
        ]),
        Place("Inside a Big Alien", "You are inside the body of a giant alien, with pulsating walls and strange organic lifeforms. A big alien ate you and the spaceship", [
            Enemy("Alien Overlord", 120, 15, voice_lines=["You will never leave this place."]),
            Enemy("Bio-Terror", 100, 12, voice_lines=["My body is my weapon."]),
            Enemy("Giant Alien King", 250, 30, is_boss=True, voice_lines=["Kneel before your king!"], key_item="Big alien brain")
        ]),
        Place("Jinkydinkyland", "A bizarre, colorful land where everything seems made out of candy and strange creatures wander. This was all vomited out by the big alien", [
            Enemy("Jinky Dinky", 100, 16, voice_lines=["I am sugar incarnate!"]),
            Enemy("Candy Horror", 145, 10, voice_lines=["This is your doom, candy hunter!"]),
            Enemy("Jinky Minus", 300, 20, is_boss=True, voice_lines=["You cannot defeat me, mortal!"], key_item="Jinky's dinky")
        ]),
        Place("Earth", "Back to home, but every building and monument destroyed after Elon Musk's death, as he coded this to happen", [
            Enemy("Rishi Sunak", 150, 10, voice_lines=["Elon Musk was my best friend... ", "How will I get money from dogecoin now"]),
            Enemy("Xi jinping", 200, 15, voice_lines=["购买我版的特斯拉机器人", "请解禁抖音", "请给我你所有的数据"]),
            Enemy("Donald Trump", 250, 30, is_boss=True, voice_lines=["Vote me as president 5 more times please", "Elon Musk was like a brother to me", "We are America"], key_item="Presidency")
        ]),
        Place("Musical stage of DOOM", "After beating a few world leaders, Gaper bingzoid has come and taken over earth, making singers and rappers the new leaders", [
            Enemy("Playboi Carti", 200, 10, voice_lines=["I will NEVER drop music again", "Everything here will be ALL RED,"]),
            Enemy("Elvis Presley", 250, 10, voice_lines=["Where am I", "WHy am I alive again", "Please kill me again"]),
            Enemy("Kanye West", 300, 30, is_boss=True, voice_lines=["Bully WILL be Album of the year", "I am making vultures 3 and 4 next year", "I need me some more nitrous"], key_item="Vultures 3")
        ]),
        Place("Space Fortress", "A high-tech fortress, heavily guarded by robotic forces. The final challenge awaits.", [
            Enemy("Mecha Terror", 250, 15, voice_lines=["You cannot match my might!"]),
            Enemy("Cyber Warrior", 250, 20, voice_lines=["I am the future of warfare."]),
            Enemy("Gaper Bingzoid", 400, 20, is_boss=True, voice_lines=["The universe will crumble before me!"])
        ]),
        Place("Carti's House", "You listened to carti's album, and you got transported to Carti's house, where he wishes to confront you", [
            Enemy("Carti's Security", 150, 15, voice_lines=["Nobody sees Carti without my approval!", "You don't belong here."]),
            Enemy("Carti's Muse", 200, 20, voice_lines=["Carti's art will destroy you.", "You can't handle this energy."]),
            Enemy("Playboi Carti", 400, 25, is_boss=True, voice_lines=["God has given me a second chance", "GIVE MY ALBUM BACK NOBODY CAN TAKE IT"], key_item="Carti's Legacy")
        ])
    ]

    shield_active = False
    for area in areas:
        if area.enemies[0].is_boss:
            required_key = area.enemies[0].key_item
            if required_key and required_key not in [item['name'] for item in player.inventory]:
                print(f"You need the {required_key} to enter this area!")
                break
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
            if enemy.key_item:
                if not post_boss_prompt(player, enemy.key_item, area):
                    break

    print("\nYou have defeated Gaper Bingzoid and saved the universe!")
    if "Carti's Legacy" in [item['name'] for item in player.inventory]:
        use_carti_legacy = input("Do you want to read the legacy that Carti has left behind? (yes/no): ").lower()
        if use_carti_legacy == "yes":
            print("\nCarti Ending: You read his legacy, inspiring you to start creating music like him, thus becoming the next Playboi Carti, and now becoming the best musician in the new age")
        else:
            if 'Artifact of Power' in [item['name'] for item in player.inventory]:
                use_artifact = input("Do you want to use the Artifact of Power to reshape the universe? (yes/no): ").lower()
                if use_artifact == "yes":
                    print("\nGood Ending: You used the Artifact of Power to bring peace to the galaxy and unlock limitless possibilities!")
                else:
                    print("\nBad Ending: You chose not to use the Artifact of Power. The universe remains in turmoil, and the potential for greatness is lost.")            
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
