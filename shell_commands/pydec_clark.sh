wsclean -size 1024 1024 -scale 0.8asec -save-first-residual -channels-out 1 -pol i -niter 20 -auto-threshold 1 -gain 0.1 -data-column DATA -python-deconvolution clean/clark.py -name clark_test sim_field1.MS
