# -*- coding: utf-8 -*- 
import collections
import numpy as np
import tensorflow as tf
import datetime

import preprocess

rel_num = 1345
entity_num = 14951

margin = 1
rate = 0.001
dim = 100
batch_size = 100
base_dir = "./FB15k/"


def init_vectors(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.001))

'''
preprocess 
'''
starttime = datetime.datetime.now()
# read dictionary
e2id, rel2id = preprocess.read_dic(base_dir)
# read train set
train_h, train_r, train_t, graph, entity_count, left_positive, right_positive = preprocess.read_train_set(base_dir, e2id, rel2id)
endtime = datetime.datetime.now()
print 'preprocess finished: ', (endtime - starttime)

'''
transE model
'''
head_pos = tf.placeholder(tf.int32)
tail_pos = tf.placeholder(tf.int32)
head_neg = tf.placeholder(tf.int32)
tail_neg = tf.placeholder(tf.int32)
rel_index = tf.placeholder(tf.int32)

# init vectors
rel_vector = init_vectors([rel_num, dim])
entity_vector = init_vectors([entity_num, dim])

# Add histogram summaries for vectors
tf.histogram_summary("rel_vector", rel_vector)
tf.histogram_summary("entity_vector", entity_vector)

# score: ||h+r-t||, size: batchsize
score_positive = tf.reduce_sum(tf.abs(tf.gather(entity_vector, head_pos) +
                                      tf.gather(rel_vector, rel_index) - tf.gather(entity_vector, tail_pos)), 1)
score_negative = tf.reduce_sum(tf.abs(tf.gather(entity_vector, head_neg) +
                                      tf.gather(rel_vector, rel_index) - tf.gather(entity_vector, tail_neg)), 1)

# loss： max(positive_sample + margin - negative_sample, 0)
temp = score_positive + margin - score_negative  # size = batchsize
loss_index = tf.greater(temp, 0)
loss = tf.reduce_sum(tf.select(loss_index, temp, [0]*batch_size))

train_op = tf.train.GradientDescentOptimizer(rate).minimize(loss)

'''
train
'''
train_num = len(train_h)
batch_num = train_num / batch_size
with tf.Session() as sess:
    merged = tf.merge_all_summaries()
    writer = tf.train.SummaryWriter("logs/", sess.graph)
    # initialize all variables
    tf.initialize_all_variables().run()
 
    print 'start training...'
    for i in range(1000):
        starttime = datetime.datetime.now()
        error = 0.0
        for j in range(batch_num):
            batch = np.random.randint(0, train_num, batch_size)
            # build negative samples
            neg_head = []
            neg_tail = []
            for k in batch:
                h = train_h[k]
                t = train_t[k]
                r = train_r[k]
                pro = np.random.randint(0, 2)
                if pro == 0:
                    neg_h = np.random.randint(0, entity_num)
                    while neg_h in left_positive[r][t]:
                        neg_h = np.random.randint(0, entity_num)
                    neg_head.append(neg_h)
                    neg_tail.append(t)
                else:
                    neg_t = np.random.randint(0, entity_num)
                    while neg_t in right_positive[r][h]:
                        neg_t = np.random.randint(0, entity_num)
                    neg_head.append(h)
                    neg_tail.append(neg_t)

            # training
            _, loss_value = sess.run([train_op, loss], feed_dict={head_pos: train_h[batch], tail_pos: train_t[batch],
                                                                  rel_index: train_r[batch], head_neg: neg_head,
                                                                  tail_neg: neg_tail})

            error += loss_value
        summary = sess.run(merged)
        writer.add_summary(summary, i)  # Write summary
        endtime = datetime.datetime.now()
        print "iteration ", i, " : ", error, ' time: ',  (endtime - starttime)
        # save model
        np.save("relation2vec.npy", sess.run(rel_vector))
        np.save("entity2vec.npy", sess.run(entity_vector))


