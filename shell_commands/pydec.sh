wsclean -size 1024 1024 -scale 0.8asec -save-first-residual -channels-out 1 -pol i -niter 1 -auto-threshold 3 -gain 0.2  -data-column DATA -python-deconvolution clean/hogbom.py -name hogbom_test sim_field1.MS
