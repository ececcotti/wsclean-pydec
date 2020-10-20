import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

hdul = fits.open('sim_field1-MS-MFS-residual.fits', mode='update')
data = hdul[0].data

# set all data to zero to generate blank image
data[0,0,:,:] = 0.0
data[0,0,0,0] = 1e-20

outfile = 'blank_field.fits'
print 'Generate blank_field.fits as blank image'
hdul.writeto('blank_field.fits')

hdul.close()

