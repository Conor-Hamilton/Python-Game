import random

class Animal:
    population = []
    reproduction_energy_threshold = 15
    reproduction_energy_cost = 10
    hide_chance = 0.0 


    def __init__(self, name, energy, x, y):
        self.name = name
        self.energy = energy
        self.x = x 
        self.y = y 
        self.alive = True
        self.__class__.population.append(self)


    def move(self, max_x, max_y):
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        dx, dy = random.choice(direction)

        self.x = max(0, min(self.x + dx, max_x - 1))
        self.y = max(0, min(self.y + dy, max_y - 1))
        self.energy -= 1
        if self.energy <= 0:
            self.die()

    def eat(self, food_energy):
        self.energy += food_energy
        print(f"{self.name} ate food and gained {food_energy} energy.")

    def __str__(self):
        return f"{self.name} is at ({self.x}, {self.y}) with {self.energy} energy."

    def die(self):
        if self.alive:
            self.alive = False
            self.__class__.population.remove(self)
            print(f"{self.name} died.")

    def hide_successful(self):
        return random.random() < self.hide_chance

    def reproduce(self):
        if self.energy >= self.__class__.reproduction_energy_threshold:
            self.energy -= self.__class__.reproduction_energy_cost
            return self.__class__(self.x, self.y)
        return None
            

    def __str__(self):
        return f"{self.name} is at ({self.x}, {self.y}) with {self.energy} energy."

class Herbivore(Animal):
    def graze(self, plant):
        self.eat(plant.energy)
        print(f"{self.name} grazes on a plant.")

class Rabbit(Herbivore):
    hide_chance = 0.3
    reproduction_energy_threshold = 12
    reproduction_energy_cost = 8

    def __init__(self, x, y):
        super().__init__("Rabbit", 10, x, y)

class Carnivore(Animal):
    def hunt(self, prey):
        if not self.alive or not prey.alive:
            return
        if prey.hide_successful():
            print(f"{prey.name} got away from {self.name}!")
            return
        self.eat(prey.energy)
        print(f"{self.name} hunts and eats {prey.name}.")
        prey.die()

class Fox(Carnivore):
    hide_chance = 0.2
    reproduction_energy_threshold = 20
    preproduction_energy_cost = 12

    def __init__(self, x, y):
        super ().__init__("Fox", 20, x, y)

class Wolf(Carnivore):
    reproduction_energy_threshold = 25
    reproduction_energy_cost = 15

    def __init__(self, x, y):
        super().__init__("Wolf", 30, x, y)

class Plant:
    def __init__(self, x, y):  
        self.x = x
        self.y = y
        self.energy = 5
        self.alive = True


class World:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.animals = []
        self.plants = []
        self.generate_plants(10)

    def generate_plants(self, num_plants):
        for _ in range(num_plants):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.plants.append(Plant(x, y))

    def add_animal(self, animal):
        self.animals.append(animal)

    def simulate_step(self):
        for animal in self.animals[:]:
            if animal.alive:
                animal.move(self.width, self.height)

        for predator in self.animals[:]:
            if isinstance(predator, Carnivore) and predator.alive:
                for prey in self.animals[:]:
                    if prey is not predator and prey.alive and (predator.x, predator.y) == (prey.x, prey.y):
                        predator.hunt(prey)

        for herbivore in self.animals[:]:
            if isinstance(herbivore, Herbivore) and herbivore.alive:
                for plant in self.plants[:]:
                    if plant.alive and (herbivore.x, herbivore.y) == (plant.x, plant.y):
                        herbivore.graze(plant)
                        plant.alive = False

        new_animals = []
        for animal in self.animals[:]:
            if animal.alive:
                new_animal = animal.reproduce()
                if new_animal:
                    new_animals.append(new_animal)
        self.animals.extend(new_animals)

        if random.random() < 0.1 and len(self.plants) < 50:
            self.plants.append(Plant(random.randint(0, self.width-1), random.randint(0, self.height-1)))

        self.plants = [p for p in self.plants if p.alive]
        self.animals = [a for a in self.animals if a.alive]

        self.check_population()

    def check_population(self):
        rabbit_count = len([a for a in self.animals if isinstance(a, Rabbit)])
        if rabbit_count <= 2:
            for predator in self.animals:
                if isinstance(predator, (Fox, Wolf)):
                    predator.energy -= 3
                    print(f"{predator.name} is starving due to low rabbits!")

    def status_report(self):
        print("\n--- Status Report ---")
        print(f"Rabbits: {len(Rabbit.population)}")
        print(f"Foxes: {len(Fox.population)}")
        print(f"Wolves: {len(Wolf.population)}")
        print(f"Plants: {len(self.plants)}")


# Example Usage
world = World()
world.add_animal(Rabbit(5, 5))
world.add_animal(Rabbit(8, 8))
world.add_animal(Fox(3, 3))
world.add_animal(Wolf(10, 10))

for day in range(30):
    print(f"\nDay {day + 1}")
    world.simulate_step()
    world.status_report()


