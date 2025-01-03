from lib import remove_repetitions, zeroer

N_OF_FINGERS = 5 # all operations will be modulus N_OF_FINGERS


# Class defining every game state
class state:
    a1, a2, b1, b2 = 1, 1, 1, 1 # hands of both players in decreasing order
    def __init__(self, a1, a2, b1, b2):
        a = [int(a1),int(a2)]
        b = [int(b1),int(b2)]
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
    
    def strA(self):
        return f"({self.a1}{self.a2})"
    
    def strB(self):
        return f"({self.b1}{self.b2})"
    
    def Adj(self): # all possible outcomes
        ADJs = []
        
        # Split
        if self.a2 == 0 and self.a1%2==0:
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

class stateAnalyzer:
    nOfConfings = 0
    nOfHandConfings = 0
    states = []
    bestMoves = []
    stateEvaluations = []
    stateResults = []
    stateAdj = []
    gamma = 0.005
    epsilon = 0.01

    def __init__(self, gamma=0.0025, epsilon=0.05):
        self.states, self.stateEvaluations, self.bestMoves, self.stateResults = self.stateGenerator()
        self.gamma, self.epsilon = gamma, epsilon
        
        for i in self.states:
            self.stateAdj.append(i.Adj())

    def logicalIteration(self): # P(N) = zeroer(MAX(ADJ); epsilon+gamma*#ADJ) # Updates values and returns if any update has happened
        new_stateResult = self.stateResults[:]
        has_done_any_updates = False

        for j, s in enumerate(self.states):
            if self.stateResults[j] != " ": # State has alredy been analyzed
                continue
            ADJS = s.Adj()

            is_winning_state = False # We don't consider state winning until we find a winning continuation
            is_losing_state = True   # We consider the state losing until we find a not losing continuation

            for k in ADJS:
                i = self.states.index(k)
                res = self.stateResults[i]
                if res == -1: # There's a winning continuation
                    is_winning_state = True
                if res != 1:  # There's a not losing continuation
                    is_losing_state = False


            # Upated value
            if is_winning_state:
                new_stateResult[j] = 1
            if is_losing_state:
                new_stateResult[j] = -1

            if is_losing_state or is_winning_state: # We need to evaluate the state statistically
                has_done_any_updates = True

                m = -1.0 # MAXIMUM VALUE SO FAR
                for k in ADJS:
                    try: # because the state may not have an evaluation
                        o = float(self.stateEvaluations[self.states.index(k)])
                        m = max(m, -o)
                    except:
                        pass
                self.stateEvaluations[j] = zeroer(m, self.epsilon + self.gamma * (len(ADJS)-1))

        self.stateResults = new_stateResult[:]
        return has_done_any_updates
    
    def multiLogicIteration(self):
        last_iteration_has_done_any_updates = True
        while last_iteration_has_done_any_updates:
            last_iteration_has_done_any_updates = self.logicalIteration()

    def printMoves(self):
        # prints intestation
        print("     | ", end="")
        for i in range(1,self.nOfHandConfings):
             print(self.states[i].strB(), end="  | ")
        
        # rows containes the states of every row of the game
        rows = []
        r = []
        for i in self.states:
            r.append(i)
            if i.b1 == i.b2 and i.b1 == N_OF_FINGERS -1:
                rows.append([k for k in r])
                r = []

        for i in rows:
            print("\n"+"-"*118)
            for j in range(4):
                if j == 0:
                    print(end=i[0].strA() + " |")
                else:
                    print("\n",end="     |")
                for s in i:
                    if s.strB() == "(00)":
                        continue
                    ADJ = s.Adj()
                    A = "       "
                    if len(ADJ)>j:
                        A = str(ADJ[j])
                    print(A,end="|")

    def printAnalysis(self):
        # prints intestation
        print("     |       ", end="")
        for i in range(1,self.nOfHandConfings):
            print(self.states[i].strB(), end="     |       ")
        
        # rows containes the states of every row of the game
        rows = []
        r = []
        for i in self.states:
            r.append(i)
            if i.b1 == i.b2 and i.b1 == N_OF_FINGERS -1:
                if i.a1 != 0:
                    rows.append([k for k in r])
                r = []

        for i in rows:
            print("\n"+"-"*244)
            for j in range(4):
                if j == 0:
                    print(end=i[0].strA() + " | ")
                else:
                    print("\n",end="     | ")
                for s in i:
                    if s.strB() == "(00)" or s.strA() == "(00)":
                        continue
                    ADJ = s.Adj()
                    A = "              "
                    if len(ADJ)>j:
                        a = ADJ[j]
                        r = " U"
                        v = "     "
                        
                        if type(self.stateResults[self.states.index(a)]) == int:
                           r = [" T"," W"," L"][self.stateResults[self.states.index(a)]] # -1 LOST, 0 UNKOWN, 1 WON

                        if type(self.stateEvaluations[self.states.index(a)]) == float:
                            v = str(round(self.stateEvaluations[self.states.index(a)],2))
                            v = " "*(5-len(v)) + v
                        A = str(ADJ[j])+r+v
                    print(A,end=" | ")

    def stateGenerator(self):
        self.nOfHandConfings = (N_OF_FINGERS*(N_OF_FINGERS+1)/2) 
        self.nOfHandConfings = int(self.nOfHandConfings) 
        self.nOfConfings = self.nOfHandConfings ** 2

        States = [] # set of all states
        bestMoves = [" " for i in range(0, self.nOfConfings)] # best move for every state
        Values = [" " for i in range(0, self.nOfConfings)] # value of every state [-1;1]

        j = 0
        for a in range(0, N_OF_FINGERS, 1):
            for b in range(a + 1):
                for c in range(0, N_OF_FINGERS, 1):
                    for d in range(c + 1):
                        States.append(state(a,b,c,d)) # Generating states
                        if a == b and a == 0: # it's a lost game
                            Values[j] = -1.0
                            bestMoves[j] = []
                        j+=1
               # States, eval,  best,      result if perfect match
        return (States, Values, bestMoves, [int(k) if type(k)==float else " " for k in Values]) # a " " means unkown

if __name__ == "__main__":
    print("WELCOME TO FINGER'S GAME ANALYSIS")
    s = stateAnalyzer()
    s.multiLogicIteration()
    s.printAnalysis()