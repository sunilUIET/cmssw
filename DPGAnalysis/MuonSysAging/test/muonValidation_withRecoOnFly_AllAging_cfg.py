# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions auto:run2_mc -n 10 --era Phase2 --eventcontent FEVTDEBUGHLT -s RAW2DIGI,L1Reco,RECO:localreco --datatier GEN-SIM-DIGI-RAW --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2023LReco --geometry Extended2023LReco --no_exec --filein file:out_sim.root --fileout out_local_reco.root
import FWCore.ParameterSet.Config as cms

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
    input = cms.untracked.int32(99)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#'/store/relval/CMSSW_8_1_0_pre12/RelValSingleMuPt100Extended/GEN-SIM-DIGI-RAW/81X_mcRun2_asymptotic_v8_2023D1-v1/00000/365BDCBC-E782-E611-AEAA-0CC47A7C351E.root',
'/store/relval/CMSSW_8_1_0_pre12/RelValSingleMuPt100Extended/GEN-SIM-DIGI-RAW/81X_mcRun2_asymptotic_v8_2023D1-v1/00000/404D2F7A-E582-E611-876F-0CC47A7C3422.root'

)
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
#process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("CondCore.DBCommon.CondDBCommon_cfi")

#from CondCore.DBCommon.CondDB_cfi import *
from CondCore.DBCommon.CondDBSetup_cfi import *

process.mcSource = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0),
        authenticationPath = cms.untracked.string('.')
    ),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('MuonSystemAgingRcd'),
        tag = cms.string('MuonSystemAging_test')
    )),
    connect = cms.string('sqlite_file:MuonSystemAging.db')
)

#---- Validation stuffs ----#
## Default validation modules
process.load("Configuration.StandardSequences.Validation_cff")
#process.validation_step = cms.Path(process.validation)
## Load muon validation modules
#process.recoMuonVMuAssoc.outputFileName = 'validationME.root'
#process.muonValidation_step = cms.Path(cms.SequencePlaceholder("mix")+process.recoMuonValidation)
process.muonValidation_step = cms.Path(process.recoMuonValidation)
#process.schedule = cms.Schedule(
#    process.raw2digi_step,
##    process.validation_step,
#    process.muonValidation_step,
#    process.MEtoEDMConverter_step,process.outpath)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

#--------------------------------------------------------------------------
# CSC aging

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    csc2DRecHitsOverload = cms.PSet(
        initialSeed = cms.untracked.uint32(81)
    ),
)

process.csc2DRecHitsOverload = cms.EDProducer('CFEBBufferOverloadProducer',
    cscRecHitTag = cms.InputTag("csc2DRecHits"),
#    failureRate = cms.untracked.double(0.15),
    doUniformFailure = cms.untracked.bool(True),
    doCFEBFailure = cms.untracked.bool(True),
)

# change input to cscSegments
process.cscSegments.inputObjects = "csc2DRecHitsOverload"

process.csclocalreco.replace(process.cscSegments, process.csc2DRecHitsOverload)
process.csclocalreco += process.cscSegments


# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.localreco*process.offlineBeamSpot*process.standalonemuontracking)
process.endjob_step = cms.EndPath(process.endOfProcess)
###process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.muonValidation_step, process.MEtoEDMConverter_step,process.outpath)

from DPGAnalysis.MuonSysAging.DTChamberMasker_cff import *
appendChamberMaskerAtUnpacking(process,True,True,[
    # MB4 of top sectors
    "WH-2_ST4_SEC2","WH-2_ST4_SEC3","WH-2_ST4_SEC4","WH-2_ST4_SEC5","WH-2_ST4_SEC6",
    ])

#--------------------------------------------------------------------------
# RPC aging

from DPGAnalysis.MuonSysAging.RPCChamberMasker_cff import *
appendRPCChamberMaskerAtUnpacking2(process,True,[637570221,637645128])

reRunDttf( process )

