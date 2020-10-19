import numpy as np
import optparse
import os,sys
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS

o = optparse.OptionParser()
o.set_usage('plot_fits.py [options] *.fits')
o.add_option('--pdf', dest='save_pdf', default=False, action='store_true', help='Save image as pdf')
o.add_option('--png', dest='save_png', default=False, action='store_true', help='Save image as png')
o.add_option('--name', dest='outfile', default=None, type=str, help='Output image name with no extension (default = fits file name')
opts,args = o.parse_args(sys.argv[1:])

fitsname = args[0]
hdul = fits.open(fitsname)
hdr = hdul[0].header
data = hdul[0].data[0,0,:,:]
wcs = WCS(hdr,naxis=2)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1, projection=wcs)
ra = ax.coords[0]
dec = ax.coords[1]
ra.set_major_formatter('hh:mm:ss')
dec.set_major_formatter('dd:mm:ss')

plt.imshow(data, origin='lower', cmap='jet',
	aspect='auto', interpolation='none')
plt.colorbar().set_label('Jy/beam', rotation=90)
ax.coords.grid(color='silver', ls='solid', alpha=0.5)
plt.xlabel('Right Ascension (J2000)')
plt.ylabel('Declination (J2000)')

outimage = opts.outfile
if outimage == None: outimage = fitsname.split('.')[0]

plt.title(outimage)
if opts.save_pdf:
	plt.savefig(outimage + '.pdf')
if opts.save_png:
	plt.savefig(outimage + 'png', dpi=200)
plt.show()
plt.close()

