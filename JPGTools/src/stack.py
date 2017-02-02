#class for defining a stack
class Stack:
    def __init__(self, limit):
        self.items = []
        self.limit = limit
         
    #method for pushing an item on a stack
    def push(self,item):
        if item in self.items: self.items.remove(item)
        self.items.append(item)
        if len(self.items) > self.limit: self.items.pop(0)
         
    #method for popping an item from a stack
    def pop(self):
        return self.items.pop()
     
    #method to check whether the stack is empty or not
    def isEmpty(self):
        return (self.items == [])
     
    #method to get the top of the stack
    def topOfStack(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)
    