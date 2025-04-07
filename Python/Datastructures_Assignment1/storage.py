
class Node:
    def __init__(self, data):
        """ Store the data, and set next to None"""
        self.data = data
        self.next = None

    def __str__(self):
        """ Return a string representation of the data """
        return f"{self.data}"


class Storage:
    def __init__(self):
        """ Creates an empty Storage class. Sets head to None. """
        self.head = None

    def push(self, data):
        """ Create a Node to hold the data, then put it at the head of the list. """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        """ Remove the head Node and return its data. """
        if self.isempty():
            return None
        else:
            head_node = self.head
            self.head = self.head.next
            return head_node.data

    def peek(self):
        """ Return the data from the head Node, without removing it. """
        if self.isempty():
            return None
        else:
            return self.head.data

    def isempty(self) -> bool:
        """ Return True if the list is empty, otherwise False """
        return self.head is None
