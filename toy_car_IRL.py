# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# IRL algorith originally developed for the cart pole problem, modified to run on the toy car obstacle avoidance problem for testing
import numpy as np
import logging
import scipy
from playing import play #get the RL Test agent, gives out feature expectations after 2000 frames
from nn import neural_net #construct the nn and send to playing
from cvxopt import matrix
from cvxopt import solvers
from flat_game import carmunk
from learning import IRL_helper

NUM_SENSORS = 3

# <codecell>

class irlAgent:
    def __init__(self): #initial constructor sorta function
        self.randomPolicy =  [ 708.15413373  ,823.07586729 , 618.50741771  ,  0.0 ] # random initialization
        #self.expertPolicy = [ 662.72064093 , 689.52239795 , 894.57495776  ,  0.0  ] # anti clock motion
        self.expertPolicy =  [ 756.72859592 , 723.5764696 ,  619.23933676 , 0.0  ] # clock motion
        self.epsilon = 1.0
        self.policiesFE = {np.linalg.norm(np.asarray(self.expertPolicy)-np.asarray(self.randomPolicy)):self.randomPolicy}


    def getRLAgentFE(self, W): #get the feature expectations of a new poliicy using RL agent
        IRL_helper(W) # train the agent and save the model 
        saved_model = 'saved-models/164-150-100-50000-25000.h5' # use the saved model to get the feature expectaitons
        model = neural_net(NUM_SENSORS, [164, 150], saved_model)
        return  play(model)#return feature expectations
    
    def policyListUpdater(self, W):  #update the policyFE list and differences upon arrival of a new weight(policy)
        tempFE = self.getRLAgentFE(W)
        self.policiesFE[np.linalg.norm(np.asarray(self.expertPolicy)-np.asarray(tempFE))] = tempFE
        
    def optimalWeightFinder(self):
        while True:
            W = self.optimization()
            print ("weights obtained ::", W )
            t = min(self.policiesFE)
            print ("the value of t is:: ", t )
            if t < self.epsilon:
                break
            self.policyListUpdater(W)
            print ("the distances  ::", self.policiesFE.keys())
        return W
    
    def optimization(self):
        m = len(self.expertPolicy)
        P = matrix(2.0*np.eye(m), tc='d')
        q = matrix(np.zeros(m), tc='d')
        #G = matrix((np.matrix(self.expertPolicy) - np.matrix(self.randomPolicy)), tc='d')
        policyList = []
        h_list = [1]
        policyList.append(self.expertPolicy)
        for i in self.policiesFE.keys():
            policyList.append(self.policiesFE[i])
            h_list.append(1)
        policyMat = np.matrix(policyList)
        policyMat[0] = -1*policyMat[0]
        G = matrix(policyMat, tc='d')
        h = matrix(-np.array(h_list), tc='d')
        sol = solvers.qp(P,q,G,h)
        #print sol['status']
        #return sol['x']
        weights = np.squeeze(np.asarray(sol['x']))
        norm = np.linalg.norm(weights)
        weights = weights/norm
        return weights
                
            
            
if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    #rlEpisodes = 200
    #rlMaxSteps = 250
    #W = [-0.9, -0.9, -0.9, -0.9, 1]
    #env = gym.make('CartPole-v0')
    irlearner = irlAgent()
    #print irlearner.policiesFE
    #irlearner.policyListUpdater(W)
    #print irlearner.rlAgentFeatureExpecs(W)
    #print irlearner.expertFeatureExpecs()
    print (irlearner.optimalWeightFinder())
    #print irlearner.optimization(20)
    #np.squeeze(np.asarray(M))


