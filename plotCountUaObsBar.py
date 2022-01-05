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

def countbar(ctrlfile, exptfile, plottype, outputfile):

    CSYNOPZ,CSYNOPZDATES= np.loadtxt(ctrlfile+"/count_SYNOP_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CSHIPZ,CSHIPZDATES= np.loadtxt(ctrlfile+"/count_SHIP_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CSHIPU,CSHIPUDATES= np.loadtxt(ctrlfile+"/count_SHIP_u10m_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CSHIPV,CSHIPUDATES= np.loadtxt(ctrlfile+"/count_SHIP_v10m_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CBUOYZ,CBUOYZDATES= np.loadtxt(ctrlfile+"/count_BUOY_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CAIREPT,CAIREPTDATES= np.loadtxt(ctrlfile+"/count_AIREP_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CAIREPU,CAIREPUDATES= np.loadtxt(ctrlfile+"/count_AIREP_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CAIREPV,CAIREPVDATES= np.loadtxt(ctrlfile+"/count_AIREP_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CAMDARU,CAMDARUDATES= np.loadtxt(ctrlfile+"/count_AMDAR_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CAMDARV,CAMDARVDATES= np.loadtxt(ctrlfile+"/count_AMDAR_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CAMDART,CAMDARTDATES= np.loadtxt(ctrlfile+"/count_AMDAR_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CEAMDART,CEAMDARTDATES= np.loadtxt(ctrlfile+"/count_EAMDAR_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CEAMDARU,CEAMDARUDATES= np.loadtxt(ctrlfile+"/count_EAMDAR_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CEAMDARV,CEAMDARVDATES= np.loadtxt(ctrlfile+"/count_EAMDAR_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CPILOTU,CPILOTUDATES= np.loadtxt(ctrlfile+"/count_PILOT_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CPILOTV,CPILOTVDATES= np.loadtxt(ctrlfile+"/count_PILOT_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CTEMPU,CTEMPUDATES= np.loadtxt(ctrlfile+"/count_TEMP_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CTEMPV,CTEMPVDATES= np.loadtxt(ctrlfile+"/count_TEMP_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CTEMPT,CTEMPTDATES= np.loadtxt(ctrlfile+"/count_TEMP_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CTEMPQ,CTEMPQDATES= np.loadtxt(ctrlfile+"/count_TEMP_q_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CAMSUABT,CAMSUABTDATES= np.loadtxt(ctrlfile+"/count_AMSUA_bt_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
    CMHSBT,CMHSBTDATES= np.loadtxt(ctrlfile+"/count_MHS_bt_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

    CSYNOP_TOT=CSYNOPZ
    CSHIP_TOT=CSYNOPZ+CSHIPZ+CSHIPU+CSHIPV
    CBUOY_TOT=CBUOYZ

    CPILOT_TOT=CPILOTU+CPILOTV
    CTEMP_TOT=CTEMPT+CTEMPU+CTEMPV+CTEMPQ

    CAIREP_TOT=CAIREPT+CAIREPU+CAIREPV
    CAMDAR_TOT=CAMDART+CAMDARU+CAMDARV+CEAMDART+CEAMDARU+CEAMDARV

    CAMSUABT_TOT=CAMSUABT
    CMHSBT_TOT=CMHSBT

    Cmeans_exp=[np.mean(CSYNOP_TOT), np.mean(CSHIP_TOT), np.mean(CBUOY_TOT), np.mean(CAIREP_TOT), np.mean(CAMDAR_TOT), np.mean(CPILOT_TOT), np.mean(CTEMP_TOT), np.mean(CAMSUABT_TOT), np.mean(CMHSBT_TOT)]
    Cyerrs_exp=[np.ptp(CSYNOP_TOT),  np.ptp(CSHIP_TOT),  np.ptp(CBUOY_TOT),  np.ptp(CAIREP_TOT),  np.ptp(CAMDAR_TOT),  np.ptp(CPILOT_TOT),  np.ptp(CTEMP_TOT),  np.ptp(CAMSUABT_TOT),  np.ptp(CMHSBT_TOT)]

    Ctot_tot=np.sum(Cmeans_exp)
    Cmperc_exp=Cmeans_exp/Ctot_tot

    if exptfile != None :
        ESYNOPZ,ESYNOPZDATES= np.loadtxt(exptfile+"/count_SYNOP_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        ESHIPZ,ESHIPZDATES= np.loadtxt(exptfile+"/count_SHIP_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        ESHIPU,ESHIPUDATES= np.loadtxt(exptfile+"/count_SHIP_u10m_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        ESHIPV,ESHIPUDATES= np.loadtxt(exptfile+"/count_SHIP_v10m_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        EBUOYZ,EBUOYZDATES= np.loadtxt(exptfile+"/count_BUOY_z_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        EAIREPT,EAIREPTDATES= np.loadtxt(exptfile+"/count_AIREP_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EAIREPU,EAIREPUDATES= np.loadtxt(exptfile+"/count_AIREP_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EAIREPV,EAIREPVDATES= np.loadtxt(exptfile+"/count_AIREP_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        EAMDARU,EAMDARUDATES= np.loadtxt(exptfile+"/count_AMDAR_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EAMDARV,EAMDARVDATES= np.loadtxt(exptfile+"/count_AMDAR_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EAMDART,EAMDARTDATES= np.loadtxt(exptfile+"/count_AMDAR_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        EEAMDART,EEAMDARTDATES= np.loadtxt(exptfile+"/count_EAMDAR_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EEAMDARU,EEAMDARUDATES= np.loadtxt(exptfile+"/count_EAMDAR_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EEAMDARV,EEAMDARVDATES= np.loadtxt(exptfile+"/count_EAMDAR_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        EPILOTU,EPILOTUDATES= np.loadtxt(exptfile+"/count_PILOT_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EPILOTV,EPILOTVDATES= np.loadtxt(exptfile+"/count_PILOT_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        ETEMPU,ETEMPUDATES= np.loadtxt(exptfile+"/count_TEMP_u_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        ETEMPV,ETEMPVDATES= np.loadtxt(exptfile+"/count_TEMP_v_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        ETEMPT,ETEMPTDATES= np.loadtxt(exptfile+"/count_TEMP_t_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        ETEMPQ,ETEMPQDATES= np.loadtxt(exptfile+"/count_TEMP_q_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        EAMSUABT,EAMSUABTDATES= np.loadtxt(exptfile+"/count_AMSUA_bt_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})
        EMHSBT,EMHSBTDATES= np.loadtxt(exptfile+"/count_MHS_bt_12_pp.txt", unpack=True,converters={1:mdates.strpdate2num('%Y%m%d')})

        ESYNOP_TOT=ESYNOPZ
        ESHIP_TOT=ESYNOPZ+ESHIPZ+ESHIPU+ESHIPV
        EBUOY_TOT=EBUOYZ

        EPILOT_TOT=EPILOTU+EPILOTV
        ETEMP_TOT=ETEMPT+ETEMPU+ETEMPV+ETEMPQ

        EAIREP_TOT=EAIREPT+EAIREPU+EAIREPV
        EAMDAR_TOT=EAMDART+EAMDARU+EAMDARV+EEAMDART+EEAMDARU+EEAMDARV

        EAMSUABT_TOT=EAMSUABT
        EMHSBT_TOT=EMHSBT

        Emeans_exp=[np.mean(ESYNOP_TOT), np.mean(ESHIP_TOT), np.mean(EBUOY_TOT), np.mean(EAIREP_TOT), np.mean(EAMDAR_TOT), np.mean(EPILOT_TOT), np.mean(ETEMP_TOT), np.mean(EAMSUABT_TOT), np.mean(EMHSBT_TOT)]
        Eyerrs_exp=[np.ptp(ESYNOP_TOT),  np.ptp(ESHIP_TOT),  np.ptp(EBUOY_TOT),  np.ptp(EAIREP_TOT),  np.ptp(EAMDAR_TOT),  np.ptp(EPILOT_TOT),  np.ptp(ETEMP_TOT),  np.ptp(EAMSUABT_TOT),  np.ptp(EMHSBT_TOT)]

        Etot_tot=np.sum(Emeans_exp)
        Emperc_exp=Emeans_exp/Etot_tot

    label_exp=['SYNOP',  'SHIP',  'BUOY',  'AIREP',  'AMDAR',  'PILOT',  'TEMP', 'AMSU-A', 'MHS']

    index = np.arange(len(Cmeans_exp))
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    fig = plt.figure(figsize=(8.27,2.4))
    ax = fig.add_subplot(111)

    if exptfile != None :
        if plottype == "num" :
            #plt.bar(index+bar_width/2, Cmeans_exp, bar_width, alpha=opacity, color='b', yerr=Cyerrs_exp, error_kw=error_config, label='Observations')
            #plt.bar(index+bar_width/2, Emeans_exp, bar_width, alpha=opacity, color='r', yerr=Eyerrs_exp, error_kw=error_config, label='Observations')
            plt.bar(index, Cmeans_exp, bar_width, alpha=opacity, color='b', error_kw=error_config, label='ctrl')
            plt.bar(index+bar_width, Emeans_exp, bar_width, alpha=opacity, color='r', error_kw=error_config, label='expt')
            ylabelstring="Data count []"
        if plottype == "perc" :
            #plt.bar(index, 100*Cmperc_exp, bar_width, alpha=opacity, color='b', yerr=Cyerrs_exp, error_kw=error_config, label='ctrl')
            #plt.bar(index+bar_width/2, 100*Emperc_exp, bar_width, alpha=opacity, color='r', yerr=Eyerrs_exp, error_kw=error_config, label='expt')
            plt.bar(index, 100*Cmperc_exp, bar_width, alpha=opacity, color='b', error_kw=error_config, label='ctrl')
            plt.bar(index+bar_width, 100*Emperc_exp, bar_width, alpha=opacity, color='r', error_kw=error_config, label='expt')
            ylabelstring="Data count [%]"
    else : 
        if plottype == "num" :
            #plt.bar(index+bar_width/2, Cmeans_exp, bar_width, alpha=opacity, color='b', yerr=Cyerrs_exp, error_kw=error_config, label='Observations')
            plt.bar(index+bar_width/2, Cmeans_exp, bar_width, alpha=opacity, color='b', error_kw=error_config, label='Observations')
            ylabelstring="Data count []"
        if plottype == "perc" :
            #plt.bar(index+bar_width/2, 100*Cmperc_exp, bar_width, alpha=opacity, color='b', yerr=Cyerrs_exp, error_kw=error_config, label='Observations')
            plt.bar(index+bar_width/2, 100*Cmperc_exp, bar_width, alpha=opacity, color='b', error_kw=error_config, label='Observations')
            ylabelstring="Data count [%]"

    plt.legend(loc='upper left',prop={'size':10},labelspacing=0,title="",frameon=False, fancybox=False, ncol=2)

    #plt.title('Observations')
    plt.xlabel('Observations',fontsize=10)
    plt.ylabel(ylabelstring,fontsize=10)

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(label_exp, fontsize=10)

    plt.savefig(outputfile,format='png')

def main(argv):

  parser = argparse.ArgumentParser(description='plot observation count bar chart')

  parser.add_argument('--version', action='version', version='%(prog)s 1.0')

  parser.add_argument("-c", "--ctrl-files", dest="cfile", required=True,  help="CTRL experiment count directory", metavar="CTRL-DIR", type=extant_file)

  parser.add_argument("-e", "--expt-files", dest="efile", required=False, help="EXPT experiment count directory", metavar="EXPT-DIR", type=extant_file)

  parser.add_argument("-t", "--plot-type", dest="ptype",  required=False, help="plot type: num/perc", metavar="PLOT-TYPE", default="num")

  parser.add_argument("-o", "--output",    dest="ofile",  required=False, help="output PNG file", metavar="OUTPUT-PNG", default="out.png")

  args = parser.parse_args()

  print(args)

  ctrlfile=args.cfile
  exptfile=args.efile
  plottype=args.ptype
  outputfile=args.ofile

  try:
      countbar(ctrlfile, exptfile, plottype, outputfile,)
  except Exception as err:
      print err
      traceback.format_exc()

if __name__ == "__main__":
   main(sys.argv[1:])

