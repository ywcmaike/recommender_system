import collections
import numpy as np
import tensorflow as tf
import datetime

import preprocess

rel_num = 1345
entity_num = 14951
base_dir = "./FB15k/"
relation2vec_dir = "relation2vec.npy"
entity2vec_dir = "entity2vec.npy"

# read dictionary
e2id ,rel2id = preprocess.read_dic(base_dir)
# read relation type
r_11, r_1n, r_n1, r_nn = preprocess.read_rel_type(base_dir)
# read test set
test_h, test_r, test_t, left_positive, right_positive, _, _, triplet_num = preprocess.read_test_set(base_dir, e2id, rel2id)
# load embeddings
entity_vector = np.load(entity2vec_dir)
rel_vector = np.load(relation2vec_dir)

head = tf.placeholder(tf.float32, [100])
tail = tf.placeholder(tf.float32, [100])
rel = tf.placeholder(tf.float32, [100])
positive_l = tf.placeholder(tf.bool, [entity_num])
positive_r = tf.placeholder(tf.bool, [entity_num])

score = tf.reduce_sum(tf.abs(head+rel-tail))

head_list = tf.reshape(tf.tile(head, [entity_num]), [entity_num, 100])
tail_list = tf.reshape(tf.tile(tail, [entity_num]), [entity_num, 100])
rel_list = tf.reshape(tf.tile(rel, [entity_num]), [entity_num, 100])

left_list = tf.reduce_sum(tf.abs(entity_vector + rel_list - tail_list), 1)
right_list = tf.reduce_sum(tf.abs(head_list + rel_list - entity_vector), 1)

left_bool = tf.less(left_list, score)  # true if less than test entity
right_bool = tf.less(right_list, score)

left_rank = tf.reduce_sum(tf.to_int32(left_bool)) + 1
right_rank = tf.reduce_sum(tf.to_int32(right_bool)) + 1

left_filter_rank = tf.reduce_sum(tf.to_int32(tf.logical_and(left_bool, positive_l))) + 1
right_filter_rank = tf.reduce_sum(tf.to_int32(tf.logical_and(right_bool, positive_r))) + 1

# test
l_sum = 0; r_sum = 0
l_filter_sum = 0; r_filter_sum = 0
l_hit_1 = 0; r_hit_1 = 0
l_filter_hit_1 = 0; r_filter_hit_1 = 0
l_hit_10 = 0; r_hit_10 = 0
l_filter_hit_10 = 0; r_filter_hit_10 = 0
l_mrr = 0; r_mrr = 0
l_filter_mrr = 0; r_filter_mrr = 0

l_11_h10=0; l_1n_h10=0; l_n1_h10=0; l_nn_h10=0
r_11_h10=0; r_1n_h10=0; r_n1_h10=0; r_nn_h10=0
num_11=0; num_1n=0; num_n1=0; num_nn=0

total_num = len(test_h)
starttime = datetime.datetime.now()
with tf.Session() as sess:
    # initialize all variables
    tf.initialize_all_variables().run()
    for i in range(total_num): 
        h = test_h[i]
        r = test_r[i]
        t = test_t[i]
        left = np.array([True]*entity_num)
        right = np.array([True]*entity_num)
        left[left_positive[r][t]] = False  # positive entities
        right[right_positive[r][h]] = False

        l_rank, r_rank, l_filter_rank, r_filter_rank = sess.run([left_rank, right_rank, left_filter_rank, right_filter_rank],
                        feed_dict ={head: entity_vector[h], tail: entity_vector[t], rel: rel_vector[r],
                        positive_l: left, positive_r: right})

        l_sum += l_rank
        r_sum += r_rank
        l_filter_sum += l_filter_rank
        r_filter_sum += r_filter_rank
            
        if l_rank <= 10:
            l_hit_10 += 1
            if l_rank == 1:
                l_hit_1 += 1
        if r_rank <= 10:
            r_hit_10 += 1
            if r_rank == 1:
                r_hit_1 += 1       
        if l_filter_rank <= 10:
            l_filter_hit_10 += 1
            if l_filter_rank == 1:
                l_filter_hit_1 += 1
            if r in r_11:
                l_11_h10 += 1
            elif r in r_1n:
                l_1n_h10 += 1
            elif r in r_n1:
                l_n1_h10 += 1
            else:
                l_nn_h10 += 1
        if r_filter_rank <= 10:
            r_filter_hit_10 += 1
            if r_filter_rank == 1:
                r_filter_hit_1 += 1
            if r in r_11:
                r_11_h10 += 1
            elif r in r_1n:
                r_1n_h10 += 1
            elif r in r_n1:
                r_n1_h10 += 1
            else:
                r_nn_h10 += 1
                
        l_mrr += 1.0/l_rank
        r_mrr += 1.0/r_rank
        l_filter_mrr += 1.0/l_filter_rank
        r_filter_mrr += 1.0/r_filter_rank
        
        if r in r_11:
            num_11 += 1
        elif r in r_1n:
            num_1n += 1
        elif r in r_n1:
            num_n1 += 1
        else:
            num_nn +=1
 
        if i % 5000 == 0:
            print i
    endtime = datetime.datetime.now()
    print 'test finished: ', (endtime - starttime)
f = open('result.txt', 'w')
f.write("        mr" + '\t' + 'f_mr' + '\t' + 'Hits@10' + '\t' + 'f_Hits@10' + '\t' + 'Hit@1' + '\t'+'f_Hit@1' + '\t' + 'mrr' + '\t' + 'f_mrr'+'\n' )
f.write('left:  '+str("%.3f" %(float(l_sum)/total_num)) + '\t' + str("%.3f" %(float(l_filter_sum)/total_num)) + '\t' + str("%.3f" %(float(l_hit_10)/total_num)) + '\t' + str("%.3f" %(float(l_filter_hit_10)/total_num)) + '\t' + str("%.3f" %(float(l_hit_1)/total_num)) + '\t'+ str("%.3f" %(float(l_filter_hit_1)/total_num)) + '\t' + str("%.3f" %(l_mrr/total_num)) + '\t' + str("%.3f" %(l_filter_mrr/total_num))+'\n')
f.write('right: '+str("%.3f" %(float(r_sum)/total_num)) + '\t' + str("%.3f" %(float(r_filter_sum)/total_num)) + '\t' + str("%.3f" %(float(r_hit_10)/total_num)) + '\t' + str("%.3f" %(float(r_filter_hit_10)/total_num)) + '\t' + str("%.3f" %(float(r_hit_1)/total_num)) + '\t'+ str("%.3f" %(float(r_filter_hit_1)/total_num)) + '\t' + str("%.3f" %(r_mrr/total_num)) + '\t' + str("%.3f" %(r_filter_mrr/total_num))+'\n')
f.write( 'mean : '+str("%.3f" %(float(r_sum+l_sum)/(2*total_num))) + '\t' + str("%.3f" %(float(r_filter_sum+l_filter_sum)/(2*total_num))) + '\t' + str("%.3f" %(float(r_hit_10+l_hit_10)/(2*total_num))) + '\t' + str("%.3f" %(float(r_filter_hit_10+l_filter_hit_10)/(2*total_num))) + '\t' + str("%.3f" %(float(r_hit_1+l_hit_1)/(2*total_num))) + '\t'+ str("%.3f" %(float(r_filter_hit_1+l_filter_hit_1)/(2*total_num))) + '\t' + str("%.3f" %((r_mrr+l_mrr)/(2*total_num))) + '\t' + str("%.3f" %((r_filter_mrr+l_filter_mrr)/(2*total_num)))+'\n'+'\n')
f.write("filtered hits@10 rate :"+'\n')
f.write('relation_type'+'\t'+'left_hits@10'+'\t'+'right_hits@10'+'\n')
f.write('1-1'+'\t\t'+ str("%.4f" %(float(l_11_h10)/num_11))+'\t\t'+str("%.3f" %(float(r_11_h10)/num_11))+'\n')
f.write('1-N'+'\t\t'+ str("%.4f" %(float(l_1n_h10)/num_1n))+'\t\t'+str("%.3f" %(float(r_1n_h10)/num_1n))+'\n')
f.write('N-1'+'\t\t'+ str("%.4f" %(float(l_n1_h10)/num_n1))+'\t\t'+str("%.3f" %(float(r_n1_h10)/num_n1))+'\n')
f.write('N-N'+'\t\t'+ str("%.4f" %(float(l_nn_h10)/num_nn))+'\t\t'+str("%.3f" %(float(r_nn_h10)/num_nn))+'\n')
f.close()


