# wsclean-pydec
Python deconvolution support for WSClean, which can now execute a python script during each major deconvolution iteration.

## Usage
The Python support in WSClean is called by the parameter `-python-deconvolution <filename>`, 
which runs a custom deconvolution algorithm written in Python.
For example, a full Python deconvolution WSClean run looks like this:
```
wsclean -size 1024 1024 -scale 1amin -niter 1000000 -mgain 0.8 -auto-threshold 5 \
  -python-deconvolution deconvolution-example.py 1052736496-averaged.ms
```

