import numpy as np

def load_cuts(fname):
    with open(fname, 'r') as f:
        data = []
        for line in f:
            if not line[0] == '#':
                data.append(list(line[:-1]))
    return np.array(data, dtype=int)

def load_ways(fname):
    return np.loadtxt(fname).astype(int)

def mirror_invert(x):
    #x = np.concatenate((x, x[:,::-1]), axis=0) # mirror (-> becomes <-)
    x = np.concatenate((x, x==0), axis=0) # flip/invert all
    return np.unique(x, axis=0).astype(int)

# Which rows from m1 are not in m2
def which_not_match(m1, m2):
    # .all(axis=1) compares for each line if all elements are equal
    # .any() compares if there's at least one line the are totally equal
    is_in = [(row == m2).all(axis=1).any() for row in m1] # w in small
    is_in = np.array(is_in)
    return np.where(is_in == False)[0].reshape(-1)

# Possible combinations obtainable with p hyperplanes in h=2
# Recursively calls itself
def sum_votes(p, votes_sum):
    if(p==1):
        return votes_sum
    else:
        votes = []
        for j,row in enumerate(votes_sum):
            #print('\t'*p, p, j, votes_sum[j:].shape)
            vote = row + sum_votes(p-1, votes_sum[j:])
            votes.append(vote)
        return np.concatenate(np.array(votes), axis=0)

def sort_matrix(m):
    m_vec = [''.join(row.astype(str)) for row in m]
    return m[np.argsort(m_vec)]


def combine_hyperplanes(w_p1, p=1):
    n = w_p1.shape[1]
    votes = sum_votes(p=p, votes_sum=w_p1).reshape(-1,n)
    w = np.unique(votes > p/2, axis=0)
    w = np.concatenate((w_p1, w), axis=0)
    w = mirror_invert(w)
    return sort_matrix(w)
