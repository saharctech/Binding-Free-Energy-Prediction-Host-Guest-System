import rdkit
import deepchem as dc
import pandas as pd
import numpy as np
import tensorflow as tf
import sklearn
from deepchem.metrics import to_one_hot
from deepchem.feat.mol_graphs import ConvMol
OPTIMIZER = tf.keras.optimizers.Adam(0.05)
max_epoch = 300
df = pd.read_csv('molecule_parameters.csv')
df.dropna(how='any', inplace=True)
round_number = 1

# Reading PDB files
# Dictionary with complex names as keys and molecule as values
PDBs = {}
from os import listdir
from os.path import isfile, join
mypath = '../dataset'
onlyfiles = [f for f in listdir(mypath) if f not in ('.DS_Store') and f in (df['complex-name'].tolist())]
for f in onlyfiles:
    PDBs.update({f: rdkit.Chem.rdmolfiles.MolFromPDBFile(mypath + '/' + f + '/com_new.pdb')})
for key, value in dict(PDBs).items():
    if value is None:
        del PDBs[key]

# Randomly shuffling the PDBs
import random
l = list(PDBs.items())
random.shuffle(l)
PDBs = dict(l)

# Featurizing
featurizer = dc.feat.ConvMolFeaturizer(per_atom_fragmentation=False)
TRAIN_SET = .7
VAL_SET = .3
PDBs.pop('',None)
X = []
X_ids = []
# one_add = 0 if len(PDBs.keys()) % 2 == 0 else 1
for k in PDBs.keys():
    X_ids.append(k)
    X.append(featurizer.featurize(PDBs[k]))
train_split_index = int(len(X) * TRAIN_SET)
val_split_index = int(len(X) * VAL_SET)
X = [x[0] for x in X]
X_train_featurized = X[:train_split_index]
# X_val_featurized = X[train_split_index: (train_split_index + val_split_index)]
X_val_featurized = X[train_split_index:]
X_test_featurized = X[train_split_index:]

host_names = [i.split('-')[0] for i in X_ids]
# train
host_names_train = host_names[:train_split_index]
# guest_names_train = guest_names[:train_split_index]
# Val
# host_names_val = host_names[train_split_index:(train_split_index + val_split_index)]
# guest_names_val = guest_names[train_split_index:(train_split_index + val_split_index)]
host_names_val = host_names[train_split_index:]
# guest_names_val = guest_names[train_split_index:]
# test
host_names_test = host_names[train_split_index:]
# guest_names_test = guest_names[train_split_index:]


x_add_train, x_add_val, x_add_test, y_train, y_val, y_test = [], [], [], [], [], []
# Train
for i in range(len(host_names_train)):
    new_df = df[(df['complex-name'] == host_names_train[i])]
    y_train.append(new_df['ddg'].to_numpy()[0])
    x_add_train.append(new_df[[c for c in df.columns if ('etot' not in c) and ('delta' not in c) and
                               ('gb-' in c or 'vdwaals' in c)]].to_numpy()[0])
y_train = np.array(y_train)
# Val
for i in range(len(host_names_val)):
    new_df = df[(df['complex-name'] == host_names_val[i])]
    y_val.append(new_df['ddg'].to_numpy()[0])
    x_add_val.append(new_df[[c for c in df.columns if ('etot' not in c) and ('delta' not in c)
                         and ('gb-' in c or 'vdwaals' in c)]].to_numpy()[0])
y_val = np.array(y_val)

# Test
for i in range(len(host_names_test)):
    new_df = df[(df['complex-name'] == host_names_test[i])]
    y_test.append(new_df['ddg'].to_numpy()[0])
    x_add_test.append(new_df[[c for c in df.columns if ('etot' not in c) and ('delta' not in c)
                         and ('gb-' in c or 'vdwaals' in c)]].to_numpy()[0])
y_test = np.array(y_test)



x_preprocessed_train, x_preprocessed_val, x_preprocessed_test = [], [], []

## for X train
multiConvMol = ConvMol.agglomerate_mols(X_train_featurized)
x_preprocessed_train = [multiConvMol.get_atom_features(), multiConvMol.deg_slice, np.array(multiConvMol.membership)]
for i in range(1, len(multiConvMol.get_deg_adjacency_lists())):
    x_preprocessed_train.append(multiConvMol.get_deg_adjacency_lists()[i])
x_preprocessed_train.append(np.array(x_add_train))

## for X val
multiConvMol = ConvMol.agglomerate_mols(X_val_featurized)
x_preprocessed_val = [multiConvMol.get_atom_features(), multiConvMol.deg_slice, np.array(multiConvMol.membership)]
for i in range(1, len(multiConvMol.get_deg_adjacency_lists())):
    x_preprocessed_val.append(multiConvMol.get_deg_adjacency_lists()[i])
x_preprocessed_val.append(np.array(x_add_val))


## for X test
multiConvMol = ConvMol.agglomerate_mols(X_test_featurized)
x_preprocessed_test = [multiConvMol.get_atom_features(), multiConvMol.deg_slice, np.array(multiConvMol.membership)]
for i in range(1, len(multiConvMol.get_deg_adjacency_lists())):
    x_preprocessed_test.append(multiConvMol.get_deg_adjacency_lists()[i])
x_preprocessed_test.append(np.array(x_add_test))

# Train
x_train = np.full([14, np.max([v.shape[0] for v in x_preprocessed_train]),
                  np.max([v.shape[1] for v in x_preprocessed_train if len(v.shape) > 1])], 1.123456)

for i,j in enumerate(x_preprocessed_train):
    if len(j.shape) > 1:
        x_train[i][:j.shape[0],:j.shape[1]] = np.array(j)
    else:
        print(len(j.shape))
        x_train[i][:len(j), :1] = np.array(j).reshape(j.shape[0], 1)
x_train = x_train.reshape([1] + list(x_train.shape))

# Validation
x_val = np.full([14, np.max([v.shape[0] for v in x_preprocessed_val]),
                  np.max([v.shape[1] for v in x_preprocessed_val if len(v.shape) > 1])], 1.123456)
for i,j in enumerate(x_preprocessed_val):
    if len(j.shape) > 1:
        x_val[i][:j.shape[0],:j.shape[1]] = np.array(j)
    else:
        x_val[i][:len(j), :1] = np.array(j).reshape(j.shape[0], 1)
x_val = x_val.reshape([1] + list(x_val.shape))

# Test
x_test = np.full([14, np.max([v.shape[0] for v in x_preprocessed_test]),
                  np.max([v.shape[1] for v in x_preprocessed_test if len(v.shape) > 1])], 1.123456)
for i,j in enumerate(x_preprocessed_test):
    if len(j.shape) > 1:
        x_test[i][:j.shape[0],:j.shape[1]] = np.array(j)
    else:
        x_test[i][:len(j), :1] = np.array(j).reshape(j.shape[0], 1)
x_test = x_test.reshape([1] + list(x_test.shape))

# PGNN model
pgnn_test_accuracy = []
pgnn_train_accuracy = []
## !!!!!!!! important
## !!!!!!!! important
## !!!!!!!! important
## !!!!!!!! important
batch_size = len(host_names_train)
batch_size
# batch_size=10

from deepchem.models.layers import GraphConv, GraphPool, GraphGather
import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.layers import Dense, Input, BatchNormalization, Concatenate
from tensorflow.keras import initializers


class GBGraphConvModel(tf.keras.Model):

    def modify_graphgather(self, batch_size):
        self.readout.batch_size = batch_size
        self.batch_size = batch_size

    def __init__(self, batch_size):
        super(GBGraphConvModel, self).__init__()
        self.input_shapes = None
        self.batch_size = batch_size
        self.gc1 = GraphConv(32, activation_fn=tf.nn.tanh)
        self.batch_norm1 = layers.BatchNormalization()
        self.gp1 = GraphPool()

        self.gc2 = GraphConv(32, activation_fn=tf.nn.tanh)
        self.batch_norm2 = layers.BatchNormalization()
        self.gp2 = GraphPool()

        self.dense1 = layers.Dense(64, activation=tf.nn.tanh)
        self.batch_norm3 = layers.BatchNormalization()
        self.readout = GraphGather(batch_size=self.batch_size, activation_fn=tf.nn.tanh)

        self.dense2 = layers.Dense(1)
        self.dense3 = layers.Dense(1,
                                   kernel_initializer=initializers.Constant(
                                       [.5, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1]),
                                   bias_initializer=initializers.Zeros())

    def call(self, inputs):
        inputs = inputs[0]
        x = []
        #     input_shapes = [[4822, 75], [11, 2], [4822], [1142, 1], [1635, 2], [2042, 3],
        #                    [3, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10]]
        for i in range(len(self.input_shapes)):
            x.append(tf.reshape(inputs[i][inputs[i] != 1.123456], self.input_shapes[i]))
        for i in range(1, len(self.input_shapes)):
            x[i] = tf.cast(x[i], tf.int32)
        x_add = tf.reshape(inputs[13][inputs[13] != 1.123456], [self.batch_size, 15])
        gc1_output = self.gc1(x)
        batch_norm1_output = self.batch_norm1(gc1_output)
        gp1_output = self.gp1([batch_norm1_output] + x[1:])

        gc2_output = self.gc2([gp1_output] + x[1:])
        batch_norm2_output = self.batch_norm1(gc2_output)
        gp2_output = self.gp2([batch_norm2_output] + x[1:])

        dense1_output = self.dense1(gp2_output)
        batch_norm3_output = self.batch_norm3(dense1_output)
        readout_output = self.readout([batch_norm3_output] + x[1:])

        model_var = self.dense2(readout_output)
        binding_affinity = tf.concat([model_var, x_add], axis=1)
        return self.dense3(binding_affinity)


hybrid_model = GBGraphConvModel(train_split_index)
hybrid_model.compile(loss='mse', optimizer= OPTIMIZER)

# Training PGNN model
pgnn_losses, pgnn_val_losses = [], []

val_size = len(y_val)
train_size = len(y_train)

for epoch in range(max_epoch):
    hybrid_model.modify_graphgather(train_size)
    hybrid_model.input_shapes = [i.shape for i in x_preprocessed_train]
    loss = hybrid_model.fit(x_train, y_train.reshape([1, -1]), epochs=1)
#     metric = dc.metrics.Metric(dc.metrics.score_function.rms_score)
    pgnn_losses.append(loss.history['loss'])
    hybrid_model.input_shapes = [i.shape for i in x_preprocessed_val]
    hybrid_model.modify_graphgather(val_size)
    pgnn_val_losses.append(hybrid_model.evaluate(x_val, y_val.reshape([1, -1])))

# Loss per Epoch graph
import matplotlib.pyplot as plt
# f, ax = plt.subplots()
plt.plot(range(len(pgnn_losses)), pgnn_losses, label='train loss')
plt.plot(range(len(pgnn_val_losses)), pgnn_val_losses, label='val loss')
plt.legend(loc='upper right');
plt.xlabel("Epoch")
plt.ylabel("Loss (Kcal/mol)")
plt.savefig('comb_loss.png')

hybrid_model.input_shapes = [i.shape for i in x_preprocessed_test]
hybrid_model.modify_graphgather(len(y_test))
evalu = hybrid_model.evaluate(x_test, y_test.reshape([1, -1]))
pgnn_rmse_test = np.sqrt(evalu)
print(pgnn_rmse_test)
train_loss = pgnn_losses[-1]
import math
train_hybrid_rmse = math.sqrt(train_loss[0])
train_hybrid_rmse
pgnn_test_accuracy.append(pgnn_rmse_test)
pgnn_train_accuracy.append(train_hybrid_rmse)

# Data Driven Model
## !!!!!!!! important
## !!!!!!!! important
## !!!!!!!! important
## !!!!!!!! important
input_shapes = [i.shape for i in x_preprocessed_train]
dd_test_accuracy = []
dd_train_accuracy = []
batch_size = len(host_names_train)
batch_size
from deepchem.models.layers import GraphConv, GraphPool, GraphGather
import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.layers import Dense, Input, BatchNormalization, Concatenate
from tensorflow.keras import initializers


# batch_size = int(len(df) / 2)

class GBGraphConvModel(tf.keras.Model):

    def modify_graphgather(self, batch_size):
        self.readout.batch_size = batch_size
        self.batch_size = batch_size

    def __init__(self, batch_size):
        super(GBGraphConvModel, self).__init__()
        self.input_shapes = None
        self.batch_size = batch_size
        self.gc1 = GraphConv(32, activation_fn=tf.nn.tanh)
        self.batch_norm1 = layers.BatchNormalization()
        self.gp1 = GraphPool()

        self.gc2 = GraphConv(32, activation_fn=tf.nn.tanh)
        self.batch_norm2 = layers.BatchNormalization()
        self.gp2 = GraphPool()

        self.dense1 = layers.Dense(64, activation=tf.nn.tanh)
        self.batch_norm3 = layers.BatchNormalization()
        self.readout = GraphGather(batch_size=self.batch_size, activation_fn=tf.nn.tanh)

        self.dense2 = layers.Dense(1)

    #     self.dense3 = layers.Dense(1,
    #          kernel_initializer=initializers.Constant([.5, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1]),
    #          bias_initializer=initializers.Zeros())

    def call(self, inputs):
        inputs = inputs[0]
        x = []
        #     input_shapes = [[4822, 75], [11, 2], [4822], [1142, 1], [1635, 2], [2042, 3],
        #                    [3, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10]]
        for i in range(len(self.input_shapes)):
            x.append(tf.reshape(inputs[i][inputs[i] != 1.123456], self.input_shapes[i]))
        for i in range(1, len(self.input_shapes)):
            x[i] = tf.cast(x[i], tf.int32)
        x_add = tf.reshape(inputs[13][inputs[13] != 1.123456], [self.batch_size, 15])
        gc1_output = self.gc1(x)
        batch_norm1_output = self.batch_norm1(gc1_output)
        gp1_output = self.gp1([batch_norm1_output] + x[1:])

        gc2_output = self.gc2([gp1_output] + x[1:])
        batch_norm2_output = self.batch_norm1(gc2_output)
        gp2_output = self.gp2([batch_norm2_output] + x[1:])

        dense1_output = self.dense1(gp2_output)
        batch_norm3_output = self.batch_norm3(dense1_output)
        readout_output = self.readout([batch_norm3_output] + x[1:])

        model_var = self.dense2(readout_output)
        #     binding_affinity = tf.concat([model_var, x_add], axis=1)
        return model_var  # self.dense3(binding_affinity)


dd_model = GBGraphConvModel(train_split_index)
dd_model.compile(loss='mse', optimizer='adam')

# Data Driven model training
dd_losses, dd_val_losses = [], []
# max_epoch = 100
val_size = len(y_val)
train_size = len(y_train)

for epoch in range(max_epoch):
    dd_model.modify_graphgather(train_size)
    dd_model.input_shapes = [i.shape for i in x_preprocessed_train]
    loss = dd_model.fit(x_train, y_train.reshape([1, -1]), epochs=1)
#     metric = dc.metrics.Metric(dc.metrics.score_function.rms_score)
    dd_losses.append(loss.history['loss'])
    dd_model.input_shapes = [i.shape for i in x_preprocessed_val]
    dd_model.modify_graphgather(val_size)
    dd_val_losses.append(dd_model.evaluate(x_val, y_val.reshape([1, -1])))

# Data Driven Loss per Epoch chart
import matplotlib.pyplot as plt
# f, ax = plt.subplots()
plt.plot(range(len(dd_losses)), dd_losses, label='train loss')
plt.plot(range(len(dd_val_losses)), dd_val_losses, label='val loss')
plt.legend(loc='upper right');
plt.xlabel("Epoch")
plt.ylabel("Loss (Kcal/mol)")
# plt.ylim(0,100)
plt.savefig('ind_loss.png')

dd_model.input_shapes = [i.shape for i in x_preprocessed_test]
dd_model.modify_graphgather(len(y_test))
test_pgnn_loss = dd_model.evaluate(x_test, y_test.reshape([1, -1]))
dd_rmse_test = np.sqrt(test_pgnn_loss)
# print(dd_rmse_test)
dd_train_loss = dd_losses[-1]
dd_train_loss
import math
train_dd_rmse = math.sqrt(dd_train_loss[0])
train_dd_rmse
dd_test_accuracy.append(dd_rmse_test)
dd_train_accuracy.append(train_dd_rmse)

# Model Comparison
# Test
results_df = pd.DataFrame(np.array([dd_rmse_test,pgnn_rmse_test,train_dd_rmse,train_hybrid_rmse]).reshape(-1, 4),columns=['test-data-driven-rmse', 'test-pgnn-rmse', 'train-data-driven-rmse','train-pgnn-rmse'])
file_name = 'results_r' + round_number + '.csv'
results_df.to_csv(file_name)