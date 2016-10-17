# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --conditions auto:run2_mc -n 10 --era Phase2 --eventcontent FEVTDEBUGHLT -s L1,DIGI2RAW,RAW2DIGI,L1Reco,RECO:localreco --datatier GEN-SIM-DIGI-RAW --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2023LReco --geometry Extended2023LReco --no_exec --filein file:out_sim.root --fileout out_local_reco.root
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Phase2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023LRecoReco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:genEvts/out_l1.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(10485760),
    fileName = cms.untracked.string('out_local_reco.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
#--------------------------------------------------------------------------

# CSC
# case 0  :: all detectors in
# case 1  :: ME1/1 switched off
# case 2  :: ME2/1 switched off
# case 3  :: ME3/1 switched off
# case 4  :: ME4/1 switched off
# default :: all detectors in

# RPC
# case 0  :: NO RPC Upgrade
# case 1  :: RE3/1 switched off
# case 2  :: RE4/1 switched off
# case 3  :: RPC Upgrade switched on
# default :: all detectors in

#GEM
# case 0  :: all detectors off
# case 1  :: GE1/1 switched on
# case 2  :: GE2/1 switched on
# case 3  :: all detectors in
# default :: all detectors in

process.load('RecoLocalMuon.RPCRecHit.rpcRecHits_cfi')
process.load('RecoLocalMuon.GEMRecHit.gemRecHits_cfi')
process.load('RecoLocalMuon.CSCRecHitD.cscRecHitD_cfi')

#235 MCHF: GE2/1 + RE3/1 + RE4/1 switched off
process.csc2DRecHits.stationToUse = cms.untracked.int32(0)
process.rpcRecHits.recAlgoConfig.stationToUse = cms.untracked.int32(0)
process.gemRecHits.recAlgoConfig.stationToUse = cms.untracked.int32(1)


# CSC aging

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    csc2DRecHitsOverload = cms.PSet(
        initialSeed = cms.untracked.uint32(81)
    ),
)

process.csc2DRecHitsOverload = cms.EDProducer('CFEBBufferOverloadProducer',
    cscRecHitTag = cms.InputTag("csc2DRecHits"),
    failureRate = cms.untracked.double(0.15),
    doUniformFailure = cms.untracked.bool(True),
    doCFEBFailure = cms.untracked.bool(True),
)

# change input to cscSegments
process.cscSegments.inputObjects = "csc2DRecHitsOverload"

process.csclocalreco.replace(process.cscSegments, process.csc2DRecHitsOverload)
process.csclocalreco += process.cscSegments


# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# Path and EndPath definitions
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.localreco)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.L1simulation_step,process.digi2raw_step,process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023LReco 

#call to customisation function cust_2023LReco imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2023LReco(process)

# End of customisation functions

