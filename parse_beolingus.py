import pickle
import json

def beolingus_as_list(file):
    lines = []
    with open(file, mode='r', encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                lines.append(line)
    return lines


lines = beolingus_as_list('data/de-en.txt')


def split_beolingus(lines):
    beo_dict = {}
    for i, line in enumerate(lines):
        i += 1
        line_dict = {}
        line = line.split('::')
        german = line[0]
        english = line[1]
        german = german.split('|')
        english = english.split('|')
        # if len(german) != len(english):
        #    print(line)
        for e, l in enumerate(german):
            line_dict[german[e]] = english[e]
        beo_dict[i] = line_dict
    return beo_dict


beo_dict = split_beolingus(lines)


def write_beolingus(beo_dict):
    file=open('beolingus_output.txt','w', encoding="utf-8")
    for k, v in beo_dict.items():
        file.write(str(k)+str(v)+"\n")


write_beolingus(beo_dict)


def serialize_beolingus(pickled_beolingus):
    with open('beolingus_serialized.txt','wb') as file:
        file.write(pickled_beolingus)


pickled_beolingus=pickle.dumps(beo_dict)
serialize_beolingus(pickled_beolingus)


def load_beolingus(pickled_beolingus):
    file = open('beolingus_unserialized.txt', 'w', encoding="utf-8")
    unpickled_beolingus = pickle.load(open(pickled_beolingus, 'rb'))
    file.write(str(unpickled_beolingus))


load_beolingus('beolingus_serialized.txt')


# counter = 0
# for k, v in beo_dict.items():
#     if counter < 10:
#         (k, v)
#     counter += 1
