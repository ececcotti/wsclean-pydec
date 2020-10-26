import numpy as np
import optparse
import os,sys
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS

o = optparse.OptionParser()
o.set_usage('plot_fits.py [options] *.fits')
o.add_option('--size', dest='size', default="8,6", type="str", help='Size of the output image (default: 8,6)')
o.add_option('--vmin', dest='vmin', default=None, type="float", help='Minimum value of the colormap (default: data minimum)')
o.add_option('--vmax', dest='vmax', default=None, type="float", help='Maximum value of the colormap (default: data maximum)')
o.add_option('--cmap', dest='cmap', default="jet", type="str", help='Colormap (default: jet)')
o.add_option('--cbar_label', dest='cbar_label', default=None, type="str", help='Label of the color bar (default: BUNIT from header)')
o.add_option('--pdf', dest='save_pdf', default=False, action='store_true', help='Save image as pdf')
o.add_option('--png', dest='save_png', default=False, action='store_true', help='Save image as png')
o.add_option('--name', dest='outfile', default=None, type="str", help='Output image name with no extension (default: fits name')
opts,args = o.parse_args(sys.argv[1:])

fitsname = args[0]
hdul = fits.open(fitsname)
hdr = hdul[0].header
data = hdul[0].data[0,0,:,:]
wcs = WCS(hdr,naxis=2)

imsize = np.array(opts.size.split(','), dtype=np.float64)
fig = plt.figure(figsize=(imsize[0],imsize[1]))
ax = fig.add_subplot(1,1,1, projection=wcs)
ra = ax.coords[0]
dec = ax.coords[1]
ra.set_major_formatter('hh:mm:ss')
dec.set_major_formatter('dd:mm:ss')

vmin0 = opts.vmin
if vmin0 == None: vmin0 = np.min(data)
vmax0 = opts.vmax
if vmax0 == None: vmax0 = np.max(data)
cbar_label0 = opts.cbar_label
if cbar_label0 == None: cbar_label0 = hdr['BUNIT']

plt.imshow(data, origin='lower', cmap=opts.cmap,
	aspect='auto', interpolation='none', 
	vmin=vmin0, vmax=vmax0)
plt.colorbar().set_label(cbar_label0, rotation=90)
ax.coords.grid(color='silver', ls='solid', alpha=0.5)
plt.xlabel('Right Ascension (J2000)')
plt.ylabel('Declination (J2000)')

outimage = opts.outfile
if outimage == None: outimage = fitsname.split('.')[0]

plt.title(outimage)
if opts.save_pdf:
	plt.savefig(outimage + '.pdf')
if opts.save_png:
	plt.savefig(outimage + '.png', dpi=200)
plt.show()
plt.close()

