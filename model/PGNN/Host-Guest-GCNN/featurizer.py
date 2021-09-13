import deepchem as dc
from os import listdir
import os
from os.path import isfile, join
import rdkit
from rdkit import Chem
from deepchem.metrics import to_one_hot
from deepchem.feat.mol_graphs import ConvMol
import numpy as np
import pandas as pd
from model import GBGraphConvModel
from deepchem.feat import MolGraphConvFeaturizer


#load Host-guest-dataset
df = pd.read_excel('Dataset/host-guest-dataset.xlsx')
df = df.dropna()
print(df.head())

# read pdb files
pdbs = {}
pdb_files = [f for f in os.listdir("PDB") if isfile(join("PDB", f))]

# Convert PDB to Mol object
for f in pdb_files:
    pdbs.update({f.split('.')[0].replace('-s', ''): rdkit.Chem.rdmolfiles.MolFromPDBFile("PDB" + '/' + f)})

# create a featurizer object
featurizer = dc.feat.ConvMolFeaturizer()

X = []
X_ids = []
one_add = 0 if len(pdbs.keys()) % 2 == 0 else 1
for k in pdbs.keys():
    X_ids.append(k)
    X.append(featurizer.featurize(pdbs[k]))
X = [x[0] for x in X]
X_train_featurized = X[:int(len(X) / 2)]
X_test_featurized = X[int(len(X) / 2) + one_add:]

# get host and guest names
host_names = [i.split('-')[0] for i in X_ids]
guest_names = ['guest-' + (i.split('-')[0].replace('s', '')) for i in X_ids]

# split dataset into test and train
host_names_train = host_names[:int(len(host_names) / 2)]
guest_names_train = guest_names[:int(len(guest_names) / 2)]
host_names_test = host_names[int(len(host_names) / 2) + one_add:]
guest_names_test = guest_names[int(len(guest_names) / 2) + one_add:]

# preparing test, train dataset
x_add_train, x_add_test, y_train, y_test = [], [], [], []
for i in range(len(host_names_train)):
    new_df = df[(df['Host'] == host_names_train[i]) & (df['Guest'] == guest_names_train[i])]
    y_train.append(new_df['EX _H_(kcal/mol)'].to_numpy()[0])
    x_add_train.append(new_df[[c for c in df.columns if ('Etot' not in c) and ('delta' not in c)
                               and ('Ex_difference' not in c) and ('gb_' in c or 'VDWAALS' in c)]].to_numpy()[0])
y_train = np.array(y_train)

for i in range(len(host_names_test)):
    new_df = df[(df['Host'] == host_names_test[i]) & (df['Guest'] == guest_names_test[i])]
    y_test.append(new_df['EX _H_(kcal/mol)'].to_numpy()[0])
    x_add_test.append(new_df[[c for c in df.columns if ('Etot' not in c) and ('delta' not in c)
                              and ('Ex_difference' not in c) and ('gb_' in c or 'VDWAALS' in c)]].to_numpy()[0])
y_test = np.array(y_test)



# preprocessing
x_preprocessed_train, x_preprocessed_test = [], []


## for X train
multiConvMol = ConvMol.agglomerate_mols(X_train_featurized)
x_preprocessed_train = [multiConvMol.get_atom_features(), multiConvMol.deg_slice, np.array(multiConvMol.membership)]
for i in range(1, len(multiConvMol.get_deg_adjacency_lists())):
    x_preprocessed_train.append(multiConvMol.get_deg_adjacency_lists()[i])
x_preprocessed_train.append(np.array(x_add_train))

## for X test
multiConvMol = ConvMol.agglomerate_mols(X_test_featurized)
x_preprocessed_test = [multiConvMol.get_atom_features(), multiConvMol.deg_slice, np.array(multiConvMol.membership)]
for i in range(1, len(multiConvMol.get_deg_adjacency_lists())):
    x_preprocessed_test.append(multiConvMol.get_deg_adjacency_lists()[i])
x_preprocessed_test.append(np.array(x_add_test))

x_train = np.full([14, np.max([v.shape[0] for v in x_preprocessed_train]),
                  np.max([v.shape[1] for v in x_preprocessed_train if len(v.shape) > 1])], 1.123456)


for i,j in enumerate(x_preprocessed_train):
    if len(j.shape) > 1:
        x_train[i][:j.shape[0],:j.shape[1]] = np.array(j)
    else:
        x_train[i][:len(j), :1] = np.array(j).reshape(j.shape[0], 1)
x_train = x_train.reshape([1] + list(x_train.shape))

x_test = np.full([14, np.max([v.shape[0] for v in x_preprocessed_test]),
                  np.max([v.shape[1] for v in x_preprocessed_test if len(v.shape) > 1])], 1.123456)
for i,j in enumerate(x_preprocessed_test):
    if len(j.shape) > 1:
        x_test[i][:j.shape[0],:j.shape[1]] = np.array(j)
    else:
        x_test[i][:len(j), :1] = np.array(j).reshape(j.shape[0], 1)
x_test = x_test.reshape([1] + list(x_test.shape))

#running the model
batch_size = int(len(df) / 2)
model = GBGraphConvModel()
model.compile(loss='mse', optimizer='adam')

model.fit(x_train, y_train.reshape([1, -1]), epochs=100)
input_shapes = [i.shape for i in x_preprocessed_test]
model.evaluate(x_test, y_test.reshape([1, -1]))

np.sqrt(34)
np.sqrt(np.mean((df['EX _H_(kcal/mol)'].to_numpy() - df['gb_delta_H'].to_numpy())**2))