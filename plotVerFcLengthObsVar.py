#!/usr/bin/python

import traceback
import os
import sys
import re
import argparse

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates  as mdates 
import numpy as np
import datetime

def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x

def verfc (ctrlfile, exptfile, obstype, obsvar, outputfile):

    CVERHOUR,COBSCOUNT,COBSAVG,COBSSD,COBSVAR,COBSRMS= np.loadtxt(ctrlfile+"/obver_"+obstype+"_"+obsvar+".txt", unpack=True)

    if exptfile != None :  
        EVERHOUR,EOBSEOUNT,EOBSAVG,EOBSSD,EOBSVAR,EOBSRMS= np.loadtxt(exptfile+"/obver_"+obstype+"_"+obsvar+".txt", unpack=True)

    fig = plt.figure(figsize=(8.27,2.4))
    ax = fig.add_subplot(111)

    if exptfile != None :  
        plt.plot(CVERHOUR,COBSAVG,linestyle='--',color='red',label='CTRL Bias',linewidth=2)
        plt.plot(CVERHOUR,COBSRMS,linestyle='-',color='red',label='CTRL RMS',linewidth=2)
        plt.plot(EVERHOUR,EOBSAVG,linestyle='--',color='blue',label='EXPT Bias',linewidth=2)
        plt.plot(EVERHOUR,EOBSRMS,linestyle='-',color='blue',label='EXPT RMS',linewidth=2)
    else :
        plt.plot(CVERHOUR,COBSAVG,linestyle='--',color='red',label='Bias',linewidth=2)
        plt.plot(CVERHOUR,COBSRMS,linestyle='-',color='red',label='RMS',linewidth=2)

    plt.axhline(y=0.0, color='k', linestyle='-')

    plt.legend(loc='upper left',prop={'size':10},labelspacing=0,title="",frameon=False, fancybox=False, ncol=2)

    #plt.title('Mean O-B, O-A: OBS geopotential')

    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    ax.yaxis.grid() #vertical lines
    ax.xaxis.grid() #horizontal lines

    ax.set_xlabel('Forecast length [h]',fontsize=10)
    if obsvar == "z" :
        ylabelstring="[m]"
    elif obsvar == "t" :
        ylabelstring="[K]"
    else :
        ylabelstring="[]"

    ax.set_ylabel(ylabelstring,fontsize=10)

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    major_xticks = np.arange(   0,  51,  6)
    minor_xticks = np.arange(   0,  51,  1)
    ax.set_xticks(major_xticks)                                                       
    ax.set_xticks(minor_xticks, minor=True)                                           

#    major_yticks = np.arange(-250, 450, 100)
#    minor_yticks = np.arange(-250, 450,  20)
#    ax.set_yticks(major_yticks)                                                       
#    ax.set_yticks(minor_yticks, minor=True)                                           
# 
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(10)

    ax.grid('on')

    ax.set_xlim(  0, 51)
#    ax.set_ylim(-250, 420)

    plt.savefig(outputfile,format='png')

def main(argv):

  parser = argparse.ArgumentParser(description='plot forecast verification')

  parser.add_argument('--version', action='version', version='%(prog)s 1.0')

  parser.add_argument("-c", "--ctrl-files", dest="cfile", required=True,  help="CTRL experiment count directory", metavar="CTRL-DIR", type=extant_file)

  parser.add_argument("-e", "--expt-files", dest="efile", required=False, help="EXPT experiment count directory", metavar="EXPT-DIR", type=extant_file)

  parser.add_argument("-t", "--obs-type",   dest="otype", required=False, help="obs type: SYNOP/BUOY/SHIP", metavar="OBS-TYPE", default="SYNOP")

  parser.add_argument("-v", "--obs-var",    dest="vtype", required=False, help="obs var: Z", metavar="OBS-VAR", default="z")

  parser.add_argument("-o", "--output",     dest="ofile",  required=False, help="output PNG file", metavar="OUTPUT-PNG", default="out.png")

  args = parser.parse_args()

  print(args)

  ctrlfile=args.cfile
  exptfile=args.efile
  obstype=args.otype
  obsvar=args.vtype
  outputfile=args.ofile

  try:
      verfc(ctrlfile, exptfile, obstype, obsvar, outputfile,)
  except Exception as err:
      print err
      traceback.format_exc()

if __name__ == "__main__":
   main(sys.argv[1:])

