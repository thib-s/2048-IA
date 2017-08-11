import pickle

import os


def save_obj(obj, name):
    try:
        os.mkdir("obj")
    except:
        None
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    try:
        os.mkdir("obj")
    except:
        None
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def display_object(file):
    print (load_obj(file))
