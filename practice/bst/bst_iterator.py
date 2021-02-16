class BSTIterator:
    # @param root, a binary search tree's root node
    def __init__(self, root):
        self.root = root
        self.stack = []
        
        cnode = root
        while cnode is not None:
            self.stack.append(cnode)
            cnode = cnode.left
    
    # @return a boolean, whether we have a next smallest number
    def hasNext(self):
        return len(self.stack) > 0        

    # @return an integer, the next smallest number
    def next(self):
        cnode = self.stack[-1]
        del self.stack[-1]

        if cnode.right is not None:
            tnode = cnode.right
            self.stack.append(tnode)
            while tnode.left is not None:
                self.stack.append(tnode.left)
                tnode = tnode.left

        return cnode.val


def test():
    from bst import Tree

    x = [10, 33, 1, 5, 65, 3, 25, 167, 34, 6 , 15, 28]
    bst = Tree(x[0])
    for val in x[1:]:
        bst.insert(bst.root, val)
    
    i = BSTIterator(bst.root)
    while i.hasNext():
        print(i.next())
    
if __name__ == '__main__':
    test()