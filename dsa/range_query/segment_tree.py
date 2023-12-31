MAX_INT = 1_000_000

# get the smallest power of 2 that no less than x
def msb(x: int) -> int:
    if x.bit_count() == 1:
        return x 
    else:
        return 1 << (x.bit_length())

# Recursive Building for sum query
class SegmentTreeNode:

    def __init__(self, start: int, end: int, sum: int,
                left: 'SegmentTreeNode' = None, 
                right: 'SegmentTreeNode' = None):
        self.start = start
        self.end = end 
        self.sum = sum 

        self.left = left 
        self.right = right

class SegmentTree:

    tree: SegmentTreeNode
    
    def __init__(self, nums: list[int]):
        self.nums = nums 
        self.tree = self.__build_tree(0, len(nums) - 1)

    # query in O(log(n))
    def query_sum(self, a: int, b: int, root: SegmentTreeNode = None) -> int:
        if root == None:
            root =  self.tree
        
        if root.start == a and root.end == b:
            return root.sum
        
        mid = (root.start + root.end) // 2
        if b <= mid:
            return self.query_sum(a, b, root.left)
        elif a > mid:
            return self.query_sum(a, b, root.right)
        else:
            return self.query_sum(a, mid, root.left) + \
                   self.query_sum(mid + 1, b, root.right)
    
    # update in O(log(n))
    def update(self, idx: int, val: int, root: SegmentTreeNode = None):
        if root == None:
            root = self.tree
        
        # find the leaf node, stop searching
        if root.start == root.end == idx:
            # update leaf value
            root.sum = val  
            return
        
        mid = (root.start + root.end) // 2
        if idx <= mid:
            self.update(idx, val, root.left)
        else:
            self.update(idx, val, root.right)
        # Important: update node sum........
        root.sum = root.left.sum + root.right.sum

    def __build_tree(self, start: int, end: int) -> SegmentTreeNode:
        if start == end:
            return SegmentTreeNode(start, end, self.nums[start])
        
        mid = (start + end) // 2
        left = self.__build_tree(start, mid)
        right = self.__build_tree(mid + 1, end)
        return SegmentTreeNode(start, end, left.sum + right.sum, left, right)


# Iterative List Building for minimum query
class SegmentTreeList:
    """
    Easy to implement for arrays whose length are power of 2.
    If not, one can always append zeroes to make up the length.

    for node with idx (0-index): 
        left: 2 * idx + 1
        right: 2 * idx + 2
        parent: (idx - 1) // 2
    """

    tree_list: list[int]

    def __init__(self, nums: list[int]):
        self.nums = nums 
        self.__build_tree()
    
    # query in O(log(n))
    def query_min(self, a: int, b: int) -> int:
        a += self.offset
        b += self.offset
        
        res = MAX_INT
        while a <= b:
            if a % 2 == 0: # a is on right child
                res = min(res, self.tree_list[a])
                a += 1
            if b % 2 == 1: # b is on left child
                res = min(res, self.tree_list[b])
                b -= 1
            
            a = (a - 1) // 2
            b = (b - 1) // 2
        
        return res
    
    # update in O(log(n))
    def update(self, idx: int, val: int):
        idx += self.offset
        self.tree_list[idx] = val

        while (idx - 1) // 2 >= 0:
            idx = (idx - 1) // 2 # parent_idx
            tmp = self.tree_list[idx]
            
            if 2 * idx + 1 < len(self.tree_list):
                tmp = min(tmp, self.tree_list[2 * idx + 1])
            if 2 * idx + 2 < len(self.tree_list):
                tmp = min(tmp, self.tree_list[2 * idx + 2])
            
            self.tree_list[idx] = tmp

    # build in O(n) with extra space O(n)
    def __build_tree(self) -> list[int]:
        n = len(self.nums)
        self.offset = msb(n) - 1
        self.tree_list = [MAX_INT] * (self.offset + n)

        # put in leaf values
        for i in range(n):
            self.tree_list[i + self.offset] = self.nums[i]
        
        # update non-leaf values
        for i in range(self.offset - 1, -1, -1):
            tmp = self.tree_list[i]

            if 2 * i + 1 < self.offset + n:
                tmp = min(tmp, self.tree_list[2 * i + 1])
            if 2 * i + 2 < self.offset + n:
                tmp = min(tmp, self.tree_list[2 * i + 2])
            
            self.tree_list[i] = tmp


# Iterative List Building for sum query
class SegmentTreeEasyList:
    """
    This is a much easier implementation for segment tree with 
    list structure, but it is also much harder to understand.

    for node with idx (1-index): 
        left: idx << 1
        right: idx << 1 | 1
        parent: idx >> 1
    """

    tree_list: list[int]

    def __init__(self, nums: list[int]):
        self.nums = nums
        self.__build_tree()
    
    # query in O(log(n))
    def query_sum(self, a: int, b: int) -> int:
        a += len(self.nums)
        b += len(self.nums)

        res = 0
        while a <= b:
            if (a & 1):
                res += self.tree_list[a]
                a += 1
            
            if ((b + 1) & 1):
                res += self.tree_list[b]
                b -= 1
            
            a >>= 1
            b >>= 1

        return res
    
    # update in O(log(n))
    def update(self, idx: int, val: int):
        idx += len(self.nums)
        self.tree_list[idx] = val

        while idx > 1:
            idx >>= 1 # parent idx

            self.tree_list[idx] =\
            self.tree_list[idx << 1] + self.tree_list[idx << 1 | 1]

    # build in O(n) with extra space O(n)
    def __build_tree(self) -> list[int]:
        n = len(self.nums)
        self.tree_list = [0] * (2 * n) # !!!

        # original values with offset n
        for i in range(n):
            self.tree_list[i + n] = self.nums[i]
        
        # non-leaf values from (n - 1) ~ 1
        for i in range(n - 1, 0, -1):
            self.tree_list[i] = \
            self.tree_list[i << 1] + self.tree_list[i << 1 | 1]



if __name__ == "__main__":
    nums = [1, 3, 4, -3, 8, 6, 1, 4, 2]
    mySegTree = SegmentTree(nums)
    mySegTreeEasy = SegmentTreeEasyList(nums)
    mySegTreeList = SegmentTreeList(nums)
    
    print(f"Orignal nums: {nums}")

    print("Segment Tree:")
    print(f"Range [0, 1] sum: {mySegTree.query_sum(0, 1)}")
    print(f"Range [0, 6] sum: {mySegTree.query_sum(0, 6)}")
    print(f"Range [6, 7] sum: {mySegTree.query_sum(6, 7)}")
    print("Segment Tree (Easy List Version):")
    print(f"Range [0, 1] sum: {mySegTreeEasy.query_sum(0, 1)}")
    print(f"Range [0, 6] sum: {mySegTreeEasy.query_sum(0, 6)}")
    print(f"Range [6, 7] sum: {mySegTreeEasy.query_sum(6, 7)}")

    print(f"Update index 3 with -4")
    mySegTree.update(3, -4)
    mySegTreeEasy.update(3, -4)
    print(f"Range [1, 3] sum: {mySegTree.query_sum(1, 3)}")
    print(f"Range [1, 3] sum: {mySegTreeEasy.query_sum(1, 3)}")

    print("Segment Tree (List Version):")
    print(f"Range [0, 1] min: {mySegTreeList.query_min(0, 1)}")
    print(f"Range [0, 6] min: {mySegTreeList.query_min(0, 6)}")
    print(f"Range [6, 7] min: {mySegTreeList.query_min(6, 7)}")

    print(f"Update index 3 with -4")
    mySegTreeList.update(3, -4)
    print(f"Range [1, 3] min: {mySegTreeList.query_min(1, 3)}")