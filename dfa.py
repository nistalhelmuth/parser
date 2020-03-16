from draw import drawDFA

class Node():
    def __init__(self,  label, left=None,right=None):
        self.left = left
        self.right = right
        self.label = label
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = None
        self.nullable = None
        self.position = None
    
    def setPositions(self, positions=[]):
        if self.label == '*':
            self.left.setPositions(positions)
            return positions
        if self.label == '|' or self.label == '.':
            new_positions = self.left.setPositions(positions)
            self.right.setPositions(new_positions)
            return positions
        else:
            if len(positions) > 0 :
                self.position = len(positions)
            else:
                self.position = 0
            positions.append((self.label, self.position))
            return positions

    def setNullable(self):
        if self.label == '|':
            self.nullable = self.left.setNullable() or self.right.setNullable()
        elif self.label == '.':
            A = self.left.setNullable()
            B = self.right.setNullable()
            self.nullable = A and B
        elif self.label == '*':
            self.left.setNullable()
            self.nullable = True
        elif self.label == '#':
            self.nullable = True
        else:
            self.nullable = False
        
        if self.right != None and self.left != None:
            print((self.left.label, self.label, self.right.label), self.nullable)
        elif self.label == '*':
            print((self.left.label, self.label), self.nullable)
        else:
            print((self.label), self.nullable)
        
        return self.nullable
    
    def setFirstPos(self):
        if self.label == '|':
            A = self.left.setFirstPos()
            B = self.right.setFirstPos()
            self.firstpos = A.union(B)
        elif self.label == '.':
            A = self.left.setFirstPos()
            B = self.right.setFirstPos()
            if self.left.nullable:
                self.firstpos = B.union(A)
            else:
                self.firstpos = A
        elif self.label == '*':
            self.firstpos = self.left.setFirstPos()
        #elif self.label != '#':
        else:
            self.firstpos.add(self.position)

        if self.right != None and self.left != None:
            print((self.left.label, self.label, self.right.label), self.firstpos)
        elif self.label == '*':
            print((self.left.label, self.label), self.firstpos)
        else:
            print((self.label), self.firstpos)
        return self.firstpos

    def setLastPos(self):
        if self.label == '|':
            A = self.left.setLastPos()
            B = self.right.setLastPos()
            self.lastpos = A.union(B)
        elif self.label == '.':
            A = self.left.setLastPos()
            B = self.right.setLastPos()
            if self.right.nullable:
                self.lastpos = A.union(B)
            else:
                self.lastpos = B
        elif self.label == '*':
            self.lastpos = self.left.setLastPos()
        #elif self.label != '#':
        else:
            self.lastpos.add(self.position)   

        if self.right != None and self.left != None:
            print((self.left.label, self.label, self.right.label), self.lastpos)
        elif self.label == '*':
            print((self.left.label, self.label), self.lastpos)
        else:
            print((self.label), self.lastpos)         
        return self.lastpos
    
    def setFollowPos(self, table = {}, positions=set()):
        if self.label == '.':
            table = self.left.setFollowPos(table, self.right.firstpos)
            table = self.right.setFollowPos(table, positions)
        elif self.label == '|':
            table = self.left.setFollowPos(table, positions)
            table = self.right.setFollowPos(table, positions)
        elif self.label == '*':
            table = self.left.setFollowPos(table, self.left.lastpos.union(positions))
        
        #elif self.label != '#':
        else:
            if self.followpos == None:
                self.followpos = positions
            else:
                self.followpos.union(positions)
            #print(self.label, self.position, self.followpos)
            table[(self.label, self.position)] = self.followpos
        return table

        

    def evaluate(self, followtable, language):
        transitions = {}
        Dstates = [self.firstpos]
        letters = 'ABCDEFGHI'
        count = 0
        print(followtable)
        while count < len(Dstates):
            group = Dstates[count]
            for letter in language:
                U = set()
                for pos in group:
                    if (letter, pos) in followtable.keys():
                        A = followtable[(letter, pos)]
                        U = U.union(A)
                if len(U) == 0:
                    continue
                if U not in Dstates:
                    Dstates.append(U)

                if letters[count] in transitions.keys():
                    transitions[letters[count]][letter] =  letters[Dstates.index(U)]
                else:
                    transitions[letters[count]] = {letter: letters[Dstates.index(U)]}
            count += 1
        print(Dstates)
        print(count)
        return transitions, letters[:count]

    def show(self):
        if self.left != None:
            self.left.show()
        if self.right != None:
            self.right.show()
        '''            
        if self.right != None and self.left != None:
            #print(self.nullable, (self.left.label, self.label, self.right.label), self.position, self.firstpos, self.lastpos, self.followpos)
            print((self.left.label, self.label, self.right.label), self.position, self.followpos)
        elif self.label == '*':
            #print(self.nullable, (self.left.label, self.label), self.position, self.firstpos, self.lastpos, self.followpos)
            print((self.left.label, self.label), self.position, self.followpos)
        else:
            #print(self.nullable, (self.label), self.position, self.firstpos, self.lastpos, self.followpos)
            #print((self.label), self.position, self.followpos)
        '''
        if self.label not in '.|*':
            print((self.label), self.position, self.followpos)
        

class DFA:

    def __init__(self, expre):
        self.start = 0
        self.accept = -1
        # Genera el arbol
        self.stack = []
        for ch in expre:
            if ch == '*':
                node_A = self.stack.pop()
                self.stack.append(Node(left=node_A,label='*'))
            elif ch == '.' or ch =='|':
                node_A = self.stack.pop()
                node_B = self.stack.pop()
                self.stack.append(Node(left=node_B, label=ch, right=node_A))
            elif ch == '+': #rr*
                node_A = self.stack.pop()
                node_B = Node(left=node_A, label='*')
                self.stack.append(Node(left=node_A, label='.', right=node_B))
            elif ch == '?': #r|ɛ
                node_A = self.stack.pop()
                node_B = Node(label='#')
                self.stack.append(Node(left=node_A, label='|', right=node_B))
            else:
                self.stack.append(Node(label=ch))
        node_A = self.stack.pop()
        node_B = Node(label='#')
        self.stack.append(Node(left=node_A, label=ch, right=node_B))
        core = self.stack.pop()
        # Encuentra el lenguaje
        self.language = ''
        for letter in expre:
            if letter not in self.language and letter not in '*|().' and letter not in '()':
                self.language += (letter)
        
        print(self.language)
        print('positions')
        core.setPositions()
        print('nullables')
        core.setNullable()
        print('firstpos')
        core.setFirstPos()
        print('lastpos')
        core.setLastPos()
        print('followpos')
        followtable = core.setFollowPos()
        print(followtable)
        #print(followtable)
        transitions, states = core.evaluate(followtable, self.language)
        print(transitions)
        drawDFA(states, transitions)

nfa = DFA('ab|*abb.|*#..')