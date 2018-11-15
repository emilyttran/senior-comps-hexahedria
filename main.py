import _pickle as pickle
import os
import errno
from midi_to_statematrix import *

import multi_training
import model


def gen_adaptive(m, pcs, times, keep_thoughts=False, name="final"):
    xIpt, xOpt = map(lambda x: numpy.array(x, dtype='int8'), multi_training.getPieceSegment(pcs))
    all_outputs = [xOpt[0]]
    if keep_thoughts:
        all_thoughts = []
    m.start_slow_walk(xIpt[0])
    cons = 1
    for time in range(multi_training.batch_len * times):
        resdata = m.slow_walk_fun(cons)
        nnotes = numpy.sum(resdata[-1][:, 0])
        if nnotes < 2:
            if cons > 1:
                cons = 1
            cons -= 0.02
        else:
            cons += (1 - cons) * 0.3
        all_outputs.append(resdata[-1])
        if keep_thoughts:
            all_thoughts.append(resdata)
    noteStateMatrixToMidi(numpy.array(all_outputs), 'output/' + name)
    if keep_thoughts:
        pickle.dump(all_thoughts, open('output/' + name + '.p', 'wb'))


def fetch_train_thoughts(m, pcs, batches, name="trainthoughts"):
    all_thoughts = []
    for i in range(batches):
        ipt, opt = multi_training.getPieceBatch(pcs)
        thoughts = m.update_thought_fun(ipt, opt)
        all_thoughts.append((ipt, opt, thoughts))
    pickle.dump(all_thoughts, open('output/' + name + '.p', 'wb'))

def create_output_file(name):
    directory_path = "output/" + name
    print(os.path.exists(directory_path))
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def run_training(genre, size):
    name = genre + "_" + str(size)
    create_output_file(name)
    pcs = multi_training.loadPieces(genre)
    m = model.Model([300, 300], [100, 50], dropout=0.5)
    multi_training.trainPiece(m, pcs, 10000, output_name= name)
    gen_adaptive(m, pcs, 10, name=name)
    pickle.dump(m.learned_config, open("path_to_weight_file.p", "wb"))


if __name__ == '__main__':
    run_training("mozart", 20)
#    pcs = multi_training.loadPieces("mozart_sonatas_smaller_subset")
#    m = model.Model([300, 300], [100, 50], dropout=0.5)
#    multi_training.trainPiece(m, pcs, 10000)
#    gen_adaptive(m, pcs, 10, name="composition")
#    pickle.dump(m.learned_config, open("path_to_weight_file.p", "wb"))
