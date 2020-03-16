
# Python program to convert infix expression to postfix 
  
# Class to convert the expression 
class Conversion: 
      
    # Constructor to initialize the class variables 
    def __init__(self, capacity): 
        self.top = -1 
        self.capacity = capacity 
        # This array is used a stack  
        self.array = [] 
        # Precedence setting 
        self.output = [] 
        self.precedence = {'*':3, '?':3, '+':3, '.':2, '|':1} 
      
    # Pop the element from the stack 
    def pop(self): 
        if not self.top == -1: 
            self.top -= 1
            return self.array.pop() 
        else: 
            return "$"
  
    # Check if the precedence of operator is strictly 
    # less than top of stack or not 
    def notGreater(self, i): 
        try: 
            a = self.precedence[i] 
            b = self.precedence[self.array[-1] ] 
            return True if a  <= b else False
        except KeyError:  
            return False
              
    # The main function that converts given infix expression 
    # to postfix expression 
    def infixToPostfix(self, exp): 
          
        # Iterate over the expression for conversion 
        for i in exp: 
            # If the character is an operand,  
            # add it to output 
            if i.isalpha(): 
                self.output.append(i) 
              
            # If the character is an '(', push it to stack 
            elif i  == '(': 
                self.top += 1
                self.array.append(i)
  
            # If the scanned character is an ')', pop and  
            # output from the stack until and '(' is found 
            elif i == ')': 
                while( (not self.top == -1) and self.array[-1]  != '('): 
                    a = self.pop() 
                    self.output.append(a) 
                if (not self.top == -1 and self.array[-1]  != '('): 
                    return -1
                else: 
                    self.pop() 
  
            # An operator is encountered 
            else: 
                while(not self.top == -1 and self.notGreater(i) and i != '*'): 
                    self.output.append(self.pop()) 
                self.top += 1
                self.array.append(i)
  
        # pop all the operator from the stack 
        while not self.top == -1: 
            self.output.append(self.pop()) 
  
        print ("".join(self.output) )
  
# Driver program to test above function 
#exp = "(a|b)*.a.b.b.c"
#exp = "b*.a.b|#"
#exp = "b*.a.b?" #
#exp = "((a|b)*)*.#.((a|b)|#)*"
exp = "(a|b)*.((a|(b.b))*.#))"
obj = Conversion(len(exp)) 
obj.infixToPostfix(exp) 
  
# This code is contributed by Nikhil Kumar Singh(nickzuck_007) 
