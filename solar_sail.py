#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os 
import sys
import seaborn as sns
import matplotlib.ticker as mticker

c = 299792458
s2yr = 3600*24*365.25
ly = c*s2yr; 
rad2deg = 180/np.pi
L = 3.83e26 #Sun's luminosity

npts = 1000000
step = 1000; # TRY TO IMPROVE RESOLUTION

AU  = float(input("\nLaunch distance from Sun in AU [e.g. 1 for Earth orbit]?  "))
d = float(input("Distance to travel in light-years [e.g. 4.22 for Proxima Centauri]? "))
m = float(input("Total mass of sail + payload in kg? "))
A = float(input("Area of sail in metre squared [e.g. 1e6]? "))
b = float(input("Albedo of sail [b=0 to 1,totally absorbant to totally reflective]? ")) 
while b < 0  or b > 1:
    b = float(input("Albedo of sail [b=0 to 1,totally absorbant to totally reflective]? ")) 

R = d*c*s2yr
t = R**4*np.pi*m*c/(12*L*A)
gamma = 1
t =0; v= 0;
AU2m= 1.5e11
r = AU*AU2m
a_0 = L*A*b/(2*np.pi*gamma*m*c*r**2)
r_0 = r

array = [];  # FOR PLOT

for i in range(npts*step):
    dt = float(i)/step  # MUCH QUICKER AND FINE REOLUTION AT START (~ s), WHERE IT'S NEEDED
    #dt = float(npts)/step
    a = L*A*b/(2*np.pi*gamma*m*c*r**2)
    v = v+a*dt
    gamma = (1-(v/c)**2)**-0.5
    r = r+(v*dt)
    t = t+dt

    array.append(t); array.append(a); array.append(v);array.append(r);# FOR PLOT

    if r>R:
         break

print("-------------------------------------------------------------------------------------------")
print("   For A = %1.1e m^2, , b = %1.1f, m = %1.1f kg, launching from %1.1f AU, initial acc = %1.2f m/s^2 " %(A,b,m,AU,a_0))
print("   To travel %1.3f ly [%1.3e m] takes t = %1.1f yr [%1.2e s],\n    where final a = %1.3e m/s^2 and v = %1.0f km/s [%1.4fc]" %(r/ly,r,t/s2yr,t,a,v*1e-3,v/c))
print("-------------------------------------------------------------------------------------------")

ARR = np.reshape(array,(-1, 4)); 

plt.rcParams.update({'font.size': 12})  
fig, (ax1, ax2,ax3) = plt.subplots(1, 3, figsize=(15, 5)) 
plt.setp(ax1.spines.values(), linewidth=2)

ax1.plot(ARR[:,0]/s2yr, ARR[:,1], '-', linewidth=3, color='b')
ax1.set_yscale('log');ax1.set_xscale('log')
def update_ticks(z, pos):
    if z ==1:
        return '1 '
    elif z >1 and z <1000:
        return '%d' %(z)
    elif z < 1 and z > 0.001:
        return z
    else:
        return  '10$^{%1.0f}$' %(np.log10(z))  # THIS WORKED!! AND ALL THAT SHITE THAT WAS ONLINE

ax1.xaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
ax1.set_xlabel('Time, $t$ [years]'); ax1.set_ylabel('Acceleration, $a$ [m s$^{-2}$]')
ax1.text(10**-10,10**-6,"$m$ = %1.0f kg, $A$ = 10$^%d$ m$^2$" %(m,np.log10(A)),fontsize = 12)
ax1.text(10**-10,10**-7,"$r_i$ = %1.0f AU, gives" %(AU),fontsize = 12)  
ax1.text(10**-10,10**-8,"$a_i$ = %1.2f m s$^{-2}$" %(a_0),fontsize = 12)
ax1.text(10**-10,10**-9,"$v_f$ = %1.0f km s$^{-1}$ [%1.4f$c$]" %(v*1e-3,v/c),fontsize = 12)
ax1.text(10**-10,10**-10,"$t$ = %1.0f yr for %1.2f ly" %(t/s2yr,r/ly),fontsize = 12)

plt.setp(ax2.spines.values(), linewidth=2)
ax2.plot(ARR[:,0]/s2yr, ARR[:,2]*1e-3, '-', linewidth=3, color='g')
ax2.set_yscale('log');ax2.set_xscale('log')

ax2.xaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
ax2.set_xlabel('Time, $t$ [years]'); ax2.set_ylabel('Velocity, $v$ [km s$^{-1}$]')

plt.setp(ax3.spines.values(), linewidth=2)
ax3.plot(ARR[:,0]/s2yr, ARR[:,3]/ly, '-', linewidth=3, color='r')
ax3.set_yscale('log');ax3.set_xscale('log')

ax3.xaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
ax3.set_xlabel('Time, $t$ [years]'); ax3.set_ylabel('Distance, $d$ [light-years]')

plt.tight_layout(pad=2.0)
plot = "sail_AU=%1.1f_d=%1.2f_ly_m=%1.1f_kg_A=%1.2e_m2" %(AU,d,m,A); png = "%s.png" % (plot)
#plt.savefig(png);  print("Plot written to", png);
plt.show()

