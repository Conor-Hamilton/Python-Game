import random

class Animal:
    def __init__(self, name, energy, x, y):
        self.name = name
        self.energy = energy
        self.x = x # X positioning on grid
        self.y = y # Y positioning on grid 

    def move(self):
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Up, Down, Right, Left
        dx, dy = random.choice(direction)
        self.x += dx
        self.y += dy

    def eat(self, food_energy):
        self.energy += food_energy
        print(f"{self.name} ate food and gained {food_energy} energy.")

    def __str__(self):
        return f"{self.name} is at ({self.x}, {self.y}) with {self.energy} energy."

class Herbivore(Animal):
    def graze(self):
        self.eat(5)
        print(f"{self.name} grazes on plants.")

class Rabbit(Herbivore):
    def __init__(self, x, y):
        super().__init__("Rabbit", energy=10, x=x, y=y)

class Carnivore(Animal):
    def hunt(self, prey):
        if (self.x, self.y) == (prey.x, prey.y) and prey.energy > 0:
            self.eat(prey.energy)
            print(f"{self.name} hunts and eats {prey.name}.")
            prey.energy = 0 # Prey is dead
        else:
            print(f"{self.name} failed to hunt {prey.name}.")

class Fox(Carnivore):
    def __init__(self, x, y):
        super ().__init__("Fox", energy=20, x=x, y=y)

class Wolf(Carnivore):
    def __init__(self, x, y):
        super().__init__("Wolf", energy=30, x=x, y=y)

rabbit = Rabbit(x=2, y=3)
fox = Fox(x=2,y=3)
wolf = Wolf(x=5, y=5)

rabbit.move()
fox.move()
wolf.move()


fox.hunt(rabbit)
wolf.hunt(fox)

print(rabbit)
print(fox)
print(wolf)




