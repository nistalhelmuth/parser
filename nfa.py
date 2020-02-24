NUMS = '0123456789'
OPS = '*/+-'

class Node():
  def __init__(self,  label, left=None,right=None):
    self.left = left
    self.right = right
    self.label = label
  

  '''
    crea un NFA a partir de un nodo inicial
    input: 
      states: array de estados
      transitions: diccionario de transiciones de la forma:
        {
          nodo_incial: {
            input: [nodo_siguiente, nodo_siguiente]
          }
        }
      start: número del nodo inicial
      end: número del nodo final
  '''
  def evaluate(self, states=[0,-1], transitions={ 0: {}}, start=0, end=-1):

    #crea un nodo nuevo
    def addState(states, transitions):
      new_state = max(states) + 1
      states.append(new_state)
      transitions[new_state] = {}
      return states, transitions, new_state

    if self.label == '*': #caso para a*
      states, transitions, new_state1 = addState(states, transitions)
      if '#' in transitions[start].keys():
        transitions[start]['#'].append(new_state1)
        transitions[start]['#'].append(end)
      else:
        transitions[start] = {'#':[new_state1, end]}
      states, transitions, new_state2 = addState(states, transitions)
      transitions[new_state2] = {'#':[end, new_state1]}
      states, transitions = self.left.evaluate(states, transitions, new_state1, new_state2)
      return states, transitions

    if self.label == '.': #caso para a.b
      states, transitions, new_state1 = addState(states, transitions)
      states, transitions = self.left.evaluate(states, transitions, new_state1, end)
      states, transitions = self.right.evaluate(states, transitions, start, new_state1)
      return states, transitions

    if self.label == '|': #caso para a|b
      states, transitions, new_state1 = addState(states, transitions)
      states, transitions, new_state2 = addState(states, transitions)
      if '#' in transitions[start].keys():
        transitions[start]['#'].append(new_state1)
        transitions[start]['#'].append(new_state2)
      else:
        transitions[start] = {'#':[new_state1, new_state2]}

      states, transitions, new_state3 = addState(states, transitions)
      states, transitions, new_state4 = addState(states, transitions)
      transitions[new_state3] = {'#':[end]}
      transitions[new_state4] = {'#':[end]}
      states, transitions = self.left.evaluate(states, transitions, new_state1, new_state3)
      states, transitions = self.right.evaluate(states, transitions, new_state2, new_state4)
      return states, transitions

    else: #caso para a
      if start in transitions.keys(): 
        if self.label in transitions[start].keys():
          transitions[start][self.label].append(end)
        else:
          transitions[start][self.label] = [end]
      else: 
        transitions[start] = {self.label: [end]}
      return states, transitions
    

class NFA:
  '''
    crea un arbol según una expresión en posfix
  '''
  def __init__(self, expre):
    self.stack = []
    for ch in expre:
      if ch == '*':
        node_A = self.stack.pop()
        self.stack.append(Node(left=node_A,label='*'))
      elif ch == '.' or ch =='|':
        node_A = self.stack.pop()
        node_B = self.stack.pop()
        self.stack.append(Node(left=node_A, label=ch, right=node_B))
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
    core = self.stack.pop()
    self.states, self.transitions = core.evaluate()
    self.language = ''
    for letter in expre:
      if letter not in self.language and letter not in '*|().' and letter not in '()':
        self.language += (letter)
    print(self.language)
    print(self.states)
    print(self.transitions)
  
  def convertToDFA(self):
    def closure(states):
      stack = []
      for state in states:
        if state != -1:
          stack = stack + self.transitions[state]['#']
      group = states
      while len(stack):
        element = stack.pop()
        if element == -1:
          continue
        if element not in group:
          group.append(element)
        if '#' in self.transitions[element].keys():
          for node in self.transitions[element]['#']:
            stack.append(node)
      
      return group
    
    def move(states, value):
      group = []
      for state in states:
        if state != -1 and value in self.transitions[state].keys():
          for element in self.transitions[state][value]:
            if element not in group:
              group.append(element)      
      return group
    
    transitions = {}
    Dstate = [closure([0])]
    letters = 'ABCDEFGHI'
    count = 0
    while count < len(Dstate):
      group = Dstate[count]
      for letter in self.language:
        U = closure(move(group, letter))
        if (len(U)==0):
          continue
        if ( U not in Dstate):
          Dstate.append(U)
        if letters[count] in transitions.keys(): 
          if letter in transitions[letters[count]].keys():
            transitions[letters[count]][letter].append(letters[Dstate.index(U)])
          else:
            transitions[letters[count]][letter] = [letters[Dstate.index(U)]]
        else: 
          transitions[letters[count]] = {letter: [letters[Dstate.index(U)]]}
      count += 1
    print(transitions)
    print(letters[:count])
    #print(self.transitions[1]['#'])
    

  

#test = input('to evaluate: ')
nfa = NFA('a*b*|c.')
nfa.convertToDFA()


