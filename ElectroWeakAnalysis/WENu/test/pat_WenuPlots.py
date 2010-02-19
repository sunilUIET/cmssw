import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")


process.MessageLogger = cms.Service(
        "MessageLogger",
            categories = cms.untracked.vstring('info', 'debug','cout')
            )

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)


# source
process.source = cms.Source("PoolSource", 
     fileNames = cms.untracked.vstring(
    'rfio:/castor/cern.ch/cms/store/relval/CMSSW_3_5_1/RelValZEE/GEN-SIM-RECO/MC_3XY_V21-v1/0001/005DD63C-B51C-DF11-BA60-0030487CD6E6.root',
    )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

## Load additional processes
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
## global tags:
process.GlobalTag.globaltag = cms.string('MC_3XY_V21::All')
#process.GlobalTag.globaltag = cms.string('STARTUP31X_V4::All')
process.load("Configuration.StandardSequences.MagneticField_cff")


################################################################################################
###    P r e p a r a t i o n      o f    t h e    P A T    O b j e c t s   f r o m    A O D  ###
################################################################################################

## pat sequences to be loaded:
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")
process.load("PhysicsTools.PatAlgos.patSequences_cff")
#process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
##
#
# for ecal isolation: set the correct name of the ECAL rechit collection
# 
#process.eleIsoDepositEcalFromHits.ExtractorPSet.barrelEcalHits = cms.InputTag("reducedEcalRecHitsEB", "", "RECO")
#process.eleIsoDepositEcalFromHits.ExtractorPSet.endcapEcalHits = cms.InputTag("reducedEcalRecHitsEE", "", "RECO")
#
#
#process.eidRobustHighEnergy.reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB", "", "RECO")
#process.eidRobustHighEnergy.reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE", "", "RECO")     

## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## MET creation     <=== WARNING: YOU MAY WANT TO MODIFY THIS PART OF THE CODE       %%%%%%%%%%%%%
##                                specify the names of the MET collections that you need here %%%%
##                                                                                             #%%
## if you don't specify anything the default MET is the raw Calo MET                           #%%
process.layer1RawCaloMETs = process.patMETs.clone(                                          #%%
    metSource = cms.InputTag("met","","RECO"),
    addTrigMatch = cms.bool(False),
    addMuonCorrections = cms.bool(False),
    addGenMET = cms.bool(False),
    )
## specify here what you want to have on the plots! <===== MET THAT YOU WANT ON THE PLOTS  %%%%%%%
myDesiredMetCollection = 'layer1RawCaloMETs'
## modify the sequence of the MET creation:                                                    #%%
process.makePatMETs = cms.Sequence(process.patMETCorrections * process.patMETs *
                                   process.layer1RawCaloMETs)
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## modify the final pat sequence: keep only electrons + METS (muons are needed for met corrections)
process.load("RecoEgamma.EgammaIsolationAlgos.egammaIsolationSequence_cff")
#process.electronEcalRecHitIsolationLcone.ecalBarrelRecHitProducer = cms.InputTag("reducedEcalRecHitsEB")
#process.electronEcalRecHitIsolationScone.ecalBarrelRecHitProducer = cms.InputTag("reducedEcalRecHitsEB")
#process.electronEcalRecHitIsolationLcone.ecalEndcapRecHitProducer = cms.InputTag("reducedEcalRecHitsEE")
#process.electronEcalRecHitIsolationScone.ecalEndcapRecHitProducer = cms.InputTag("reducedEcalRecHitsEE")
#
#process.electronEcalRecHitIsolationLcone.ecalBarrelRecHitCollection = cms.InputTag("")
#process.electronEcalRecHitIsolationScone.ecalBarrelRecHitCollection = cms.InputTag("")
#process.electronEcalRecHitIsolationLcone.ecalEndcapRecHitCollection = cms.InputTag("")
#process.electronEcalRecHitIsolationScone.ecalEndcapRecHitCollection = cms.InputTag("")
#
#
process.patElectronIsolation = cms.Sequence(process.egammaIsolationSequence)

process.patElectrons.isoDeposits = cms.PSet()
process.patElectrons.userIsolation = cms.PSet(
       tracker = cms.PSet(
            src = cms.InputTag("electronTrackIsolationLcone"),
        ),
        ecal = cms.PSet(
            src = cms.InputTag("electronEcalRecHitIsolationScone"),
        ),
        hcal = cms.PSet(
            src = cms.InputTag("electronHcalTowerIsolationScone"),
        ),
        user = cms.VPSet(),

    )

##
## Pre-calculated electron identification selections
##
## set the variable false if you don't need them, or if you use your own PSet
##
## any input tag you set corresponds to a valuemap that either it is stored in the event
## or you create it yourself
process.patElectrons.addElectronID = cms.bool(True)
process.patElectrons.electronIDSources = cms.PSet(
    eidRobustLoose      = cms.InputTag("eidRobustLoose"),
    eidRobustTight      = cms.InputTag("eidRobustTight"),
    eidLoose            = cms.InputTag("eidLoose"),
    eidTight            = cms.InputTag("eidTight"),
    )
##
process.patElectrons.addGenMatch = cms.bool(False)
process.patElectrons.embedGenMatch = cms.bool(False)
##
## if you want to create your own pre-calculated ID then you have to run it
##
## process.myOwnPreCalID =  cms.Sequence(process.idfilter)
## process.patElectronIDs = cms.Sequence(process.myOwnPreCalID)
## process.makePatElectrons = cms.Sequence(process.patElectronIDs*process.patElectronIsolation*process.patElectrons)
process.makePatElectrons = cms.Sequence(process.patElectronIsolation*process.patElectrons)
process.makePatCandidates = cms.Sequence(process.makePatElectrons+process.makePatMuons+process.makePatMETs)

process.patDefaultSequence = cms.Sequence(process.makePatCandidates)
##
##  ################################################################################
##
##  the filter to select the candidates from the data samples
##
##
## WARNING: you may want to modify this item:
HLT_process_name = "HLT"   # options: HLT or HLT8E29
# trigger path selection
HLT_path_name    = "HLT_Ele15_LW_L1R"
# trigger filter name
HLT_filter_name  =  "hltL1NonIsoHLTNonIsoSingleElectronLWEt15PixelMatchFilter"
#
process.wenuFilter = cms.EDFilter('WenuCandidateFilter',
                                  # cuts
                                  ETCut = cms.untracked.double(30.),
                                  METCut = cms.untracked.double(0.),
                                  vetoSecondElectronEvents = cms.untracked.bool(False),
                                  ETCut2ndEle = cms.untracked.double(20.),
                                  # trigger here
                                  useTriggerInfo = cms.untracked.bool(False),
                                  triggerCollectionTag = cms.untracked.InputTag("TriggerResults","",HLT_process_name),
                                  triggerEventTag = cms.untracked.InputTag("hltTriggerSummaryAOD","",HLT_process_name),
                                  hltpath = cms.untracked.string(HLT_path_name),
                                  hltpathFilter = cms.untracked.InputTag(HLT_filter_name,"",HLT_process_name),
                                  electronMatched2HLT = cms.untracked.bool(False),
                                  electronMatched2HLT_DR = cms.untracked.double(0.2),
                                  # electrons and MET
                                  electronCollectionTag = cms.untracked.InputTag("patElectrons","","PAT"),
                                  metCollectionTag = cms.untracked.InputTag(myDesiredMetCollection,"","PAT")

                                  )
####################################################################################
##
## the W selection that you prefer
selection_a2 = cms.PSet (
    trackIso_EB = cms.untracked.double(2.2),
    ecalIso_EB = cms.untracked.double(4.2),
    hcalIso_EB = cms.untracked.double(2.0),
    sihih_EB = cms.untracked.double(0.0099),
    dphi_EB = cms.untracked.double(0.025),
    deta_EB = cms.untracked.double(0.0040),
    hoe_EB = cms.untracked.double(1000.0),
    
    trackIso_EE = cms.untracked.double(1.1),
    ecalIso_EE = cms.untracked.double(3.4),
    hcalIso_EE = cms.untracked.double(1.3),
    sihih_EE = cms.untracked.double(0.028),
    dphi_EE = cms.untracked.double(0.020),
    deta_EE = cms.untracked.double(0.0066),
    hoe_EE = cms.untracked.double(1000.0)
    )

selection_test = cms.PSet (
    trackIso_EB = cms.untracked.double(10),
    ecalIso_EB = cms.untracked.double(10),
    hcalIso_EB = cms.untracked.double(10),
    sihih_EB = cms.untracked.double(0.1),
    dphi_EB = cms.untracked.double(1),
    deta_EB = cms.untracked.double(1),
    hoe_EB = cms.untracked.double(1),
    
    trackIso_EE = cms.untracked.double(10),
    ecalIso_EE = cms.untracked.double(10),
    hcalIso_EE = cms.untracked.double(10),
    sihih_EE = cms.untracked.double(1),
    dphi_EE = cms.untracked.double(1),
    deta_EE = cms.untracked.double(1),
    hoe_EE = cms.untracked.double(1)
    )

selection_inverse = cms.PSet (
    trackIso_EB_inv = cms.untracked.bool(True),
    trackIso_EE_inv = cms.untracked.bool(True)
    )

####################################################################################
##
## and the plot creator
process.plotter = cms.EDAnalyzer('WenuPlots',
                                 # selection in use
                                 selection_a2,
                                 selection_inverse,
                                 # if usePrecalcID the precalculated ID will be used only
                                 usePrecalcID = cms.untracked.bool(True),
                                 usePrecalcIDType = cms.untracked.string('eidTight'),
                                 usePrecalcIDSign = cms.untracked.string('='),
                                 usePrecalcIDValue = cms.untracked.double(1),
                                 # selections cuts on the fly
                                 # ..  should be there even not in use
                                 # ..  they are not used if usePrecalcID = true
                                 #
                                 #
                                 wenuCollectionTag = cms.untracked.InputTag(
    "wenuFilter","selectedWenuCandidates","PAT")
                                 )




process.p = cms.Path(process.patDefaultSequence +process.wenuFilter + process.plotter)
# process.p = cms.Path(process.patSequences + process.wenuFilter + process.eca)


#### SET OF Trigger names for AOD - 321
#
#  HLTPath_[0] = "HLT_Ele10_LW_L1R";
#  HLTFilterType_[0] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt10PixelMatchFilter","","HLT8E29");
#  HLTPath_[1] = "HLT_Ele10_LW_EleId_L1R";
#  HLTFilterType_[1] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt10EleIdDphiFilter","","HLT8E29");
#  HLTPath_[2] = "HLT_Ele15_LW_L1R";
#  HLTFilterType_[2] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt15PixelMatchFilter","","HLT8E29");
#  HLTPath_[3] = "HLT_Ele15_SC10_LW_L1R";
#  HLTFilterType_[3] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt15ESDoubleSC10","","HLT8E29");
#  HLTPath_[4] = "HLT_Ele15_SiStrip_L1R";
#  HLTFilterType_[4] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronSiStripEt15PixelMatchFilter","","HLT8E29");
#  HLTPath_[5] = "HLT_Ele20_LW_L1R";
#  HLTFilterType_[5] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt15EtFilterESet20","","HLT8E29");
#  HLTPath_[6] = "HLT_DoubleEle5_SW_L1R";
#  HLTFilterType_[6] = edm::InputTag("hltL1NonIsoHLTNonIsoDoubleElectronEt5PixelMatchFilter","","HLT8E29");
#  HLTPath_[7] = "HLT_Ele15_SC10_LW_L1R";
#  HLTFilterType_[7] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt15ESDoubleSC10","","HLT8E29");
#  HLTPath_[8] = "tba";
#  HLTFilterType_[8] = edm::InputTag("tba");
#  HLTPath_[9] = "tba";
#  HLTFilterType_[9] = edm::InputTag("tba");
#  // e31 menu
#  HLTPath_[10] = "HLT_Ele10_SW_L1R";
#  HLTFilterType_[10] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt10PixelMatchFilter","","HLT");
#  HLTPath_[11] = "HLT_Ele15_SW_L1R";
#  HLTFilterType_[11] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15PixelMatchFilter","","HLT");
#  HLTPath_[12] = "HLT_Ele15_SiStrip_L1R"; // <--- same as [4]
#  HLTFilterType_[12] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronSiStripEt15PixelMatchFilter","","HLT");
#  HLTPath_[13] = "HLT_Ele15_SW_LooseTrackIso_L1R";
#  HLTFilterType_[13] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15LTITrackIsolFilter","","HLT");
#  HLTPath_[14] = "HLT_Ele15_SW_EleId_L1R";
#  HLTFilterType_[14] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15EleIdDphiFilter","","HLT");
#  HLTPath_[15] = "HLT_Ele20_SW_L1R";
#  HLTFilterType_[15] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt20PixelMatchFilter","","HLT");
#  HLTPath_[16] = "HLT_Ele20_SiStrip_L1R";
#  HLTFilterType_[16] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronSiStripEt20PixelMatchFilter","","HLT");
#  HLTPath_[17] = "HLT_Ele25_SW_L1R";
#  HLTFilterType_[17] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15EtFilterESet25","","HLT");
#  HLTPath_[18] = "HLT_Ele25_SW_EleId_LooseTrackIso_L1R";
#  HLTFilterType_[18] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15EleIdTrackIsolFilterESet25LTI","","HLT");
#  HLTPath_[19] = "HLT_DoubleEle10_SW_L1R";
#  HLTFilterType_[19] = edm::InputTag("hltL1NonIsoHLTNonIsoDoubleElectronEt10PixelMatchFilter","","HLT");
#  HLTPath_[20] = "HLT_Ele15_SC15_SW_EleId_L1R";
#  HLTFilterType_[20] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15EleIdESDoubleSC15","","HLT");
#  HLTPath_[21] = "HLT_Ele15_SC15_SW_LooseTrackIso_L1R";
#  HLTFilterType_[21] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15LTIESDoubleSC15","","HLT");
#  HLTPath_[22] = "HLT_Ele20_SC15_SW_L1R";
#  HLTFilterType_[22] = edm::InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt20ESDoubleSC15","","HLT");
