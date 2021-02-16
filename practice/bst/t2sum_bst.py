class bst_iterator:
    def __init__(self, root, reverse=False):
        self.stack = []
        self.reverse = reverse

        cnode = root
        while cnode is not None:
            self.stack.append(cnode)
            cnode = self.get_next_node(cnode)
    
    def get_next_node(self, cnode):
        if self.reverse:
            return cnode.right
        else:
            return cnode.left

    def get_other_node(self, cnode):
        if not self.reverse:
            return cnode.right
        else:
            return cnode.left

    def has_next(self):
        return len(self.stack) > 0
    
    def next(self):
        cnode = self.stack[-1]
        del self.stack[-1]

        if self.get_other_node(cnode) is not None:
            tnode = self.get_other_node(cnode)
            while tnode is not None:
                self.stack.append(tnode)
                tnode = self.get_next_node(tnode)

        return cnode.val

class Solution:
    # @param A : root node of tree
    # @param B : integer
    # @return an integer
    def t2Sum(self, A, B):
        if A is None:
            return 0

        fw_it, rv_it = bst_iterator(A), bst_iterator(A, reverse=True)

        l, r = fw_it.next(), rv_it.next()
        while fw_it.has_next() and rv_it.has_next() and (l < r):
            if (l + r) == B:
                return 1
            
            elif (l + r) < B:
                r = rv_it.next()
            else:
                l = fw_it.next()
        
        return 0
            

if __name__ == '__main__':
    from bst import from_list
    x = [7, 10, 9, 20]
    bst = from_list(x)

    sol = Solution()
    sol.t2Sum(bst.root, 19)