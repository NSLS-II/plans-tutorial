### Theta cuts at various energies

gs.TABLE_COLS = ['fccd_stats1_total','fccd_stats2_total','fccd_stats3_total','fccd_stats4_total'];

gs.PLOT_Y = 'fccd_stats3_total'


def Ecuts():
    
    # get the current positions
    my_HKL = tardis.position
    
    # Dark images
    shclose()
    fccd_set(50,4)
    olog('Dark images #{} @ {:.3f}Hz'.format((db[-1].get('start').get('scan_id')+1), 1./fccd.acquire_time.get()))
    RE(ct())
    fccd_set(50,1)
    shopen()
    
    # Light images
    my_energies = arange(840,860,2)-0.5
    for my_E in my_energies:
         
         MonoClosedLoop()
         sleep(1)
         mov(pgm_en,my_E)
         sleep(2)
         MonoKill()
         #MonoOpenLoopAmpOn()
         
         tardis.calc.energy = (pgm_en.readback.value+5.0)/10000
         tardis.move([my_HKL.h,my_HKL.k,my_HKL.l],wait = True)
         olog('({:.3f} {:.3f} {:.3f}) #{} @ {:.2f}eV, {:.3f}Hz at {:.2f}K, phase {:.3f}mm, mono killed'.format(tardis.position.h,tardis.position.k,tardis.position.l,(db[-1].get('start').get('scan_id')+1), pgm_en.get()[1], 1./fccd.acquire_time.get(), temp.a.value, caget('XF:23ID-ID{EPU:2-Ax:Phase}Pos-I')))
         RE(d2scan(theta,-.4,.4,delta,-.8,.8,40))



