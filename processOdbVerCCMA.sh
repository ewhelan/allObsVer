#!/bin/bash

###DEBUG set -x

bold=$(tput bold)
normal=$(tput sgr0)
unline=$(tput smul)

usage() {

PROGNAME=`basename $0`

cat << USAGE

${bold}NAME${normal}
        ${PROGNAME} -  process CCMA odb for forecast verification

${bold}USAGE${normal}
        ${PROGNAME} -i <input-directory> [ -C ] [ -V ]

${bold}DESCRIPTION${normal}
       A quick and dirty bash shell script to produce verification statistics from input ODB-2 files. This script relies on an installation of the ODB-API  software bundle.

       The script scans ${unline}input-directory${normal} for valid ODB-2 files (${unline}ccma_OBTYPE_HH.odb${normal}) and produces the requested statistics. 
        
${bold}OPTIONS${normal}

        -C  produce count statistics

        -V  produce verification statistics

        -i  ${unline}input-directory${normal}
            PATH to directory containing set of verification CCMA ODBs. It is assumed that this directory contains a set of tarred ODBs with the following naming convention: odb_ccma${unline}YYYYMMDDHH${normal}_${unline}FF${normal}.tar

        -h Help! Print usage information.

USAGE
}

PROCHOME=`pwd`
#
# Some defaults
#
USAGE=0
IDIR=DUMMY
BASE=ccma
DOCOUNT=0
DOOBVER=0

#date '+%Y%m%d%H' -d "2018-11-05 03:00:00 7 hour"

#while getopts ECV:s:e:d:o:h option
while getopts ECVi:o:h option
do
  case $option in
    C)
       DOCOUNT=1
       ;;
    V)
       DOOBVER=1
       ;;
    i)
       IDIR=$OPTARG
       ;;
    h)
       USAGE=1
       ;;
    *)
       USAGE=1
       ;;
  esac
done

if [ ${USAGE} -eq 1 ]; then
  usage
  exit 1
fi

if [ ${#} -eq 0 ]; then
  usage
  exit 1
fi

if [ "${IDIR}" == "DUMMY" ]; then
  echo "${unline}input-directory${normal} not specified."
  echo "Please specify using the -i option."
  echo "Exiting ..."
  exit 1
fi

if [ $DOCOUNT -eq 1 ]
then
  cd $IDIR/
  mkdir -p count
  echo
  echo " ... extracting data counts"
  echo
  for FC in 06 12 18 24 30 36 48
  do
    # conventional obs
    OBTYPE=conv
    # SYNOP
    [ ! -f count/count_SYNOP_z_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=1  AND obstype=1 AND (codetype=11 OR codetype=14) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SYNOP_z_${FC}.txt
    [ ! -f count/count_SYNOP_q_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=7  AND obstype=1 AND (codetype=11 OR codetype=14) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SYNOP_q_${FC}.txt
    [ ! -f count/count_SYNOP_t2m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ] && odb sql -T 'select count(*), andate where varno=39 AND obstype=1 AND (codetype=11 OR codetype=14) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SYNOP_t2m_${FC}.txt
    [ ! -f count/count_SYNOP_q2m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ] && odb sql -T 'select count(*), andate where varno=58 AND obstype=1 AND (codetype=11 OR codetype=14) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SYNOP_q2m_${FC}.txt
    # SHIP
    [ ! -f count/count_SHIP_z_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=1  AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SHIP_z_${FC}.txt
    [ ! -f count/count_SHIP_q_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=7  AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SHIP_q_${FC}.txt
    [ ! -f count/count_SHIP_t2m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=39 AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SHIP_t2m_${FC}.txt
    [ ! -f count/count_SHIP_q2m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=58 AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SHIP_q2m_${FC}.txt
    [ ! -f count/count_SHIP_u10m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ] && odb sql -T 'select count(*), andate where varno=41 AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SHIP_u10m_${FC}.txt
    [ ! -f count/count_SHIP_v10m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ] && odb sql -T 'select count(*), andate where varno=42 AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_SHIP_v10m_${FC}.txt
    # AIREP
    [ ! -f count/count_AIREP_t_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=2  AND obstype=2 AND codetype=141 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_AIREP_t_${FC}.txt
    [ ! -f count/count_AIREP_u_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=3  AND obstype=2 AND codetype=141 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_AIREP_u_${FC}.txt
    [ ! -f count/count_AIREP_v_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=4  AND obstype=2 AND codetype=141 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_AIREP_v_${FC}.txt
    [ ! -f count/count_AMDAR_t_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=2  AND obstype=2 AND codetype=144 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_AMDAR_t_${FC}.txt
    [ ! -f count/count_AMDAR_u_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=3  AND obstype=2 AND codetype=144 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_AMDAR_u_${FC}.txt
    [ ! -f count/count_AMDAR_v_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=4  AND obstype=2 AND codetype=144 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_AMDAR_v_${FC}.txt
    [ ! -f count/count_EAMDAR_t_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=2  AND obstype=2 AND codetype=146 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_EAMDAR_t_${FC}.txt
    [ ! -f count/count_EAMDAR_u_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=3  AND obstype=2 AND codetype=146 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_EAMDAR_u_${FC}.txt
    [ ! -f count/count_EAMDAR_v_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=4  AND obstype=2 AND codetype=146 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_EAMDAR_v_${FC}.txt
    # BUOY
    [ ! -f count/count_BUOY_z_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=1  AND obstype=4 AND codetype=165 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_BUOY_z_${FC}.txt
    # TEMP
    [ ! -f count/count_TEMP_z_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=1  AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_z_${FC}.txt
    [ ! -f count/count_TEMP_t_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=2  AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_t_${FC}.txt
    [ ! -f count/count_TEMP_u_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=3  AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_u_${FC}.txt
    [ ! -f count/count_TEMP_v_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=4  AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_v_${FC}.txt
    [ ! -f count/count_TEMP_q_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=7  AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_q_${FC}.txt
    [ ! -f count/count_TEMP_rh_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=29 AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_rh_${FC}.txt
    [ ! -f count/count_TEMP_t2m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=39 AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_t2m_${FC}.txt
    [ ! -f count/count_TEMP_q2m_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=58 AND obstype=5 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_TEMP_q2m_${FC}.txt
    # PILOT
    [ ! -f count/count_PILOT_u_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=3 AND obstype=6 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_PILOT_u_${FC}.txt
    [ ! -f count/count_PILOT_v_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]   && odb sql -T 'select count(*), andate where varno=4 AND obstype=6 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_PILOT_v_${FC}.txt
    # AMSUA
    OBTYPE=amsua
    [ ! -f count/count_AMSUA_bt_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]  && odb sql -T 'select count(*), andate where varno=119 AND obstype=7 AND sensor=3 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_AMSUA_bt_${FC}.txt
    # MHS
    OBTYPE=mhs
    [ ! -f count/count_MHS_bt_${FC}.txt -a -s ccma_${OBTYPE}_${FC}.odb ]    && odb sql -T 'select count(*), andate where varno=119 AND obstype=7 AND (sensor=4 OR sensor=15) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > count/count_MHS_bt_${FC}.txt
  done
#
# Now post-process the count files to add zero count
#
  echo " ... post-processing the data count files"
  cd $IDIR/
  SDTG=`cat dtgs | head -1`
  EDTG=`cat dtgs | tail -1`
  DATE=${SDTG:0:8}
  EDATE=${EDTG:0:8}

  while [ $DATE -le $EDATE ]
  do
    for CNTFILE in `ls count/count_*_*_[0-9][0-9].txt`
    do
      CNTPPFILE=`echo ${CNTFILE} | sed 's/\.txt/_pp.txt/'`
      [ -s ${CNTPPFILE} ] && continue
      if [ ! -f ${CNTFILE} ]
      then
        echo  "       0              ${DATE}" >> ${CNTPPFILE}
      else
        grep ${DATE} ${CNTFILE} >> ${CNTPPFILE} || echo "       0              ${DATE}" >> ${CNTPPFILE}
      fi
    done
#    DATE=`date '+%Y%m%d' -d "${DATE:0:4}-${DATE:4:2}-${DATE:6:2} 12:00:00 1 day"`
    DATE=`date '+%Y%m%d' -d "${DATE:0:4}-${DATE:4:2}-${DATE:6:2} 1 day"`
  done
else
  echo
  echo  " ... data count calculation not selected"
  echo  "     Use -C to calculate data counts"
fi

if [ $DOOBVER -eq 1 ]
then
  cd $IDIR/
  rm -rf obver/
  mkdir -p obver
  for FC in 06 12 18 24 30 36 48
  do
    # conventional obs
    OBTYPE=conv
    # SYNOP
    echo "${FC}      `odb sql -T 'select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) where varno=1  AND obstype=1 AND (codetype=11 OR codetype=14) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb`" >> obver/obver_SYNOP_z.txt
    odb sql -T 'select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) where varno=1  AND obstype=1 AND (codetype=11 OR codetype=14) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > obver/obver_SYNOP_z_${FC}.txt
    # SHIP
    echo "${FC}      `odb sql -T 'select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) where varno=1  AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb`" >> obver/obver_SHIP_z.txt
    odb sql -T 'select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) where varno=1  AND obstype=1 AND (codetype=21 OR codetype=24) AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > obver/obver_SHIP_z_${FC}.txt
    # BUOY
    echo "${FC}      `odb sql -T 'select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) where varno=1  AND obstype=4 AND codetype=165 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb`" >> obver/obver_BUOY_z.txt
    odb sql -T 'select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) where varno=1  AND obstype=4 AND codetype=165 AND obsvalue is not NULL' -i ccma_${OBTYPE}_${FC}.odb > obver/obver_BUOY_z_${FC}.txt
    # AIREP (profile)
    echo "${FC}      `odb sql -T 'select count(*), floor(vertco_reference_1/10000.0)*100+50, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=2 AND codetype=141' -i ccma_conv_${FC}.odb`" >> obver/obver_AIREP_${FC}_t.txt
    # AMDAR (profile)
    echo "${FC}      `odb sql -T 'select count(*), floor(vertco_reference_1/10000.0)*100+50, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=2 AND (codetype=144 OR codetype=146)' -i ccma_conv_${FC}.odb`" >> obver/obver_AMDAR_${FC}_t.txt
    if (( ${FC} % 12 == 0 ))
    then
    # TEMP
      odb sql -T 'select count(*), floor(vertco_reference_1/10000.0)*100+50, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=5 AND vertco_reference_1 <= 50000' -i ccma_conv_${FC}.odb >> obver/obver_TEMP_t_${FC}.txt
      odb sql -T 'select count(*), floor(vertco_reference_1/10000.0)*100+50, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=7 AND obstype=5 AND vertco_reference_1 <= 50000' -i ccma_conv_${FC}.odb >> obver/obver_TEMP_q_${FC}.txt
      odb sql -T 'select count(*), floor(vertco_reference_1/10000.0)*100+50, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=1 AND obstype=5 AND vertco_reference_1 <= 50000' -i ccma_conv_${FC}.odb >> obver/obver_TEMP_z_${FC}.txt
    fi
    # per level
    for LEV in 1000 900 850 700 500 400 300 200 100
    do
      LL=`expr ${LEV} \* 100`
      LO=`expr ${LL} + 5000` 
      HI=`expr ${LL} - 5000` 
      # AIREP
      echo "${FC}      `odb sql -T \"select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=2 AND codetype=141 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}\" -i ccma_conv_${FC}.odb`" >> obver/obver_AIREP_${LEV}_t.txt
      odb sql -T "select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=2 AND codetype=141 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}" -i ccma_conv_${FC}.odb >> obver/obver_AIREP_${LEV}_t_${FC}.txt
      # AMDAR
      echo "${FC}      `odb sql -T \"select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=2 AND (codetype=144 OR codetype=146) AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}\" -i ccma_conv_${FC}.odb`" >> obver/obver_AMDAR_${LEV}_t.txt
      odb sql -T "select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=2 AND (codetype=144 OR codetype=146) AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}" -i ccma_conv_${FC}.odb >> obver/obver_AMDAR_${LEV}_t_${FC}.txt
      if (( ${FC} % 12 == 0 ))
      then
      # TEMP
        echo "${FC}      `odb sql -T \"select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=1 AND obstype=5 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}\" -i ccma_conv_${FC}.odb`" >> obver/obver_TEMP_${LEV}_z.txt
        odb sql -T "select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=1 AND obstype=5 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}" -i ccma_conv_${FC}.odb >> obver/obver_TEMP_${LEV}_z_${FC}.txt
        echo "${FC}      `odb sql -T \"select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=5 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}\" -i ccma_conv_${FC}.odb`" >> obver/obver_TEMP_${LEV}_t.txt
        odb sql -T "select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=2 AND obstype=5 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}" -i ccma_conv_${FC}.odb >> obver/obver_TEMP_${LEV}_t_${FC}.txt
        echo "${FC}      `odb sql -T \"select count(*), avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=7 AND obstype=5 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}\" -i ccma_conv_${FC}.odb`" >> obver/obver_TEMP_${LEV}_q.txt
        odb sql -T "select count(*), andate, avg(fg_depar), stdev(fg_depar), var(fg_depar), rms(fg_depar) WHERE varno=7 AND obstype=5 AND vertco_reference_1 < ${LO} AND vertco_reference_1 >= ${HI}" -i ccma_conv_${FC}.odb >> obver/obver_TEMP_${LEV}_q_${FC}.txt
      fi
    done
  done
else
  echo
  echo  " ... verification statistics calculation not selected"
  echo  "     Use -V to calculate verification statistics."
fi
exit 0
