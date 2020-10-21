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
		raise Exception('set -mgain 1 to use Hogbom algorithm')
		
	while meta.iteration_number < meta.max_iterations:
	
		# find strength and position of the peak
		peak_idx = np.unravel_index(np.argmax(residual), residual.shape)
		peak_val = residual[peak_idx]
		
		# set the threshold
		peak_sub = peak_val - peak_val * meta.gain
		threshold = max(meta.final_threshold, peak_sub)
		if meta.iteration_number%(meta.max_iterations/10.) == 0:
			print("Starting iteration " + str(meta.iteration_number) + ", peak=" + str(peak_val) \
				+ ", threshold=" + str(threshold))
		if peak_val <= threshold: 
			print("Threshold reached")
			break

		# shift the psf to the peak position and subtract (new residual)
		psf_shift = (peak_idx[2] + height//2, peak_idx[3] + width//2)
		residual = residual - peak_val * meta.gain * np.roll(np.roll(psf, psf_shift[0], axis=1), psf_shift[1], axis=2)
		
		# update model and iteration number
		model[peak_idx] += peak_val*meta.gain
		meta.iteration_number += 1
		
	print("Stopped after iteration " + str(meta.iteration_number) + ", peak=" + str(peak_val))

	# fill dictionary for wsclean
	result = dict()
	result['residual'] = residual
	result['model'] = model
	result['level'] = peak_val
	result['continue'] = peak_val > meta.final_threshold and meta.iteration_number < meta.max_iterations
    
	print("Finished deconvolve()")
	return result
		
	
	
	
	
	
	
