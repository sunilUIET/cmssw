# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions auto:run2_mc -n 10 --era Phase2 --eventcontent FEVTDEBUGHLT -s RAW2DIGI,L1Reco,RECO:localreco --datatier GEN-SIM-DIGI-RAW --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2023LReco --geometry Extended2023LReco --no_exec --filein file:out_sim.root --fileout out_local_reco.root
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
    fileNames = cms.untracked.vstring('/store/user/subansal/mcProd/TenMuons_Pt100/TenMuons_Pt100_GEN_SIM_DIGI_CMSSW810Pre5/160525_213712/0000/out_digi_1.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:10'),
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

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.localreco)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)

#--------------------------------------------------------------------------
# RPC aging

from L1Trigger.L1IntegratedMuonTrigger.RPCChamberMasker_cff import *
appendRPCChamberMaskerAtUnpacking2(process,True,[637570221,637602989,637635757,637569201,637634737,637571545,637571677,637637213,637567793,637600561,637633329,637566989,637632525,637566993,637632529,637569037,637634573,637571565,637637101,637571449,637636985,637572317,637637853,637568057,637600825,637633593,637568025,637633561,637567381,637632917,637571805,637637341,637569325,637602093,637634861,637572569,637638105,637571569,637637105,637567065,637632601,637570229,637635765,637567285,637600053,637632821,637572589,637638125,637571157,637636693,637570485,637636021,637571181,637636717,637567069,637632605,637570365,637603133,637635901,637570481,637636017,637572445,637637981,637567005,637632541,637567373,637632909,637568509,637634045,637569425,637634961,637572561,637638097,637568409,637633945,637571281,637636817,637569973,637635509,637567157,637599925,637632693,637571197,637636733,637571321,637636857,637570237,637603005,637635773,637569453,637602221,637634989,637569977,637635513,637568305,637601073,637633841,637570097,637635633,637570197,637635733,637569709,637602477,637635245,637571161,637636697,637572429,637637965,637567669,637600437,637633205,637572045,637637581,637568301,637633837,637567213,637632749,637567801,637600569,637633337,637568053,637600821,637633589,637570109,637602877,637635645,637567965,637633501,637567993,637633529,637637081,637571193,637636729,637567281,637600049,637632817,637567469,637633005,637567953,637633489,637568177,637600945,637633713,637568469,637634005,637567021,637632557,637571317,637636853,637567885,637633421,637572085,637637621,637568213,637633749,637567441,637632977,637569305,637634841,637567341,637632877,637575669,637641205,637567665,637600433,637633201,637567805,637633341,637570233,637635769,637570321,637635857,637567033,637599801,637632569,637568505,637634041,637571453,637636989,637579769,637645305,637572573,637638109,637571277,637636813,637568237,637633773,637571925,637637461,637568089,637633625,637569457,637634993,637572437,637637973,637571961,637637497,637568345,637633881,637572345,637637881,637567189,637632725,637571413,637575620,637608388,637641156,637588100,637620868,637653636,637571816,637604584,637637352,637575462,637608230,637640998,637579430,637612198,637644966,637566980,637599748,637632516,637567242,637600010,637632778,637587818,637620586,637653354,637567722,637600490,637633258,637579784,637612552,637645320,637579658,637612426,637645194,637575242,637608010,637640778,637587976,637620744,637653512,637575466,637608234,637641002,637567524,637600292,637633060,637571658,637604426,637637194,637579882,637612650,637645418,637567462,637600230,637632998,637587556,637620324,637653092,637579942,637612710,637645478,637571210,637603978,637636746,637579748,637612516,637645284,637575338,637608106,637640874,637587976,637620744,637653512,637579910,637612678,637645446,637583944,637616712,637649480,637584106,637616874,637649642,637579782,637612550,637645318,637579592,637612360,637645128])

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023LReco 

#call to customisation function cust_2023LReco imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2023LReco(process)

# End of customisation functions

