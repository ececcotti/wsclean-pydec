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
	for i in range(maxlobe_idx)
		pixel0 = maxlobe_idx + i
		if psf_row[pixel0] == 0: break
		
	pixel_i = 2*psf_row[1] - pixel0
	pixel_f = pixel_0 + 1
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
	
	
	
