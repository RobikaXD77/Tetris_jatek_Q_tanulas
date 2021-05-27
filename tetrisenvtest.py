import pygame
import numpy as np
import random
from gym import Env
from gym.spaces import Discrete, Box

import numpy as np
import tensorflow as tf
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Permute
from tensorflow.keras.optimizers import Adam


import rl.agents
import rl.policy
import rl.memory

import tetrisenv

env = tetrisenv.TetrisEnv()


states = env.observation_space.shape
actions = env.action_space.n


#def build_model(states, actions):
#    model = Sequential()
#    model.add(Permute((2, 3, 1), input_shape=(1, 20, 10)))
#    model.add(tf.keras.layers.Conv2D(32, 3, activation = 'relu', padding = 'valid'))
#    model.add(tf.keras.layers.Conv2D(32, 3, activation = 'relu', padding = 'valid'))
#    model.add(tf.keras.layers.Conv2D(64, 3, activation = 'relu', padding = 'valid'))
#    model.add(tf.keras.layers.Conv2D(64, (14,1), activation = 'relu', padding = 'valid'))
#    model.add(tf.keras.layers.Conv2D(128, (1,3), activation = 'relu', padding = 'valid'))
#    model.add(tf.keras.layers.Conv2D(128, 1, activation = 'relu', padding = 'valid'))
    
#    model.add(Flatten())

#    model.add(Dense(128, activation='relu'))
#    model.add(Dense(512, activation='relu'))
#    model.add(Dense(actions, activation='relu'))
#    return model

#-----------------------------------------------------------------------------------------------------------

#def build_model(states, actions):
#    model = Sequential()
#    model.add(Permute((2, 3, 1), input_shape=(1, 20, 10)))
#    model.add(tf.keras.layers.Conv2D(32, 10, activation = 'relu', padding = 'valid'))
#    model.add(tf.keras.layers.Conv2D(64, (11,1), activation = 'relu', padding = 'valid'))
    
#    model.add(Flatten())

#    model.add(Dense(64, activation='relu'))
#    model.add(Dense(actions, activation='relu'))
#    return model

#------------------------------------------------------------------------------------------------------------

#def build_model(states, actions):
#    model = Sequential()
#    model.add(Permute((2, 3, 1), input_shape=(1, 20, 10)))
#    model.add(tf.keras.layers.Conv2D(32, (10,1), strides = (10,1), activation = 'relu', padding = 'valid'))
#    model.add(tf.keras.layers.ZeroPadding2D(padding = (0,1)))
#    model.add(tf.keras.layers.Conv2D(64, (1,3), activation = 'relu', padding = 'valid'))

#    model.add(Flatten())

#    model.add(Dense(320, activation='relu'))
#    model.add(Dense(640, activation='relu'))
#    model.add(tf.keras.layers.Dropout(0.2))
#    model.add(Dense(actions, activation='relu'))
#    return model

#------------------------------------------------------------------------------------------------------------

def build_model(states, actions):
    model = Sequential()
    model.add(Permute((2, 3, 1), input_shape=(1, 20, 10)))
    model.add(tf.keras.layers.Conv2D(32, (20,1), activation = 'relu', padding = 'valid'))

    model.add(Flatten())

    model.add(Dense(320, activation='relu'))
    model.add(Dense(640, activation='relu'))
    model.add(Dense(actions, activation='relu'))
    return model


model = build_model(states, actions)

print(model.summary())
print(states)

#Agent with Keras-RL



def build_agent(model, actions):
    policy = rl.policy.EpsGreedyQPolicy()
    memory = rl.memory.SequentialMemory(limit=100000, window_length=1)
    dqn = rl.agents.DQNAgent(model=model, memory=memory, policy=policy, 
                  nb_actions=actions, nb_steps_warmup=2000)
    return dqn

dqn = build_agent(model, actions)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

dqn.fit(env, nb_steps=1000000, visualize=False, verbose=1)
dqn.save_weights('dqn_10mill_model4_EpsGreedQ_100k.h5f')

#dqn.load_weights('dqn_10mill_model1_EpsGreedQ_100k.h5f')

#scores = dqn.test(env, nb_episodes=10, visualize=True, nb_max_episode_steps=500)
#print(np.mean(scores.history['episode_reward']))
