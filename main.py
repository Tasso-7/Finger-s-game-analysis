from lib import remove_repetitions

N_OF_FINGERS = 5 # all operations will be modulus N_OF_FINGERS


# Class defining every game state
class state:
    a1, a2, b1, b2 = 1, 1, 1, 1 # hands of both players in decreasing order
    def __init__(self, a1, a2, b1, b2):
        a = [a1,a2]
        b = [b1,b2]
        a.sort(reverse=True)
        b.sort(reverse=True)
        self.a1, self.a2 = a[0], a[1]
        self.b1, self.b2 = b[0], b[1]

    def __eq__(self, other):
        if not isinstance(other, state):
            return False
        else:
           return other.a1==self.a1 and other.a2==self.a2 and other.b1==self.b1 and other.b2==self.b2
    
    def __str__(self):
        return f"({self.a1}{self.a2};{self.b1}{self.b2})"
    def __repr__(self):
        return str(self)
    
    def Adj(self): # all possible outcomes
        ADJs = []
        
        # Split
        if self.a2 == 0 and a1%2==0:
            ADJs.append(state(self.a1/2, self.a1/2, self.b1, self.b2))
        # Normal moves
        for i in [self.a1,self.a2]:
            if i == 0:
                continue
            for j in [0,1]:
                if [self.b1,self.b2][j] == 0:
                    continue
                ADJs.append(state(
                    (i+[self.b1,self.b2][j])%N_OF_FINGERS, # where we actually sum
                    [self.b2,self.b1][j],self.a1,self.a2)) # values that remain unchanged
        
        return remove_repetitions(ADJs)
    

def stateGenerator():
    nOfConfings = (N_OF_FINGERS*(N_OF_FINGERS+1)/2)**2 # N of states the game can be in 
    nOfConfings = int(nOfConfings)

    States = [] # set of all states
    bestMoves = [" " for i in range(0, nOfConfings)] # best move for every state
    Values = [" " for i in range(0, nOfConfings)] # value of every state [-1;1]

    j = 0
    for a in range(0, N_OF_FINGERS, 1):
        for b in range(a + 1):
            for c in range(0, N_OF_FINGERS, 1):
                for d in range(c + 1):
                    States.append(state(a,b,c,d)) # Generating states
                    if a == b and a == 0: # it's a lost game
                        Values[j] = -1
                        bestMoves[j] = []
                    j+=1
    return (States, Values, bestMoves) # a " " means unkown

if __name__ == "__main__":
    print("WELCOME TO FINGER'S GAME ANALYSIS")
    for i in stateGenerator():
        print(i)
    