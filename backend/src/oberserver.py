class Observer:
    def update(self, message):
        raise NotImplementedError("You must implement the update method.")

class Subject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

# Example usage
class ConcreteObserver(Observer):
    def update(self, message):
        print(f"Received message: {message}")

# Creating subject and observers
subject = Subject()

observer1 = ConcreteObserver()
observer2 = ConcreteObserver()

# Registering observers
subject.register_observer(observer1)
subject.register_observer(observer2)

# Notify observers
subject.notify_observers("Hello Observers!")
