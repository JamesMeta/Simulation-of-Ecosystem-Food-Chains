class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    pass

class Cat(Animal):
    pass
dog = Dog()
dog.speak()  # Output: Dog barks

cat = Cat()
cat.speak()  # Output: Cat meows
