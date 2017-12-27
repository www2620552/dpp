import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from scipy.spatial.distance import pdist, squareform

import sampler.dpp as dpp
import sampler.mcdpp as mcdpp
import sampler.utils as utils

# currently only support cpu mode
flag_gpu = False

# Construct kernel matrix
Ngrid = 100
X = np.mgrid[-2:2:4./Ngrid, -2:2:4./Ngrid].reshape(2,Ngrid**2).transpose()
pairwise_dists = squareform(pdist(X, 'euclidean'))
L = np.exp(-pairwise_dists ** 2 / 0.5 ** 2)

# Get eigendecomposition of kernel matrix
D, V = utils.get_eig(L, flag_gpu=flag_gpu)

# Samples and plot from unif and standard DPPs
dpp_smpl  = dpp.sample(D, V, flag_gpu=flag_gpu)
mcdpp_smpl = mcdpp.sample(L, 20000, flag_gpu=flag_gpu)
unif_smpl = np.random.permutation(len(X))[:len(dpp_smpl)]

plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.plot(X[unif_smpl, 0], X[unif_smpl, 1],'r.',)
plt.title('Unif')

plt.subplot(1,3,2)
plt.plot(X[dpp_smpl, 0], X[dpp_smpl, 1],'b.',)
plt.title('DPP')

plt.subplot(1,3,3)
plt.plot(X[mcdpp_smpl, 0], X[mcdpp_smpl, 1],'g.',)
plt.title('DPP-MC')

plt.savefig('fig/unif-dpp-mcdpp', bbox_inches='tight')


# Samples and plot from unif and k-DPPs
k = 100
E = utils.get_sympoly(D, k, flag_gpu=flag_gpu)

# Samples and plot from unif and standard DPPs
unif_smpl = np.random.permutation(len(X))[:k]
dpp_smpl  = dpp.sample(D, V, E=E, k=k, flag_gpu=flag_gpu)
mcdpp_sample = mcdpp.sample(L, 20000, k=k, flag_gpu=flag_gpu)

plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.plot(X[unif_smpl, 0], X[unif_smpl, 1],'r.',)
plt.title('Unif')

plt.subplot(1,3,2)
plt.plot(X[dpp_smpl, 0], X[dpp_smpl, 1],'b.',)
plt.title('kDPP')

plt.subplot(1,3,3)
plt.plot(X[dpp_smpl, 0], X[dpp_smpl, 1],'g.',)
plt.title('kDPP-MC')

plt.savefig('fig/unif-kdpp-mckdpp', bbox_inches='tight')


