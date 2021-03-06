'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy
#from random import betavariate
#from scipy.special import btdtri


class ucb1_2(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''


    
     
    def rewards(self,choice):
        #return random.gauss(self.means[choice],self.variance[choice])
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def ucb1(self,numActions):
    
        #Set the environment
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 300000
        self.numRounds = 60000
        #self.numRounds = 100000 + self.numActions*self.numActions*self.numActions
        #numRounds = 250000
        
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-2
        
        
        self.means =[0.01 for i in range(self.numActions)]
        self.variance =[0.7 for i in range(self.numActions)]
        

        i=(1*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.07
            self.variance[i]=0.1
            i=i+1

        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.03
            i=i+1
        '''
        self.means[self.bestAction]=0.1
        self.variance[self.bestAction]=0.7
        
        
        # initialize empirical sums
        '''
        for i in range(self.numActions):
            self.payoffSums[i] = self.rewards(i)
            self.numPlays[i]=self.numPlays[i]+1
        '''
        
        theta=[0.0]*self.numActions
        success=[0.0]*self.numActions
        failure=[0.0]*self.numActions
        
        for i in range(self.numActions):
            theta[i]=random.betavariate(success[i]+1,failure[i]+1)
            #theta[i]=random.gauss((self.payoffSums[i]/(self.numPlays[i])) ,(1.0/(self.numPlays[i])))
            
        #t = numActions
        
        cumulativeReward = 0
        bestActionCumulativeReward = 0
            
        self.actionRegret=[]
        t=1
        while True:
            #ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            
            for i in range(self.numActions):
                #print random.betavariate(success[i]+1,failure[i]+1)
                theta[i]=random.betavariate((self.payoffSums[i]+1.0),self.numPlays[i]-self.payoffSums[i]+1.0)
                #theta[i]=random.gauss((self.payoffSums[i]/(self.numPlays[i])),(1.0/(self.numPlays[i])))
                #print i,theta[i]
            
            action=max(range(self.numActions), key=lambda i: theta[i])
            
            #self.posterior[arm].update(reward)
            #self.t += 1
            
            #def computeIndex(self, arm):
            #    return self.posterior[arm].sample()

            
            
            #action = max(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(action)
            '''
            theReward1 = sum(numpy.random.binomial(1,theReward,1))/1.0
            
            if theReward1==1.0:
                success[action]=success[action]+1
            else:
                failure[action]=failure[action]+1
            '''
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            if t>=self.numRounds:
                break
            
            t = t + 1
            
            #print t
            
            if t%10000==0:
                print t,regret
            
            
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward
        

        f = open('NewExpt2/expt11/testRegretTS01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t


if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(100):
            obj=ucb1_2()
            random.seed(i+j)
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.ucb1(i)
            if arm!=i-2:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('NewExpt2/expt11/testTS01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
        
