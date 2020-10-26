import numpy as np

def select_psf(psf):
	psf[psf <= 0] = 0
	
	# search main lobe and select its row
	main_idx = np.unravel_index(np.argmax(psf), psf.shape)
	main_val = psf[main_idx]
	psf_row = psf[main_idx[0],:]
	w_notZero = np.where(psf_row > 0)[0]
	w_notZero_peak = np.where(w_notZero == main_idx[1])[0][0]
	
	# search highest exterior lobe
	for i in range(main_idx[1]):
		pos_psf = main_idx[1] + i
		pos_notZero = w_notZero_peak + i
		if pos_psf != w_notZero[pos_notZero]:
			maxlobe_val = max(psf_row[w_notZero[pos_notZero]:])
			maxlobe_idx = np.where(psf_row == maxlobe_val)[0][0]
			break
	
	R_psf = maxlobe_val / main_val
	
	# select the portion of psf with the highest exterior lobe
	for i in range(maxlobe_idx):
		pixel0 = maxlobe_idx + i
		if psf_row[pixel0] == 0: break
		
	pixel_i = int(2*psf_row[1] - pixel0)
	pixel_f = int(pixel_0 + 1)
	sub_psf = psf[pixel_i:pixel_f, pixel_i:pixel_f]
	return sub_psf, R_psf

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
		raise Exception('set -mgain 1 to use Clark algorithm')
		
	# select portion of psf containing only main + maximum exterior sidelobe
	sub_psf, R_psf = select_psf(psf[0,:,:])
	
	# MAJOR CYCLE
	while meta.iteration_number <= meta.max_iterations or max(residual) > meta.final_threshold:
		if meta.iteration_number%(meta.max_iterations/10.) == 0:
			print("-- Starting major iteration " + str(meta.iteration_number))
		
		# find strength and position of the peak
		peak_idx = np.unravel_index(np.argmax(residual), residual.shape)
		peak_val = residual[peak_idx]
		
		# set the threshold for minor cycle
		threshold = peak_val * R_psf
		
		# MINOR CYCLE
		minor_iteration = 0
		residual_minor = residual
		while peak_val >= threshold:
			if meta.iteration_number%(meta.max_iterations/10.) == 0:
				print("Starting minor iteration " + str(minor_iteration) + ", peak=" + str(peak_val) \
					+ ", threshold=" + str(threshold))

			# shift the sub-psf to the peak position and subtract (new residual)
			psf_shift = (peak_idx[2] + height//2, peak_idx[3] + width//2)
			residual_minor = residual_minor - peak_val * meta.gain * np.roll(np.roll(sub_psf, psf_shift[0], axis=1), psf_shift[1], axis=2)
		
			# update partial model and iteration number
			model_partial[peak_idx] += peak_val*meta.gain
			minor_iteration += 1
			
			# new peak value
			peak_idx =  np.unravel_index(np.argmax(residual_minor), residual_minor.shape)
			peak_val = residual_minor[peak_idx]
		
		print("Minor cycles stopped after iteration " + str(minor_iteration) + ", peak=" + str(peak_val))
		
		vis_model_partial
		

	# fill dictionary for wsclean
	result = dict()
	result['residual'] = residual
	result['model'] = model
	result['level'] = peak_val
	result['continue'] = peak_val > meta.final_threshold and meta.iteration_number < meta.max_iterations
    
	print("Finished deconvolve()")
	return result
	
	
	
	
	
