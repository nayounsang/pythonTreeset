from collections import deque


class Node:
    def __init__(self, value: int, idx: int, color: int, left: int, right: int, parent: int):
        self.value = value
        self.idx = idx
        self.color = color  # 0:black 1:red
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return f"Node(value={self.value}, idx={self.idx}, color={self.color}, left={self.left}, right={self.right}, " \
               f"parent={self.parent}) "


class treeset:
    def __init__(self):
        self.deleted = deque([])
        self.root = None
        self.mem = []

    def is_null(self, idx):
        if idx is None:
            return True
        if self.mem[idx].value is None:
            return True
        return False

    def inorder(self, node_idx, result):
        if self.mem[node_idx].left is not None:
            self.inorder(self.mem[node_idx].left, result)
        result.append(self.mem[node_idx].value)
        if self.mem[node_idx].right is not None:
            self.inorder(self.mem[node_idx].right, result)

    def __contains__(self, item):  # in
        if self.root is None:
            return False
        cur = self.root
        while True:
            if self.is_null(cur):
                return False
            elif self.mem[cur].value == item:
                return True
            elif item > self.mem[cur].value:
                cur = self.mem[cur].right
            else:
                cur = self.mem[cur].left

    def __str__(self):
        r = []
        self.inorder(self.root, r)
        r_str = ', '.join(list(map(str, r)))
        return f"rbtree([{r_str}])"

    def __len__(self):
        if self.root is None:
            return 0
        stack = [self.root]
        cnt = 0
        while stack:
            node_idx = stack.pop()
            cnt += 1
            if self.mem[node_idx].left is not None:
                stack.append(self.mem[node_idx].left)
            if self.mem[node_idx].right is not None:
                stack.append(self.mem[node_idx].right)
        return cnt

    def __iter__(self):
        r = []
        self.inorder(self.root, r)
        return iter(r)

    def clear(self):
        self.deleted = deque([])
        self.root = None
        self.mem = []

    def printedge(self):
        for i in range(len(self.mem)):
            if self.mem[i].left is not None:
                print(i, self.mem[i].left, 'left')
            if self.mem[i].right is not None:
                print(i, self.mem[i].right, 'right')

    def vaild(self):
        rootc = self.mem[self.root].color
        if rootc == 0:
            print('pass the root color test')
        else:
            print('fail the root color test')
        bd = set([])
        stack = [(self.root, 0)]
        while stack:
            node_idx, black = stack.pop()
            if self.mem[node_idx].color == 0:
                black += 1
            if self.mem[node_idx].left is not None:
                stack.append((self.mem[node_idx].left, black))
            if self.mem[node_idx].right is not None:
                stack.append((self.mem[node_idx].right, black))
            if self.mem[node_idx].left is None and self.mem[node_idx].right is None:
                bd.add(black)
        if len(bd) == 1:
            print('pass the black depth test')
        else:
            print('fail the black depth test')

        stack = [self.root]
        state = False
        while stack:
            node_idx = stack.pop()
            if self.mem[node_idx].parent is not None:
                if self.mem[node_idx].color == 1 and self.get_parcolor(node_idx) == self.mem[node_idx].color:
                    state = True
                    break
            if self.mem[node_idx].left is not None:
                stack.append(self.mem[node_idx].left)
            if self.mem[node_idx].right is not None:
                stack.append(self.mem[node_idx].right)
        if state:
            print('fail the double red test')
        else:
            print('pass the double red test')


    def right_rotate(self, node_idx):

        node = self.mem[node_idx]
        left_child, left_child_idx = self.mem[node.left], node.left
        self.mem[node_idx].left = left_child.right

        if self.mem[node_idx].left is not None:
            self.mem[node.left].parent = node_idx

        self.mem[left_child_idx].parent = node.parent

        if node.parent is None:
            self.root = left_child_idx
        elif node_idx == self.mem[node.parent].left:
            self.mem[node.parent].left = left_child_idx
        else:  # right
            self.mem[node.parent].right = left_child_idx

        self.mem[left_child_idx].right = node_idx
        self.mem[node_idx].parent = left_child_idx

    def left_rotate(self, node_idx):

        node = self.mem[node_idx]
        right_child, right_child_idx = self.mem[node.right], node.right
        self.mem[node_idx].right = right_child.left

        if self.mem[node_idx].right is not None:
            self.mem[node.right].parent = node_idx

        self.mem[right_child_idx].parent = node.parent

        if node.parent is None:
            self.root = right_child_idx
        elif node_idx == self.mem[node.parent].left:
            self.mem[node.parent].left = right_child_idx
        else:  # right
            self.mem[node.parent].right = right_child_idx

        self.mem[right_child_idx].left = node_idx
        self.mem[node_idx].parent = right_child_idx

    def get_parcolor(self, node_idx):
        return self.mem[self.mem[node_idx].parent].color

    def set_parcolor(self, node_idx, c):
        self.mem[self.mem[node_idx].parent].color = c

    def get_par_child_idx(self, node_idx, d):  # d == 0:left, d==1:right
        if d == 0:
            return self.mem[self.mem[node_idx].parent].left
        else:
            return self.mem[self.mem[node_idx].parent].right

    def get_gp_idx(self, node_idx):
        return self.mem[self.mem[node_idx].parent].parent

    def insert_fixup(self, node_idx):
        while self.root != node_idx and self.get_parcolor(node_idx) == 1 and self.mem[node_idx].color == 1:
            p_idx = self.mem[node_idx].parent
            g_idx = self.mem[p_idx].parent
            if p_idx == self.mem[g_idx].left:
                u_idx = self.mem[g_idx].right
                if u_idx is not None and self.mem[u_idx].color == 1:
                    # only recoloring
                    self.mem[g_idx].color = 1
                    self.mem[p_idx].color = 0
                    self.mem[u_idx].color = 0
                    node_idx = g_idx
                else:
                    if node_idx == self.mem[p_idx].right:
                        self.left_rotate(p_idx)
                        node_idx = p_idx
                        p_idx = self.mem[node_idx].parent
                    self.right_rotate(g_idx)
                    c = self.mem[p_idx].color
                    self.mem[p_idx].color = self.mem[g_idx].color
                    self.mem[g_idx].color = c
                    node_idx = p_idx
            else:
                u_idx = self.mem[g_idx].left
                if u_idx is not None and self.mem[u_idx].color == 1:
                    # only recoloring
                    self.mem[g_idx].color = 1
                    self.mem[p_idx].color = 0
                    self.mem[u_idx].color = 0
                    node_idx = g_idx
                else:
                    if node_idx == self.mem[p_idx].left:
                        self.right_rotate(p_idx)
                        node_idx = p_idx
                        p_idx = self.mem[node_idx].parent
                    self.left_rotate(g_idx)
                    c = self.mem[p_idx].color
                    self.mem[p_idx].color = self.mem[g_idx].color
                    self.mem[g_idx].color = c
                    node_idx = p_idx
        self.mem[self.root].color = 0

    def add(self, value):
        if self.__contains__(value):
            return
        cur = self.root

        # generate new node
        if self.deleted:
            idx = self.deleted.pop()
            new_node = Node(value, idx, 1, None, None, None)
            self.mem[idx] = new_node
        else:
            idx = len(self.mem)
            new_node = Node(value, idx, 1, None, None, None)
            self.mem.append(new_node)

        # search pos
        while cur is not None:
            node = self.mem[cur]
            new_node.parent = cur
            if value < node.value:
                cur = node.left
            else:
                cur = node.right

        # bst insert
        par = new_node.parent
        if par is None:
            self.root = idx
        elif value < self.mem[par].value:
            self.mem[par].left = idx
        else:
            self.mem[par].right = idx

        # fix
        if new_node.parent is None:
            self.mem[idx].color = 0
            return
        elif self.mem[par].parent is None:
            return
        self.insert_fixup(idx)








