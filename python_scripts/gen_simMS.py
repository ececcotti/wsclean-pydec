import numpy as np
import optparse
import os,sys
from casacore import tables as tb

o = optparse.OptionParser()
o.set_usage('gen_simMS.py [options] *.MS')
o.add_option('--sigma', dest='sigma', default="1", type="float", help='Visibility noise in Jy (default: 1 Jy)')
o.add_option('--data_column', dest='data_column', default="DATA", type="str", help='Data column where noise will be added (default: DATA)')
o.add_option('--parset', dest='parset', default=None, type="str", help="Parset file to generate the simulated MS with DPPP")
opts,args = o.parse_args(sys.argv[1:])

os.system('DPPP ' + opts.parset)

filename = args[0]

t = tb.table(filename, readonly=False)
data = t.getcol(opts.data_column.upper())

nrows = data.shape[0]
nchannel = data.shape[1]
npol = data.shape[2]

# generate noise per channel and polarization
print "Generating noise"
noise = np.zeros(data.shape, dtype=np.complex128)
for i in range(nchannel):
	for j in range(npol):
		noise[:, i, j] = np.random.multivariate_normal(np.zeros(2), 0.5*opts.sigma*np.eye(2), size=nrows).view(np.complex128)[:, 0]

# add noise to data and overwrite noiseless data
print "Updating data column in the MS file"
data += noise
t.putcol(opts.data_column.upper(), data)
t.close()


		

