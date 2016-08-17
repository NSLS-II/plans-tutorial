def get_ID_calibration(gapstart,gapstop,gapstep=.2,gapoff=0):
    """
    by LW 04/20/2015
    function to automatically take a ID calibration curve_fit
    calling sequence: get_ID_calibration(gapstart,gapstop,gapstep=.2,gapoff=0)
	gapstart: minimum gap used in calibration (if <5.2, value will be set to 5.2)
	gapstop: maximum gap used in calibration
	gapstep: size of steps between two gap points
	gapoff: offset applied to calculation gap vs. energy from xfuncs.get_Es(gap-gapoff)
	thermal management of Bragg motor is automatic, waiting for cooling <80C between Bragg scans
    writes outputfile with fitted value for the center of the Bragg scan to:  '/home/xf11id/Repos/chxtools/chxtools/X-ray_database/
	changes 03/18/2016: made compatible with python V3 and latest versio of bluesky (working on it!!!)
    """
    import numpy as np
    #import xfuncs as xf
    #from dataportal import DataBroker as db, StepScan as ss, DataMuxer as dm
    import time
    from epics import caput, caget
    from matplotlib import pyplot as plt
    from scipy.optimize import curve_fit
    gaps = np.arange(gapstart, gapstop, gapstep) - gapoff   # not sure this should be '+' or '-' ...
    print('ID calibration will contain the following gaps [mm]: ',gaps)
    xtal_map = {1: 'Si111cryo', 2: 'Si220cryo'}
    pos_sts_pv = 'XF:11IDA-OP{Mono:DCM-Ax:X}Pos-Sts'
    try:
        xtal = xtal_map[caget(pos_sts_pv)]
    except KeyError:
        raise CHX_utilities_Exception('error: trying to do ID gap calibration with no crystal in the beam')
    print('using', xtal, 'for ID gap calibration')
    # create file for writing calibration data:
    fn='id_CHX_IVU20_'+str(time.strftime("%m"))+str(time.strftime("%d"))+str(time.strftime("%Y"))+'.dat'
    fpath='/tmp/'
    # fpath='/home/xf11id/Repos/chxtools/chxtools/X-ray_database/'
    try:
        outFile = open(fpath+fn, 'w')
        outFile.write('% data from measurements '+str(time.strftime("%D"))+'\n')
        outFile.write('% K colkumn is a placeholder! \n')
        outFile.write('% ID gap [mm]     K      E_1 [keV] \n')
        outFile.close()
        print('successfully created outputfile: ',fpath+fn)
    except:
        raise CHX_utilities_Exception('error: could not create output file')
    
    ### do the scanning and data fitting, file writing,....
    t_adjust=0
    center=[]
    E1=[]
    realgap=[]
    detselect(xray_eye1)
    print(gaps)
    MIN_GAP = 5.2
    for i in gaps:
        if i >= MIN_GAP: 
            B_guess=-1.0*xf.get_Bragg(xtal,xf.get_Es(i+gapoff,5)[1])[0]
        else:
            i = MIN_GAP 
            B_guess=-1.0*xf.get_Bragg(xtal,xf.get_Es(i,5)[1])[0]
        if i > 8 and t_adjust == 0:     # adjust acquistion time once while opening the gap (could write something more intelligent in the long run...)
           exptime=caget('XF:11IDA-BI{Bpm:1-Cam:1}cam1:AcquireTime')
           caput('XF:11IDA-BI{Bpm:1-Cam:1}cam1:AcquireTime',2*exptime)
           t_adjust = 1
        print('initial guess: Bragg= ',B_guess,' deg.   ID gap = ',i,' mm')
        es = xf.get_Es(i, 5)[1]
        mirror_stripe_pos = round(caget('XF:11IDA-OP{Mir:HDM-Ax:Y}Mtr.VAL'),1)
        SI_STRIPE = -7.5
        RH_STRIPE = 7.5
        if es < 9.5:
            stripe = SI_STRIPE
        elif es >= 9.5:
            stripe = RH_STRIPE
        yield from bp.abs_set(hdm.y, stripe)
        yield from bp.abs_set(foil_y, 0)  # Put YAG in beam.
        print('moving DCM Bragg angle to:', B_guess ,'deg and ID gap to', i, 'mm')
        yield from bp.abs_set(dcm.b, B_guess)
        yield from bp.abs_set(ivu_gap,i)
        print('hurray, made it up to here!')
        print('about to collect data')
        yield from ascan(dcm.b, float(B_guess-.4), float(B_guess+.4), 60,
                         md={'plan_name': 'ID_calibration',
                             'mirror_stripe': stripe})





def count_saxs(type, fnum=1,  expt= 0.1, acqt = None, att_t = 1,
               save=True, new_pos = False):
    '''By YG at 06/10/2016

        Collecting data by using eiger4M
        type: data acquisition description
        fnum: frame number
        expt: exposure time
        acqt: acquisition period
        att_t: attenuation
        save: save data or not
        new_pos: move to new sample position or not        

    '''
    #RE( count_('alignment', 1, 0.1, 0.1, att_t =  1, save=True, new_pos = False) )
    #RE( count_( 'XPCS_200C_1000 frames_1s', 1000, 1, 1 , att_t =  1, save=True, new_pos = False) )

    if acqt is None:
        acqt=expt
        
    type=type+ ' %d fr X %s exp'%(fnum,expt)
    if att_t!=1:
        type=type+ ' %d fr X %s exp'%(fnum,expt) + 'att_%s'%att_t
        att.set_T ( att_t )  #put atten
        
    RE.md['Measurement']=type
    ##Did not find how to set save
    eiger4m_save = 'XF:11IDB-ES{Det:Eig4M}cam1:SaveFiles'
    caput ( eiger4m_save,save )

    yield from bp.abs_set(eiger4m.cam.num_images, fnum)
    yield from bp.abs_set(eiger4m.cam.acquire_time, expt)
    yield from bp.abs_set(eiger4m.cam.acquire_period, acqt )

    yield from bp.abs_set(eiger4m.cam.array_counter,0)
    yield from YAG_FastSh( yag='off', fs='on' ) #put fast shutter on, yag at empty position
    
    BPMFeed(  xbpm_y= 'on' )
    sleep(3)
    BPMFeed(  xbpm_y= 'on' )
    
    if new_pos:
        yield from bp.abs_set(diff.yh, diff.yh.user_readback.value + 0.05)    
    yield from count( [eiger4m_single])
    #caput( eiger4m_save, False)

    yield from bp.abs_set(eiger4m.cam.num_images, 1)
    yield from bp.abs_set(eiger4m.cam.acquire_period, .01 )
    yield from bp.abs_set(eiger4m.cam.acquire_time, .01)

    


def BPMFeed(  xbpm_y= 'on' ):
    '''put bpm feedback on/off'''
    
    xbpm_y_pos = 'XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP'
    
    if xbpm_y is 'on':        
        caput( xbpm_y_pos, 1 )   
    else:
        caput( xbpm_y_pos, 0 )




    
