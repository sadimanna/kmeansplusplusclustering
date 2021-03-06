import sys
import numpy as np
import scipy.io as sio
#import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.svm import SVC

filename = sys.argv[1]
datafile = sio.loadmat(filename)
data = datafile['variable_name']
sizedata=[len(data), len(data[0])]
disp = []
optimal_ks = []
#Determining the optimal number of k with gap statistic method
def gap_statistic(data):
	sizedata = [len(data),len(data[0])]
	SD = []
	gap = []
	for knum in xrange(0,20):
		print knum
		#Clustering original Data
		kmeanspp = KMeans(n_clusters=knum,init = 'k-means++',max_iter = 100,n_jobs = 1)
		kmeanspp.fit(data)
		dispersion = kmeanspp.inertia_
		#Clustering Reference Data
		nrefs = 10
		refDisp = np.zeros(nrefs)
		for nref in xrange(nrefs):
			refdata = np.random.random_sample(tuple(sizedata))
			refkmeans = KMeans(n_clusters=knum,init='k-means++',max_iter=100,n_jobs=1)
			refkmeans.fit(refdata)
			refdisp = refkmeans.inertia_
			refDisp[nref]=np.log(refdisp)
		mean_log_refdisp = np.mean(refDisp)
		gap.append(mean_log_refdisp-np.log(dispersion))
		sd = (sum([(r-m)**2 for r,m in zip(refDisp,[mean_log_refdisp]*nrefs)])/nrefs)**0.5
		SD.append(sd)
	SD = [sd*((1+(1/nrefs))**0.5) for sd in SD]
	opt_k = None
	diff = []
	for i in xrange(len(gap)-1):
		diff = (SD[i+1]-(gap[i+1]-gap[i]))
		if diff>0:
			opt_k = i+10
			break
	if opt_k < 20:
		print opt_k
		return opt_k
	else:
		return 20
	#Here maximum limit is used 20 because the data used while testing this code was not supposed to have more than 20 clusters
	#However it may be changed according to need. Hence the last if-else statement may not be reuired in that case.


ntrials = 50
for ntrial in xrange(ntrials):
	print 'ntrial: ',ntrial
	optimal_ks.append(gap_statistic(data))
#Plotting the Gap curve(Values to be provided accordingly)
#plt.plot(np.linspace(10,19,10,True),gap)
#plt.show()

#The following lines of code were written to test if there are more than one clusters for which optimal number of K is obtained
#Though that should not happen
unique_opt_k = list(set(optimal_ks))
k_count = {}
count_opt_k = 0
second_opt_k = 0
opt_k = 0
for u_o_k in unique_opt_k:
	count = optimal_ks.count(u_o_k)
	k_count[u_o_k]=count
	if count>count_opt_k:
		count_opt_k = count
		opt_k = u_o_k
	elif count==count_opt_k:
		second_opt_k = u_o_k
print opt_k

#Clusterin with optimal number of k

kmeanspp = KMeans(n_clusters = opt_k,init='k-means++',max_iter=100,n_jobs=1)
kmeanspp.fit(data)
centers = kmeanspp.cluster_centers_
clusterlabels = kmeanspp.labels_
print clusterlabels
mdict = {}
mdict['clusterlabels'] = clusterlabels

sio.savemat('clusterlabels.mat',mdict,format = '4',oned_as = 'column')
print 'dan dana dan done...'
