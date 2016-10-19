# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions auto:run2_mc -n 10 --era Phase2 --eventcontent FEVTDEBUGHLT -s RAW2DIGI,L1Reco,RECO:localreco --datatier GEN-SIM-DIGI-RAW --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2023LReco --geometry Extended2023LReco --no_exec --filein file:out_sim.root --fileout out_local_reco.root
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
processName = 'RECO'
process = cms.Process(processName)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/user/subansal/mcProd/TenMuons_Pt100/TenMuons_Pt100_GEN_SIM_DIGI_CMSSW810Pre5/160525_213712/0000/out_digi_1.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

process.out = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('drop *', "keep *_MEtoEDMConverter_*_"+processName),
    fileName = cms.untracked.string('validationEDM_AllAging.root')
)
process.outpath = cms.EndPath(process.out)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.categories = ['TrackAssociator', 'TrackValidator']
process.MessageLogger.debugModules = ['*']
process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string('DEBUG'),
    default = cms.untracked.PSet(
        limit = cms.untracked.int32(0)
    ),
    TrackAssociator = cms.untracked.PSet(
        limit = cms.untracked.int32(0)
    ),
    TrackValidator = cms.untracked.PSet(
        limit = cms.untracked.int32(-1)
    )
)
process.MessageLogger.cerr = cms.untracked.PSet(
    placeholder = cms.untracked.bool(True)
)


process.load("DQMServices.Components.MEtoEDMConverter_cfi")
process.MEtoEDMConverter_step = cms.Path(process.MEtoEDMConverter)

process.load("Configuration.StandardSequences.Services_cff")

#---- Validation stuffs ----#
## Default validation modules
process.load("Configuration.StandardSequences.Validation_cff")
process.muonValidation_step = cms.Path(process.recoMuonValidation)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')


# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.localreco*process.offlineBeamSpot*process.standalonemuontracking)
process.endjob_step = cms.EndPath(process.endOfProcess)
###process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.muonValidation_step, process.MEtoEDMConverter_step,process.outpath)
#process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step, process.MEtoEDMConverter_step,process.outpath)
