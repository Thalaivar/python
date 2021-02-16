from typing import List


class Node:
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Tree:
    def __init__(self, root_val) -> None:
        self.root = Node(root_val)
        self.height = 0
    
    def insert(self, cnode, val) -> Node:
        if cnode.left is None and cnode.right is None:
            self.height += 1
            if val < cnode.val:
                cnode.left = Node(val)
            else:
                cnode.right = Node(val)
            
            return cnode

        if val < cnode.val:
            if cnode.left is None:
                cnode.left = Node(val)
                return cnode
            else:
                return self.insert(cnode.left, val)
        else:
            if cnode.right is None:
                cnode.right = Node(val)
                return cnode
            else:
                return self.insert(cnode.right, val)
    
    def traverse(self, node: Node, kind='io') -> list:
        if node is None:
            return []
        
        if kind is 'io':    
            return self.traverse(node.left, kind) + [node.val] + self.traverse(node.right, kind)
        elif kind is 'pr':
            return [node.val] + self.traverse(node.left, kind) + self.traverse(node.right, kind)
        elif kind is 'po':
            return  self.traverse(node.left, kind) + self.traverse(node.right, kind) + [node.val]
    
def from_list(l: list) -> Tree:
    bst = Tree(l[0])
    
    for x in l[1:]:
        bst.insert(bst.root, x)
    
    return bst


def traversal_test(x: list):
    bst = Tree(x[0])

    for val in x[1:]:
        bst.insert(bst.root, val)
    
    print(bst.traverse(bst.root, kind='io'))
    print(bst.traverse(bst.root, kind='pr'))
    print(bst.traverse(bst.root, kind='po'))

if __name__ == '__main__':
    x = [10, 33, 1, 5, 65, 3, 25, 167, 34, 6 , 15, 28]
    traversal_test(x)
        
