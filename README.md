# wsclean-pydec
Python deconvolution support for WSClean, which can now execute a python script during each major deconvolution iteration.

## Usage
***
The Python support in WSClean is called by the parameter `-python-deconvolution <filename>`, 
which runs a custom deconvolution algorithm written in Python.
For example, a full Python deconvolution WSClean run looks like this:
```
wsclean -size 1024 1024 -scale 1amin -niter 1000000 -mgain 0.8 -auto-threshold 5 \
  -python-deconvolution deconvolution-example.py 1052736496-averaged.ms
```

## Python scripts
***
In the `python_script` direcory there are useful scripts (and codes), e.g. to handle fits files.

-  `fix_source_list.py`: it adds a progressive number after the source name if there are more than one source with the same name.

-  `genBlank.py`: it takes in input a template fits file to generate a blank fits (i.e. setting all pixels to zero) with the same template features.

-  `plot_fits.py`: it generates plots of a fits image using WCS coordinates. The output image can be saved in pdf or png format. Other plotting
options can be listed with `python plot_fits.py -h`.
