def Thscan_vs_Eph ():

#    my_energies = arange(846,852,1)
    my_energies = arange(843,845,0.5)
    for myEE in my_energies:
        mov(pgm_en,myEE);
        tardis.calc.energy=(pgm_en.readback.value+3)/10000; 
        tardis.move(0.2485,0.2485,0.2475);
        fccd_set(1)
        olog('({:.3f} {:.3f} {:.3f}) #{} @ {:.2f}eV, {:.3f}Hz at {:.2f}K, phase {:.3f}mm'.format(tardis.position.h,tardis.position.k,tardis.position.l,(db[-1].get('start').get('scan_id')+1), pgm_en.get()[1], 1./fccd.acquire_time.get(), temp.a.value, caget('XF:23ID-ID{EPU:2-Ax:Phase}Pos-I')))
        RE(d2scan(theta,-5,5,delta,-10,10,20))
        
        
        

def Thscan_vs_position ():

    #offset = 0.0
    my_pos = arange(-1.0,-0.601,0.02)+8.5+offset        #10 micron steps
    mov(pgm_en,849); tardis.calc.energy=(pgm_en.readback.value+3)/10000; tardis.move(0.2485,0.2485,0.2475);
    fccd_set(0.2)

    for pos in my_pos:
        mov(sx,pos);       
        olog('({:.3f} {:.3f} {:.3f}) #{} @ {:.2f}eV, {:.3f}Hz at {:.2f}K, phase {:.3f}mm'.format(tardis.position.h,tardis.position.k,tardis.position.l,(db[-1].get('start').get('scan_id')+1), pgm_en.get()[1], 1./fccd.acquire_time.get(), temp.a.value, caget('XF:23ID-ID{EPU:2-Ax:Phase}Pos-I')))
#        RE(d2scan(theta,-5,5,delta,-10,10,10))

#        RE(ct())
        
#        tardis.move(0.2485,0.2485,0.2475);
#        mov(sx,7.9); mov(sy,-0.15)
#        XPCS_single ()       
        



def Temperature_macro ():
    
#    my_Temp = [20,40,60,80,100]
    my_Temp = arange(20,210,20)
    for Temp in my_Temp:
        temp_sp.setpoint.put(Temp)
        sleep(300)
        mov(sx,8.61)
        #Position_scan ()
        Thscan_vs_position ()
        
        
        
def Escan_vs_position ():

#    offset = 0.0
    my_pos = arange(-1.1,-0.701,0.05)+8.5+offset            #50 microns steps
    for pos in my_pos:
        mov(sx,pos);
        mov(pgm_en,849); tardis.calc.energy=(pgm_en.readback.value+3)/10000; tardis.move(0.2485,0.2485,0.2475);
        fccd_set(1)
#        olog('({:.3f} {:.3f} {:.3f}) #{} @ {:.2f}eV, {:.3f}Hz at {:.2f}K, phase {:.3f}mm'.format(tardis.position.h,tardis.position.k,tardis.position.l,(db[-1].get('start').get('scan_id')+1), pgm_en.get()[1], 1./fccd.acquire_time.get(), temp.a.value, caget('XF:23ID-ID{EPU:2-Ax:Phase}Pos-I')))
        
        movr(gamma, 10);
        RE(ascan(pgm_en,840,860,40));
        movr(gamma,-10);



def Position_scan_peak ():

#    offset = 0.0
    mov(sx,8.5+offset)
    mov(pgm_en,849); tardis.calc.energy=(pgm_en.readback.value+3)/10000; tardis.move(0.2485,0.2485,0.2475);
    fccd_set(0.5)
    olog('({:.3f} {:.3f} {:.3f}) #{} @ {:.2f}eV, {:.3f}Hz at {:.2f}K, phase {:.3f}mm'.format(tardis.position.h,tardis.position.k,tardis.position.l,(db[-1].get('start').get('scan_id')+1), pgm_en.get()[1], 1./fccd.acquire_time.get(), temp.a.value, caget('XF:23ID-ID{EPU:2-Ax:Phase}Pos-I')))
    RE(dscan(sx,-1.1,-0.3,80))      #10 micron steps


def Position_scan_XAS ():

    #offset = 0.0
    mov(pgm_en,850.5); tardis.calc.energy=(pgm_en.readback.value+3)/10000; tardis.move(0.2485,0.2485,0.2475);
    fccd_set(0.5)
    olog('({:.3f} {:.3f} {:.3f}) #{} @ {:.2f}eV, {:.3f}Hz at {:.2f}K, phase {:.3f}mm'.format(tardis.position.h,tardis.position.k,tardis.position.l,(db[-1].get('start').get('scan_id')+1), pgm_en.get()[1], 1./fccd.acquire_time.get(), temp.a.value, caget('XF:23ID-ID{EPU:2-Ax:Phase}Pos-I')))
    movr(gamma, 10);
    RE(ascan(sx,8.5+offset-1.1,8.5+offset-0.6,50))      #10 micron steps
    movr(gamma,-10);















def XPCS_single ():

    #offset=0.0
    mov(sx,7.8+offset)
    
    shclose()
    fccd_set(0.5,30)
    olog('Dark images #{} @ {:.3f}Hz'.format((db[-1].get('start').get('scan_id')+1), 1./fccd.acquire_time.get()))
    RE(ct())
    shopen()
    
    fccd_set(0.5,900)
    olog('({:.3f} {:.3f} {:.3f}) #{} @ {:.2f}eV, {:.3f}Hz at {:.2f}K, phase {:.3f}mm, mono active'.format(tardis.position.h,tardis.position.k,tardis.position.l,(db[-1].get('start').get('scan_id')+1), pgm_en.get()[1], 1./fccd.acquire_time.get(), temp.a.value, caget('XF:23ID-ID{EPU:2-Ax:Phase}Pos-I'))); RE(ct())
    
    shclose()
    fccd_set(0.5,30)
    olog('Dark images #{} @ {:.3f}Hz'.format((db[-1].get('start').get('scan_id')+1), 1./fccd.acquire_time.get()))
    RE(ct())
    shopen()














#Scans to run overnight

#Position_scan_XAS ()
# ---> update offset in macros above
#offset=0.5; Thscan_vs_position (); XPCS_single ()
#temp_sp.setpoint.put(40); mov(sx,7.4)








def Cooling_down ():

#    temp_sp.setpoint.put(180); mov(sx,7.8+0.5); sleep(240); 
#    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10))

#    temp_sp.setpoint.put(160); mov(sx,7.8+0.4); sleep(180);
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    temp_sp.setpoint.put(140); mov(sx,7.8+0.36); sleep(180);
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    temp_sp.setpoint.put(120); mov(sx,7.8+0.22); sleep(180);
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    temp_sp.setpoint.put(100); mov(sx,7.8+0.14); sleep(180);
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    temp_sp.setpoint.put(80); mov(sx,7.8+0.07); sleep(180); 
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    temp_sp.setpoint.put(60); mov(sx,7.8+0.03); sleep(180);
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    temp_sp.setpoint.put(40); mov(sx,7.8+0.01); sleep(180);
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    temp_sp.setpoint.put(20); mov(sx,7.8+0.0); sleep(180);
    fccd_set(0.2); RE(d2scan(theta,-5,5,delta,-10,10,10));

    closesh();



