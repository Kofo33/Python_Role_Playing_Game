import random
import time

class Character:
    def __init__(self, name, health, attack_power, defense):
        self.name = name
        self.max_health = health #so healing doesn't go above this
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 10

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        damage_taken = max(1, damage - self.defense)
        self.health = max(0, self.health - damage_taken)
        print(f"{self.name} takes {damage_taken} damage. {self.name}'s health left: {self.health}")

    def attack(self, target):
        damage = random.randint(self.attack_power - 2, self.attack_power + 5)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

    def heal(self, amount):
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        print(f"{self.name} heals for {self.health - old_health} HP. {self.name}'s health is now {self.health}.")

    def gain_experience(self, xp):
        self.experience += xp
        print(f"{self.name} gained {xp} XP.")
        self.check_level_up()

    def check_level_up(self):
        while self.experience >= self.experience_to_next_level:
            self.level += 1
            self.experience_to_next_level = int(self.experience_to_next_level * 1.5)  # Increase difficulty for next level
            self.attack_power += 2
            self.defense += 1
            self.max_health += 5
            self.health = self.max_health
            print(f"{self.name} leveled up to Level {self.level}!")


class Player(Character):
    def __init__(self, name, health, attack_power, defense):
        super().__init__(name, health, attack_power, defense)
        self.defending = False
        self.inventory = {"Health Potion": 2}
        self.starting_hp = health  # Keep track of starting HP per level

    def choose_action(self, enemies):
        print("\nChoose an action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Heal")
        print("4. Check Status")
        print("5. Use Item")
        print("6. Exit")
        choice = input("\n> ")

        if choice == "1":
            target = enemies[0] 
            self.attack(target)
            self.defending = False

        elif choice == "2":
            self.defending = True
            print(f"{self.name} is defending and will take reduced damage next turn.")

        elif choice == "3":
            self.heal(5)
            self.defending = False

        elif choice == "4":
            self.show_status()

        elif choice == "5":
            self.use_item()

        elif choice == "6":
            print("Exiting the game.")
            exit()

    def gain_experience(self, xp):
        self.experience += xp
        print(f"{self.name} gained {xp} XP.")
        self.check_level_up()

    def check_level_up(self):
        levels_gained = 0
        total_hp_increase = 0

        while self.experience >= self.experience_to_next_level:
            self.level += 1
            self.attack_power += 2
            self.defense += 1

            hp_increments = {2: 10, 3: 12, 4: 12, 5: 15}
            increment = hp_increments.get(self.level, 20)
            self.starting_hp += increment
            total_hp_increase += increment

            self.max_health = self.starting_hp
            self.health = self.max_health
            levels_gained += 1

        if levels_gained > 0:
            print(f"{self.name} leveled up {levels_gained} time(s)! HP increased by {total_hp_increase} to {self.max_health}.")


    def show_status(self):
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Defense: {self.defense}")
        print(f"Experience: {self.experience}/{self.experience_to_next_level}")
        print(f"Inventory: {self.inventory}")

    def use_item(self):
        if not self.inventory:
            print("You inventory is empty.")
            return
        print("Choose an item to use:")
        for i, (item, quantity) in enumerate(self.inventory.items(), start=1):
            print(f"{i}. {item} (x{quantity})")
        choice = input("> ")
        try:
            choice = int(choice) - 1
            item_name = list(self.inventory.keys())[choice]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return
        if item_name == "Health Potion":
            if self.health < self.max_health:
                self.heal(30)
                self.inventory[item_name] -= 1
                if self.inventory[item_name] <= 0:
                    del self.inventory[item_name]
            else:
                print("You are already at full health.")


class Enemy(Character):
    def take_turn(self, player):
        if not self.is_alive():
            return
        
        # Small pause for turn pacing
        time.sleep(1)

        action = random.choice(["attack", "heal", "attack", "defend"])

        if action == "attack":
            print(f"{self.name} prepares to strike!")
            time.sleep(0.5)
            if player.defending:
                reduced_damage = max(0, self.attack_power - player.defense * 2)
                print(f"{self.name} attacks {player.name}, but damage is reduced due to defense!")
                player.take_damage(reduced_damage)
            else:
                self.attack(player)

        elif action == "heal":
            heal_amount = random.randint(3, 6)
            print(f"{self.name} uses a turn to heal for {heal_amount} HP.")
            self.heal(heal_amount)

        elif action == "defend":
            print(f"{self.name} braces for impact and will take less damage next turn.")
            self.defense += 2

        # Reset player's defense after enemy finishes turn
        player.defending = False


class Game:
    def __init__(self):
        self.player = Player("Hero", 30, 8, 3)
        self.level_count = 1

         # Enemy names by level range
        self.enemy_names = {
            1: "Goblin",
            2: "Orc",
            3: "Troll",
            4: "Dark Knight",
            5: "Dragon"
        }

    def next_enemy(self):
        #Scale enemy stats based on level_count
        enemy_name = self.enemy_names.get(self.level_count, "Goblin")
        health = 20 + self.level_count * 5
        attack = 6 + self.level_count
        defense = 2 + self.level_count // 2
        enemy = Enemy(f"{enemy_name} Lv. {self.level_count}", health, attack, defense)
        enemy.level = self.level_count
        return enemy


    def play(self):
        while self.player.is_alive():
            if self.level_count > 5:
                print("\nCongratulations! You completed all levels!")
                break
            self.enemies = [self.next_enemy()]
            print(f"\n===== LEVEL {self.level_count} =====")
            print(f"A wild {self.enemies[0].name} appears!\n")

        # Print player and enemy stats before the battle starts
            print("Player Stats:")
            print(f'''Name: {self.player.name}
Health: {self.player.health} 
Attack: {self.player.attack_power} 
Defense: {self.player.defense} 
Level: {self.player.level} 
XP: {self.player.experience}''')

            print("\nEnemy Stats:")
            for enemy in self.enemies:
                print(f'''Name: {enemy.name}
Health: {enemy.health}
Attack: {enemy.attack_power}
Defense: {enemy.defense}
Level: {enemy.level}
XP: {enemy.experience}''')
            time.sleep(1.5)

            print("\n=========== Battle Start! ============")

            # Battle loop
            while self.player.is_alive() and any(e.is_alive() for e in self.enemies):
                print("\n========= PLAYER TURN ==========")
                self.player.choose_action(self.enemies)

                time.sleep(1.5)

                if any(e.is_alive() for e in self.enemies):
                    print("\n=========== ENEMY TURN ===========")
                    for enemy in self.enemies:
                        if enemy.is_alive():
                            enemy.take_turn(self.player)
                            time.sleep(1)

            if self.player.is_alive():
                print("You win!")
                self.player.gain_experience(10 + self.level_count * 5)
                self.player.heal(5)  # Heal a bit after winning

                self.level_count += 1  # increment level once

                print("\nNext level starting soon...\n")
                time.sleep(3)  # 3 seconds pause

            else:
                print("You lost!")
                break

            time.sleep(1)


if __name__ == "__main__":
    game = Game()
    game.play()