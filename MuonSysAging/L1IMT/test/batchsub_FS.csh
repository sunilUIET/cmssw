#!/bin/tcsh
setenv VO_CMS_SW_DIR /cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.csh
limit vmem unlim

cd /cmshome/calabria/ValidazioneOfficial2/CMSSW_6_2_0_SLHC26_patch2/src/L1Trigger/L1IntegratedMuonTrigger/test
setenv SCRAM_ARCH slc6_amd64_gcc472
eval `scramv1 runtime -csh`
#echo `pwd`
cmsRun /cmshome/calabria/ValidazioneOfficial2/CMSSW_6_2_0_SLHC26_patch2/src/L1Trigger/L1IntegratedMuonTrigger/test/step3_fullScope_cfg.py