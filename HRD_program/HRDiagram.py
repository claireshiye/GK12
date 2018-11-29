import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
import math

#matplotlib.interactive(True)

##Solar parameters
L_sun=3.83*10*26 ##J/s
R_sun=6.96*10**8 ##meter
T_sun=5780. ##Kelvin


##Read the star data extracted with online plot digitizer.
HRstars=np.genfromtxt('HRstars.csv',delimiter=',')
xhr=HRstars[:,0]; yhr=HRstars[:,1]
zhr=pow(np.array(yhr)/pow(np.array(xhr)/T_sun,4),0.25)
zhr=12*zhr/min(zhr)

##Read the Sun evolution trajectory data extracted with online plot digitizer
SunEvoldata=np.genfromtxt('SunEvol.csv', delimiter=',')
xse=SunEvoldata[:,0]; yse=SunEvoldata[:,1]

##Generate L and T array for constant radii lines
R=np.array([0.001, 0.01, 0.1, 1., 10., 100., 1000.])
T=np.linspace(1000., 50000., num=50)


##AG's add colorbar function
def addColorbar(
    ax,cmap,
    vmin,vmax,
    label,logflag = 0,
    fontsize=16,cmap_number=0,
    tick_tuple=None):
    if logflag:
        from matplotlib.colors import LogNorm as norm
        ticks = np.linspace(np.log10(vmin),np.log10(vmax),5,endpoint=True)
        tick_labels= [r"$10^{%.1f}$"%tick for tick in ticks]
        ticks = 10**ticks
    else:
        from matplotlib.colors import Normalize as norm
        ticks = np.linspace(vmin,vmax,5,endpoint=True)
        tick_labels= ticks
    
    if tick_tuple is not None:
        ticks,tick_labels = tick_tuple
    
    fig = ax.get_figure()
    ## x,y of bottom left corner, width,height in percentage of figure size
    ## matches the default aspect ratio of matplotlib
    cur_size = fig.get_size_inches()*fig.dpi        

    cur_height = cur_size[1]
    cur_width = cur_size[0]
    offset = 0.00 + cmap_number*(25/cur_width+50/cur_width)

    #ax1 = fig.add_axes([0.95 + offset, 0.125, 25./cur_width, 0.75])
    ax1=fig.add_axes([0.125, 0.91, 0.775, 0.05])

    cb1 = matplotlib.colorbar.ColorbarBase(
        ax1, cmap=cmap,
        #extend='both',
        extendfrac=0.05,
        norm=norm(vmin=vmin,vmax=vmax),
        orientation='horizontal')


    cb1.set_label(label,fontsize=fontsize)

    cb1.set_ticks(ticks)
    cb1.set_ticklabels(tick_labels)
    cb1.ax.tick_params(labelsize=fontsize-2)
    return cb1,ax1


##Main Code!!!
##Plot the background of each frame
#def init():
#    line.set_data([], [])
#    return line,
#
#def animate(i):
#	line.set_data(xse[:i],yse[:i])
#	return line

##First set up the figure, the axis, and the plot element we want to animate
fig=plt.figure()
ax=plt.gca()
line, = ax.plot([],[], '--', lw=2)
ax.set_xlim(2000,50000)
ax.set_ylim(10**-5,10**7)
ax.invert_xaxis()
ax.set_xscale('log')
ax.set_yscale('log')
#ax.locator_params(numticks=5, axis='x')
#ax.xaxis.set_major_locator(plt.MaxNLocator(5))
#minorFormatter = FormatStrFormatter('%d')
#ax.xaxis.set_minor_formatter(minorFormatter)
ax.set_xlabel(r'$Temperature(K)$')
ax.set_ylabel(r'$Luminosity(L/L_{\odot})$')
ax.set_title('HRD')

##Plot the background of each frame
for i in range(len(R)):
    L=pow(T/T_sun, 4)*pow(R[i], 2)
    ax.plot(T, L, '--', c='gray')


#def AddStar(Temp, Lum): 
###Pick a temperature between 3000 and 400000 Kelvin, and a radius between 0.1 and 100 solar mass.
###Calculate the luminosity
#    ax.scatter(Temp, Lum, s=40, marker='*')


def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data(xse[:i],yse[:i])
    return line


def HRD(SE, ADDSTAR, Temperature, Luminosity):
    ##Plot background HR Diagram
    cm = plt.cm.get_cmap('RdYlBu')
    ax.scatter(xhr, yhr, c=xhr, cmap=cm, s=zhr)
    #addColorbar(ax, plt.cm.get_cmap('coolwarm'), min(yhr), max(yhr), label=None,   logflagfontsize=14,cmap_number=-1, tick_tuple=None)
    
    ##Create animation object
    if SE=='yes':
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(xse), interval=150, blit=False  )
        return anim

    if ADDSTAR=='yes':
        thestar=ax.scatter(Temperature, Luminosity, color='purple', s=120, marker='*')
        return thestar

        
    ##Show the animation
    #plt.show()




