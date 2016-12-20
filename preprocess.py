import collections
import numpy as np


'''
def statistic_frequency(base_dir):
    head_count=[]
    tail_count = []
    for i in range(rel_num):
        triplets_by_rel = np.loadtxt(base_dir+"train/train_"+str(i)+".txt",dtype = np.int32)
        count_h = collections.Counter(triplets_by_rel[:,0]).most_common(n+1)
        count_t = collections.Counter(triplets_by_rel[:,1]).most_common(n+1)
        head_count.append(count_h)
        tail_count.append(count_t)
        
    return head_count, tail_count
    
    #statistic entity frequency and neighbors
def preprocess(train_triplets):
     #store neighbors of every entity
    graph = {}
    for i in range(len(train_triplets)):
        e1 = e2id[ train_triplets[i][0] ]
        e2 = e2id[ train_triplets[i][1] ]
        if e1 not in graph:
            graph[e1] = [e2]
        else:
            graph[e1].append(e2)
        
        if e2 not in graph:
            graph[e2] = [e1]
        else:
            graph[e2].append(e1)
    # statistic entity frequency
    temp_list = train_triplets[:,0].tolist() #[head entities]
    temp_list.extend(train_triplets[:,1].tolist()) #[all entities in train_triplets]
    entity_count = collections.Counter( temp_list ) # statistic entity frequency  
    return graph, entity_count
'''


# read dictionary
def read_dic(base_dir):
    e2id = {}
    rel2id = {}
    # read relation2id.txt"
    with open(base_dir+"relation2id.txt") as f1:
        for line in f1:
            (key, value) = line.strip().split('\t')
            rel2id[key] = int(value)
    # read "entity2id.txt"
    with open(base_dir+"entity2id.txt") as f2:
        for line in f2:
            (key, value) = line.strip().split('\t')
            e2id[key] = int(value)
    return e2id, rel2id


# read train set
def read_train_set(base_dir, e2id, rel2id):
    train_h = []
    train_r = []
    train_t = []
    graph = {}
    entity_count = {}
    left_positive = {}
    right_positive = {}
    with open(base_dir+"train.txt") as f1:
        for line in f1:
            (e1, e2, r) = line.strip().split('\t')
            e1 = e2id[e1]
            e2 = e2id[e2]
            r = rel2id[r]
            train_h.append(e1)
            train_r.append(r)
            train_t.append(e2)
            if r not in left_positive:
                left_positive[r] = {}
            if e2 not in left_positive[r]:
                left_positive[r][e2] = set([e1])
            else:
                left_positive[r][e2].add(e1)
            if r not in right_positive:
                right_positive[r] = {}
            if e1 not in right_positive[r]:
                right_positive[r][e1] = set([e2])
            else:
                right_positive[r][e1].add(e2)
            # store neighbors of every entity
            if e1 not in graph:
                graph[e1] = [e2]
            else:
                graph[e1].append(e2)
            if e2 not in graph:
                graph[e2] = [e1]
            else:
                graph[e2].append(e1)
            # statistic occurrence number of every entity 
            if e1 not in entity_count:
                entity_count[e1] = 1
            else:
                entity_count[e1] += 1
            if e2 not in entity_count:
                entity_count[e2] = 1
            else:
                entity_count[e2] += 1
            
    return np.array(train_h), np.array(train_r), np.array(train_t), graph, entity_count, left_positive, right_positive


# construct training data ,every entity represent as [100, neighbors_num] matrix
def init_input_data(graph, entity_count, base_dir, entity2vec_dir, entity_num, triplet_num, neighbors_num):
    entity_matrix = []
    # read embedings
    entity_vector = np.loadtxt(base_dir + entity2vec_dir)
    
    for i in range(entity_num):
        counter = collections.Counter(graph[i])
        num = len(counter)  # neighbors number of entity i
        data = np.zeros((neighbors_num, 100))
        for (key, value) in counter.items():
            counter[key] = float(value)/num + float(entity_count[key])/triplet_num  # calculate score of neighbors
        rank = sorted(counter.iteritems(), key=lambda d: d[1], reverse=True)

        n = neighbors_num
        if len(rank) < neighbors_num:
            n = len(rank)
            
        for j in range(n):
            data[j, :] = entity_vector[rank[j][0]]
        # data = np.reshape(data, (100,10),order='F')
        entity_matrix.append(data.T.reshape(100, neighbors_num, 1))
    return np.array(entity_matrix)


# read test set
def read_test_set(base_dir, e2id, rel2id):
    test_h = []
    test_r = []
    test_t = []
    left_positive = {}
    right_positive = {}
    graph = {}
    entity_count = {}
    triplet_num = 0
    with open(base_dir+"test.txt") as f1:
        for line in f1:
            (e1, e2, r) = line.strip().split('\t')
            e1 = e2id[e1]
            e2 = e2id[e2]
            r = rel2id[r]
            test_h.append(e1)
            test_r.append(r)
            test_t.append(e2)
            
            if r not in left_positive:
                left_positive[r] = {}
            if e2 not in left_positive[r]:
                left_positive[r][e2] = [e1]
            else:
                left_positive[r][e2].append(e1)

            if r not in right_positive:
                right_positive[r] = {}
            if e1 not in right_positive[r]:
                right_positive[r][e1] = [e2]
            else:
                right_positive[r][e1].append(e2)
    with open(base_dir+"train.txt") as f1:
        for line in f1:
            triplet_num += 1
            (e1, e2, r) = line.strip().split('\t')
            e1 = e2id[e1]
            e2 = e2id[e2]
            r = rel2id[r]
            if r not in left_positive:
                left_positive[r] = {}
            if e2 not in left_positive[r]:
                left_positive[r][e2] = [e1]
            else:
                left_positive[r][e2].append(e1)

            if r not in right_positive:
                right_positive[r] = {}
            if e1 not in right_positive[r]:
                right_positive[r][e1] = [e2]
            else:
                right_positive[r][e1].append(e2)
            # store neighbors of every entity
            if e1 not in graph:
                graph[e1] = [e2]
            else:
                graph[e1].append(e2)
            if e2 not in graph:
                graph[e2] = [e1]
            else:
                graph[e2].append(e1)
            # statistic occurrence number of every entity 
            if e1 not in entity_count:
                entity_count[e1] = 1
            else:
                entity_count[e1] += 1
            if e2 not in entity_count:
                entity_count[e2] = 1
            else:
                entity_count[e2] += 1
    with open(base_dir+"valid.txt") as f1:
        for line in f1:
            (e1, e2, r) = line.strip().split('\t')
            e1 = e2id[e1]
            e2 = e2id[e2]
            r = rel2id[r]
            if r not in left_positive:
                left_positive[r] = {}
            if e2 not in left_positive[r]:
                left_positive[r][e2] = [e1]
            else:
                left_positive[r][e2].append(e1)

            if r not in right_positive:
                right_positive[r] = {}
            if e1 not in right_positive[r]:
                right_positive[r][e1] = [e2]
            else:
                right_positive[r][e1].append(e2)
    return test_h, test_r, test_t, left_positive, right_positive, graph, entity_count, triplet_num


# read relation type
def read_rel_type(base_dir):
    r_11 = []
    r_1n = []
    r_n1 = []
    r_nn = []
    with open(base_dir+"1-1") as f1:
        for line in f1:
            r_11.append(int(line))
    with open(base_dir+"1-N") as f1:
        for line in f1:
            r_1n.append(int(line))
    with open(base_dir+"N-1") as f1:
        for line in f1:
            r_n1.append(int(line))
    with open(base_dir+"N-N") as f1:
        for line in f1:
            r_nn.append(int(line))
    return r_11, r_1n, r_n1, r_nn
