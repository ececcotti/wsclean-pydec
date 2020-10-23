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
		raise Exception('set -mgain 1 to use Clark algorithm')
		
	# select psf main lobe and highest exterior sidelobe
	# CHANGE DATA !!!
	data_all = data
	#plt.imshow(data_all)
	data[data <= 0] = 0
	#plt.imshow(data)
	#plt.colorbar()
	peak_idx = np.unravel_index(np.argmax(data), data.shape)
	peak_data = data[peak_idx[0],:]
	wnotZero = np.where(peak_data > 0)[0]
	wnotZero_peak_idx = np.where(peak_idx[1] == wnotZero)[0]
	notzero = np.nonzero(data)      

	for i in range(peak_idx[1]):
    		pos_image = peak_idx[1] + i
    		pos_wnotZero = wnotZero_peak_idx[0] + i
    		if pos_image != wnotZero[pos_wnotZero]:
        		max2nd = np.max(peak_data[wnotZero[pos_wnotZero]:])
        		w_max2nd = np.where(peak_data == max2nd)[0][0]
        		break

	Rpsf = max2nd / data[peak_idx]
	for i in range(w_max2nd):
    		pos = w_max2nd + i
    		if peak_data[pos] == 0: 
       			break
 
	pos_in = 2*peak_idx[1] - pos
	pos_f = pos +1 
	#plt.plot(peak_data[pos_in:pos_f])

	new_data = data_all[pos_in:pos_f, pos_in:pos_f]
