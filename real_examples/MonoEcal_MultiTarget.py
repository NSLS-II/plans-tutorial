## Energy calibration, grating #1

# set the mirror pitch and grating pitch offset first...
# typical values, Mirr = -0.5390, Grt = -0.3530
# DeltaOffset = -1e-3 -> DeltaE ~ +1 eV in the spectrum

# on Ti
mov(es_diag1_y,-97)
caput('XF:23ID1-BI{Diag:6-Cam:1}Stats1:CentroidThreshold',500)
sleep(5)
mov(pgm_en,450)
sleep(2)
caput('XF:23ID1-BI{Diag:6-Cam:1}Stats1:CentroidThreshold',350)
sleep(5)
RE(ascan(pgm_en,455,470,30))

# on Cu
mov(es_diag1_y,-46.5)
mov(pgm_en,925)
sleep(2)
caput('XF:23ID1-BI{Diag:6-Cam:1}Stats1:CentroidThreshold',1500)
sleep(5)
RE(ascan(pgm_en,925,960,35))



## Insert the new diagnostic after the baffle slits

caput(XF:23ID1-BI{Diag:4-FS}Cmd:In-Cmd,1)





