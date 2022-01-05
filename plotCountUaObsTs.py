#!/usr/bin/python

import traceback
import os
import sys
import re
import argparse

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates  as mdates 
import numpy as np
import datetime


def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x


def countts(countfile, avgwin, outputfile):

    SYNOPZ,SYNOPZDATES= np.loadtxt(countfile+"/count_SYNOP_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    SHIPZ,SHIPZDATES= np.loadtxt(countfile+"/count_SHIP_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    SHIPU,SHIPUDATES= np.loadtxt(countfile+"/count_SHIP_u10m_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    SHIPV,SHIPUDATES= np.loadtxt(countfile+"/count_SHIP_v10m_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    BUOYZ,BUOYZDATES= np.loadtxt(countfile+"/count_BUOY_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    AIREPT,AIREPTDATES= np.loadtxt(countfile+"/count_AIREP_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    AIREPU,AIREPUDATES= np.loadtxt(countfile+"/count_AIREP_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    AIREPV,AIREPVDATES= np.loadtxt(countfile+"/count_AIREP_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    AMDARU,AMDARUDATES= np.loadtxt(countfile+"/count_AMDAR_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    AMDARV,AMDARVDATES= np.loadtxt(countfile+"/count_AMDAR_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    AMDART,AMDARTDATES= np.loadtxt(countfile+"/count_AMDAR_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    EAMDART,EAMDARTDATES= np.loadtxt(countfile+"/count_EAMDAR_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    EAMDARU,EAMDARUDATES= np.loadtxt(countfile+"/count_EAMDAR_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    EAMDARV,EAMDARVDATES= np.loadtxt(countfile+"/count_EAMDAR_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    PILOTU,PILOTUDATES= np.loadtxt(countfile+"/count_PILOT_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    PILOTV,PILOTVDATES= np.loadtxt(countfile+"/count_PILOT_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    TEMPU,TEMPUDATES= np.loadtxt(countfile+"/count_TEMP_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    TEMPV,TEMPVDATES= np.loadtxt(countfile+"/count_TEMP_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    TEMPT,TEMPTDATES= np.loadtxt(countfile+"/count_TEMP_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    TEMPQ,TEMPQDATES= np.loadtxt(countfile+"/count_TEMP_q_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    AMSUABT,AMSUABTDATES= np.loadtxt(countfile+"/count_AMSUA_bt_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    MHSBT,MHSBTDATES= np.loadtxt(countfile+"/count_MHS_bt_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    SYNOPZ_AVG=movingaverage(SYNOPZ, avgwin)

    SHIPZ_AVG=movingaverage(SHIPZ, avgwin)
    SHIPU_AVG=movingaverage(SHIPU, avgwin)
    SHIPV_AVG=movingaverage(SHIPV, avgwin)

    BUOYZ_AVG=movingaverage(BUOYZ, avgwin)

    AIREPT_AVG=movingaverage(AIREPT, avgwin)
    AIREPU_AVG=movingaverage(AIREPU, avgwin)
    AIREPV_AVG=movingaverage(AIREPV, avgwin)

    AMDART_AVG=movingaverage(AMDART, avgwin)
    AMDARU_AVG=movingaverage(AMDARU, avgwin)
    AMDARV_AVG=movingaverage(AMDARV, avgwin)

    EAMDART_AVG=movingaverage(EAMDART, avgwin)
    EAMDARU_AVG=movingaverage(EAMDARU, avgwin)
    EAMDARV_AVG=movingaverage(EAMDARV, avgwin)

    PILOTU_AVG=movingaverage(PILOTU, avgwin)
    PILOTV_AVG=movingaverage(PILOTV, avgwin)

    TEMPU_AVG=movingaverage(TEMPU, avgwin)
    TEMPV_AVG=movingaverage(TEMPV, avgwin)
    TEMPT_AVG=movingaverage(TEMPT, avgwin)
    TEMPQ_AVG=movingaverage(TEMPQ, avgwin)

    AMSUABT_AVG=movingaverage(AMSUABT, avgwin)
    MHSBT_AVG=movingaverage(MHSBT, avgwin)

    fig = plt.figure(figsize=(8.27,1.8))
    ax = fig.add_subplot(111)

    avglw=3
    totlw=3
    ptsiz=0.5

    plt.plot_date(x=SYNOPZDATES,y=(SYNOPZ_AVG+SHIPZ_AVG+SHIPU_AVG+SHIPV_AVG),fmt='-',color='red',label='SYNOP',linewidth=avglw)
    plt.plot_date(x=BUOYZDATES,y=BUOYZ_AVG,fmt='-',color='orange',label='BUOY',linewidth=avglw)
    plt.plot_date(x=AIREPTDATES,y=(AIREPT_AVG+AIREPU_AVG+AIREPV_AVG+AMDART_AVG+AMDARU_AVG+AMDARV_AVG+EAMDART_AVG+EAMDARU_AVG+EAMDARV_AVG),fmt='-',color='blue',label='AIREP',linewidth=avglw)
    plt.plot_date(x=TEMPTDATES,y=(TEMPT_AVG+TEMPU_AVG+TEMPV_AVG+TEMPQ_AVG),fmt='-',color='olive',label='TEMP',linewidth=avglw)
    plt.plot_date(x=PILOTUDATES,y=(PILOTU_AVG+PILOTV_AVG),fmt='-',color='purple',label='PILOT',linewidth=avglw)
    plt.plot_date(x=AMSUABTDATES,y=(AMSUABT_AVG),fmt='-',color='green',label='AMSUA',linewidth=avglw)
    plt.plot_date(x=MHSBTDATES,y=(MHSBT_AVG),fmt='-',color='black',label='MHS',linewidth=avglw)

    plt.legend(loc='upper left',prop={'size':8},labelspacing=0,fancybox=False, frameon=False, ncol=7)

    #plt.title('3DVAR surface pressure observations')
    #plt.xlabel('Year',fontsize=10)
    plt.xlabel('',fontsize=10)
    #plt.ylabel('Number of observations',fontsize=10)

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    ax.set_yscale("log", nonposx='clip')
    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    ax.yaxis.grid() #vertical lines
    ax.xaxis.grid() #horizontal lines

    dfmt = mdates.DateFormatter('%y')

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(10)

    ax.grid('on')
    dfmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(dfmt)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    # ax.xaxis.set_minor_locator(mdates.HourLocator(0,25,12))

    #fig.autofmt_xdate()

    ax.set_xlim([datetime.date(2013,12,11), datetime.date(2013,12,13)])
#    ax.set_ylim(1e0, 9e3)

    #fig.autofmt_xdate()

    plt.savefig(outputfile,format='png')

def main(argv):

  parser = argparse.ArgumentParser(description='plot observation count time-series')

  parser.add_argument('--version', action='version', version='%(prog)s 1.0')

  parser.add_argument("-c", "--count-files", dest="cfile", required=True,
                    help="CTRL experiment count directory", metavar="EXTR-DIR", type=extant_file)

  parser.add_argument("-a", "--avg-win", dest="awin", required=False,
                    help="averaging window [days]", metavar="AVG-WIN", type=int, default=1)

  parser.add_argument("-o", "--output", dest="ofile", required=False,
                    help="output PNG file", metavar="OUTPUT-PNG", default="out.png")

  args = parser.parse_args()


  print(args)

  countfile=args.cfile
  avgwin=args.awin
  outputfile=args.ofile

  try:
      countts(countfile, avgwin, outputfile,)
  except Exception as err:
      print str(err)
      traceback.format_exc()

if __name__ == "__main__":
   main(sys.argv[1:])


