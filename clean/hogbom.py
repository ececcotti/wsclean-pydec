import numpy as np

def deconvolve(residual, model, psf, meta):
	nchan = residual.shape[0]
	npol = residual.shape[1]
	height = residual.shape[2]
	width = residual.shape[3]
	
	print("Start Python deconvolve() function for " + str(width) + " x " + str(height) \
		+ " x " + str(npol) + " x " + str(nchan) + " dataset")
	    
	# multiple channels and polarizations not implemented yet
	if nchan != 1 or npol != 1:
		raise NotImplementedError('number of channels and polarizations must be one')
		
	# in Hogbom cleaning no major cycle is performed
	if meta.mgain != 1: 
		raise Exception('set mgain=1 to use Hogbom algorithm')
		
	# find strength and position of the peak
	peak_idx = np.unravel_index(np.argmax(residual), residual.shape)
	peak = residual[peak_idx]
	print("Peak of " + str(peak) + " Jy found at pixel position " + str(peak_idx[2:]))
	
	
	
	
	
	
