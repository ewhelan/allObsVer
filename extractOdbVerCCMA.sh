#!/bin/bash

###DEBUG set -x

bold=$(tput bold)
normal=$(tput sgr0)
unline=$(tput smul)

usage() {

PROGNAME=`basename $0`

cat << USAGE

${bold}NAME${normal}
        ${PROGNAME} -  extract CCMA odb data for forecast verification

${bold}USAGE${normal}
        ${PROGNAME} -i <input-directory> [-o <output-directory>]

${bold}DESCRIPTION${normal}
       A quick and dirty bash shell script to extract verification statistics from a set of CCMA ODBs. The extraction process relies on an installation of the ODB-API  software bundle.

       The script scans ${unline}input-directory${normal} for tarred CCMA ODB directories. It is assumed that this directory contains a set of tarred ODBs with the following naming convention: odb_ccma${unline}YYYYMMDDHH${normal}_${unline}FF${normal}.tar. The un-tarred ODBs are copied to ${unline}output-directory${normal} and converted to ODB-2 format files. This conversion should speed up the data-processing and generation of statistics.
        
${bold}OPTIONS${normal}

        -i  ${unline}input-directory${normal}
            PATH to directory containing set of verification CCMA ODBs. It is assumed that this directory contains a set of tarred ODBs with the following naming convention: odb_ccma${unline}YYYYMMDDHH${normal}_${unline}FF${normal}.tar

        -o  ${unline}output-directory${normal}
            Speficy PATH to store extracted statisitcs. Default value is ${unline}input-directory${normal}/extr.

        -h Help! Print usage information.

USAGE
}

PROCHOME=`pwd`
#
# Some defaults
#
USAGE=0
IDIR=DUMMY
ODIR=DUMMY

#date '+%Y%m%d%H' -d "2018-11-05 03:00:00 7 hour"

while getopts i:o:h option
do
  case $option in
    i)
       IDIR=$OPTARG
       ;;
    o)
       ODIR=$OPTARG
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

#
# 0. Get first and last DTG in the input-directory
#
[ ${ODIR} == "DUMMY" ] && ODIR=${IDIR}/extr/

cd ${IDIR}/
SDTG=`ls odb_ccma[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-2][0-9]_[0-9][0-9].tar | head -1 | sed 's/[a-z,\.]//g' | sed 's/_//' | cut -c 1-10`
LDTG=`ls odb_ccma[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-2][0-9]_[0-9][0-9].tar | tail -1 | sed 's/[a-z,\.]//g' | sed 's/_//' | cut -c 1-10`
EDTG=`date '+%Y%m%d%H' -d "${LDTG:0:4}-${LDTG:4:2}-${LDTG:6:2} ${LDTG:8:2}:00:00 48 hour"`


EXTRDIR=${ODIR}
mkdir -p ${EXTRDIR}

echo $SDTG >  ${EXTRDIR}/dtgs
echo $EDTG >> ${EXTRDIR}/dtgs

#
# 1. Un-tar CCMA ODBs in to unique sub-directories
#
cd ${IDIR}/
for FILE in `ls odb_ccma[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-2][0-9]_[0-9][0-9].tar`
do
  DTGF=`echo $FILE | sed 's/[a-z,\.]//g' | sed 's/_//' `
  [ -d $EXTRDIR/${DTGF}/odb_ccma ] && continue
  mkdir -p $EXTRDIR/${DTGF}/
  tar -xvf ${FILE}
  mv odb_ccma/ $EXTRDIR/${DTGF}/
done
#
# 2. Extract data obver using ODB-API
#
which dcagen || { echo " ... ODB-API: dcagen not in PATH"; exit 1; }
which odb_migrator || { echo " ... ODB-API: odb_migrator not in PATH"; exit 1; }
cd $EXTRDIR/
for DIR in `ls -d [0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-2][0-9]_[0-9][0-9]/odb_ccma/CCMA`
do
  DTG=`echo $DIR | cut -c 1-10`
  FC=`echo $DIR | cut -c 12-13`
  echo ${DIR}
  cd ${DIR}
  [ ! -d dca ] && dcagen
  pwd
  cd ../..
  for OBTYPE in conv amsua mhs
  do
    [ ! -s ccma_${OBTYPE}_${DTG}_${FC}.odb ] && odb_migrator odb_ccma/CCMA ${PROCHOME}/sql_38/${OBTYPE}.sql ccma_${OBTYPE}_${DTG}_${FC}.odb 2>&1
  done
  cd $EXTRDIR/
done
#
# 3. Aggregate ODB2s into ccma_${OBTYPE}_${FC}.odb files
#
cd $EXTRDIR/
for OBTYPE in conv amsua mhs
do
  for FC in 06 12 18 24 30 36 48
  do
    rm -f ccma_${OBTYPE}_${FC}.odb
    cat $EXTRDIR/[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-2][0-9]_${FC}/ccma_${OBTYPE}_[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-2][0-9]_${FC}.odb >> ccma_${OBTYPE}_${FC}.odb
  done
done

exit 0
