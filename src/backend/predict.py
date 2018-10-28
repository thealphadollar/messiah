#!/usr/bin/python3
#-*- coding: utf-8 -*-

from datetime import datetime
import numpy as np
import tensorflow as tf
import pandas as pd
import time
import os


EARTHQUAKE_DATA_FILE = "data/earthquake_db.csv"
TRAINED_WEIGHTS_FILE = "data/earthquake_model.ckpt"

def mapdateTotime(x):
    try:
        # print("\n\n")
        # print(x)
        # print('\n\n')
        dt = datetime.strptime(x, "%m/%d/%Y")

    except ValueError:
        dt = datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")

    diff = dt - epoch

    return diff.total_seconds()


def predict_eq(lat, long, depth, date, train=True):
    global epoch, df1

    df1 = pd.read_csv(os.path.join(os.path.dirname(__file__), EARTHQUAKE_DATA_FILE))
    epoch = datetime(1970, 1, 1)

    # Preprocess data
    #--------------------------------------------------
    df1.Date = df1.Date.apply(mapdateTotime)

    col1 = df1[['Date','Latitude','Longitude','Depth']]
    col2 = df1['Magnitude']

    # Convert to Numpy array
    InputX1 = col1.as_matrix()
    InputY1 = col2.as_matrix()

    # print(InputX1)

    # Min-max Normalization
    X1_min = np.amin(InputX1,0)
    X1_max = np.amax(InputX1,0)

    # print("Mininum values:",X1_min)
    # print("Maximum values:",X1_max)

    Y1_min = np.amin(InputY1)     
    Y1_max = np.amax(InputY1) 
    InputX1_norm = (InputX1-X1_min)/(X1_max-X1_min)
    InputY1_norm = InputY1  #No normalization in output

    # Reshape
    Xfeatures = 3 #Number of input features
    Yfeatures = 1 #Number of input features
    samples = 23000 # Number of samples

    InputX1_reshape = np.resize(InputX1_norm,(samples,Xfeatures))
    InputY1_reshape = np.resize(InputY1_norm,(samples,Yfeatures))

    # Training data
    batch_size = 2000
    InputX1train = InputX1_reshape[0:batch_size,:]
    InputY1train = InputY1_reshape[0:batch_size,:]

    # Validation data
    v_size = 2500
    InputX1v = InputX1_reshape[batch_size:batch_size+v_size,:]
    InputY1v = InputY1_reshape[batch_size:batch_size+v_size,:]


    # Train model
    #--------------------------------------------------
    learning_rate = 0.001
    training_iterations = 1000
    display_iterations = 200

    # Input
    X = tf.placeholder(tf.float32,shape=(None,Xfeatures))

    # Output
    Y = tf.placeholder(tf.float32)

    # Neurons
    L1 = 3
    L2 = 3
    L3 = 3

    # Layer1 weights
    W_fc1 = tf.Variable(tf.random_uniform([Xfeatures,L1]))
    b_fc1 = tf.Variable(tf.constant(0.1,shape=[L1]))

    # Layer2 weights
    W_fc2 = tf.Variable(tf.random_uniform([L1,L2]))
    b_fc2 = tf.Variable(tf.constant(0.1,shape=[L2]))

    # Layer3 weights
    W_fc3 = tf.Variable(tf.random_uniform([L2,L3]))
    b_fc3 = tf.Variable(tf.constant(0.1,shape=[L3]))

    # Output layer weights
    W_fO = tf.Variable(tf.random_uniform([L3,Yfeatures]))
    b_fO = tf.Variable(tf.constant(0.1,shape=[Yfeatures]))

    # Layer 1
    matmul_fc1 = tf.matmul(X, W_fc1) + b_fc1
    h_fc1 = tf.nn.relu(matmul_fc1)   #ReLU activation

    # Layer 2
    matmul_fc2 = tf.matmul(h_fc1, W_fc2) + b_fc2
    h_fc2 = tf.nn.relu(matmul_fc2)   #ReLU activation

    # Layer 3
    matmul_fc3 = tf.matmul(h_fc2, W_fc3) + b_fc3
    h_fc3 = tf.nn.relu(matmul_fc3)   #ReLU activation

    # Output layer
    matmul_fc4 = tf.matmul(h_fc3, W_fO) + b_fO
    output_layer = matmul_fc4  #linear activation

    # Loss function
    mean_square =  tf.reduce_mean(tf.square(Y-output_layer))
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(mean_square)

    # Operation to save variables
    saver = tf.train.Saver()

    # Initialization and session
    init = tf.global_variables_initializer()

    if train:
        with tf.Session() as sess:
            sess.run(init)

            # print("Training loss:",sess.run([mean_square],feed_dict={X:InputX1train,Y:InputY1train}))

            for i in range(training_iterations):
                sess.run([train_step],feed_dict={X:InputX1train,Y:InputY1train})
                if i%display_iterations ==0:
                    print("Training loss is:",sess.run([mean_square],feed_dict={X:InputX1train,Y:InputY1train}),"at itertion:",i)
                    print("Validation loss is:",sess.run([mean_square],feed_dict={X:InputX1v,Y:InputY1v}),"at itertion:",i)

            # Save the variables to disk.
            save_path = saver.save(sess, os.path.join(os.path.dirname(__file__), TRAINED_WEIGHTS_FILE))
            # print("Model saved in file: %s" % save_path)

            # print("Final training loss:",sess.run([mean_square],feed_dict={X:InputX1train,Y:InputY1train}))
            # print("Final validation loss:",sess.run([mean_square],feed_dict={X:InputX1v,Y:InputY1v}))


    # Test model
    #--------------------------------------------------
    """
    lat = input("Enter Latitude between -77 to 86:")
    long = input("Enter Longitude between -180 to 180:")
    depth = input("Enter Depth between 0 to 700:")
    date = input("Enter the date (Month/Day/Year format):")
    """

    InputX2 = np.asarray([[lat,long,depth,mapdateTotime(date)]],dtype=np.float32)
    InputX2_norm = (InputX2-X1_min)/(X1_max-X1_min)
    InputX1test = np.resize(InputX2_norm,(1,Xfeatures))

    with tf.Session() as sess:
        # Restore variables from disk for validation.
        saver.restore(sess, os.path.join(os.path.dirname(__file__), TRAINED_WEIGHTS_FILE))
        # print("Model restored.")
        #print("Final validation loss:",sess.run([mean_square],feed_dict={X:InputX1v,Y:InputY1v}))

        output = sess.run([output_layer],feed_dict={X:InputX1test})
        # print("output:", output)

    return output[0][0][0]


if __name__ == '__main__':
    print(predict_eq(70, 70, 70, '10/10/2018'))