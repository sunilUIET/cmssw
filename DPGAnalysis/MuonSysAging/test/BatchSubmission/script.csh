#!/bin/csh

cat > script_$1.csh << EOF
#!/bin/csh

setenv VO_CMS_SW_DIR /cvmfs/cms.cern.ch
source \$VO_CMS_SW_DIR/cmsset_default.csh

setenv CASA `pwd`
echo \$CASA
cd \$CASA
setenv SCRAM_ARCH slc5_amd64_gcc472
echo $SCRAM_ARCH
eval \`scramv1 runtime -csh\`

cmsenv
cmsRun \$CASA/test_data$1.py >& /lustre/cms/store/user/calabria/HZZ_235MCHF/$1.txt

EOF

chmod 777 script_$1.csh
qsub -q local -l nodes=1:ppn=2 script_$1.csh

