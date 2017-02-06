// -*- C++ -*-
//
// Package:    L1Trigger/CSCChamberMasker
// Class:      CSCChamberMasker
// 
/**\class CSCChamberMasker CSCChamberMasker.cc L1Trigger/CSCChamberMasker/plugins/CSCChamberMasker.cc

 Description: Class to mask CSC digis or trigger segments on a chamber by chamber basis

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Carlo Battilana
//         Created:  Sun, 11 Jan 2015 15:12:51 GMT
//
//


// system include files
#include <map>
#include <memory>
#include <string>
#include <iostream>
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"

#include "Geometry/CSCGeometry/interface/CSCChamber.h"
#include "Geometry/CSCGeometry/interface/CSCLayer.h"

#include "DataFormats/CSCDigi/interface/CSCStripDigi.h"
#include "DataFormats/CSCDigi/interface/CSCStripDigiCollection.h"
#include "DataFormats/CSCDigi/interface/CSCWireDigi.h"
#include "DataFormats/CSCDigi/interface/CSCWireDigiCollection.h"
#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "DataFormats/MuonDetId/interface/CSCIndexer.h"

#include "CondFormats/MuonSystemAging/interface/MuonSystemAging.h"
#include "CondFormats/DataRecord/interface/MuonSystemAgingRcd.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "CLHEP/Random/RandomEngine.h"


//
// class declaration
//

class CSCChamberMasker : public edm::EDProducer {
public:
  explicit CSCChamberMasker(const edm::ParameterSet&);
  ~CSCChamberMasker();

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  virtual void beginJob() override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;
      
  virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;

  void createMaskedChamberCollection(edm::ESHandle<CSCGeometry> &); 

  // ----------member data ---------------------------

  edm::EDGetTokenT <CSCStripDigiCollection> m_stripDigiToken;
  edm::EDGetTokenT <CSCWireDigiCollection> m_wireDigiToken;
  std::map<CSCDetId, std::pair<unsigned int,float> > m_CSCEffs;  
  
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//
//vector<L1MuRegionalCand>
//
// constructors and destructor
//
CSCChamberMasker::CSCChamberMasker(const edm::ParameterSet& iConfig) 
    :
  m_stripDigiToken(consumes<CSCStripDigiCollection>(iConfig.getParameter<edm::InputTag>("stripDigiTag")) ),
  m_wireDigiToken(consumes<CSCWireDigiCollection>(iConfig.getParameter<edm::InputTag>("wireDigiTag")) )
{

  produces<CSCStripDigiCollection>("MuonCSCStripDigi");
  produces<CSCWireDigiCollection>("MuonCSCWireDigi");

}


CSCChamberMasker::~CSCChamberMasker()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
CSCChamberMasker::produce(edm::Event& event, const edm::EventSetup& conditions)
{
  
  edm::Service<edm::RandomNumberGenerator> randGenService;
  CLHEP::HepRandomEngine& randGen = randGenService->getEngine(event.streamID());
 
  std::unique_ptr<CSCStripDigiCollection> filteredStripDigis(new CSCStripDigiCollection());
  std::unique_ptr<CSCWireDigiCollection> filteredWireDigis(new CSCWireDigiCollection());

  if(!m_stripDigiToken.isUninitialized())
  {
      edm::Handle<CSCStripDigiCollection> cscStripDigis;
      event.getByToken(m_stripDigiToken, cscStripDigis);

      for (CSCStripDigiCollection::DigiRangeIterator j=cscStripDigis->begin(); j!=cscStripDigis->end(); j++) {
          std::vector<CSCStripDigi>::const_iterator digiItr = (*j).second.first;
          CSCDetId const cscDetId=(*j).first;

          // Since lookups are chamber-centric, make new DetId with layer=0
          CSCDetId chId = CSCDetId(cscDetId.endcap(), cscDetId.station(), cscDetId.ring(), cscDetId.chamber(), 0);
          std::cout<<"Det id: " << chId<<std::endl;

          std::vector<CSCStripDigi>::const_iterator last = (*j).second.second;
          for( ; digiItr != last; ++digiItr) {

              auto chEffIt = m_CSCEffs.find(chId);

              // std::cout<<"  Strip Digi: " << (*digiItr) <<std::endl;
              if (chEffIt != m_CSCEffs.end()) {
                  std::pair<unsigned int, float> typeEff = chEffIt->second;
                  if (typeEff.first == EFF_STRIPS && randGen.flat() <= typeEff.second) {
                      std::cout << "We're keeping this digi" << std::endl;
                      filteredStripDigis->insertDigi(cscDetId,*digiItr);
                  } else {
                      std::cout << "We're !!dropping!! this digi" << std::endl;
                  }
              } 
          }
      }
  }

  if(!m_stripDigiToken.isUninitialized())
  {

      edm::Handle<CSCWireDigiCollection> cscWireDigis;
      event.getByToken(m_wireDigiToken, cscWireDigis);

      for (CSCWireDigiCollection::DigiRangeIterator j=cscWireDigis->begin(); j!=cscWireDigis->end(); j++) {
          std::vector<CSCWireDigi>::const_iterator digiItr = (*j).second.first;
          // CSCDetId const cscDetId=(*j).first;
          // std::cout<<"Det id: " << cscDetId<<std::endl;
          std::vector<CSCWireDigi>::const_iterator last = (*j).second.second;
          for( ; digiItr != last; ++digiItr) {
              // std::cout<<"  Wire Digi: " << (*digiItr) <<std::endl;
              // FIXME, don't write out any wire digis right now to test the masking
              // filteredWireDigis->insertDigi(cscDetId,*digiItr);
          }
      }
  }



  event.put(std::move(filteredStripDigis), "MuonCSCStripDigi");
  event.put(std::move(filteredWireDigis), "MuonCSCWireDigi");

}

// ------------ method called once each job just before starting event loop  ------------
void 
CSCChamberMasker::beginJob()
{

}

// ------------ method called once each job just after ending the event loop  ------------
void 
CSCChamberMasker::endJob()
{

}

// ------------ method called when starting to processes a run  ------------
void
CSCChamberMasker::beginRun(edm::Run const& run, edm::EventSetup const& iSetup)
{

  m_CSCEffs.clear();

  edm::ESHandle<CSCGeometry> cscGeom;
  iSetup.get<MuonGeometryRecord>().get(cscGeom);

  edm::ESHandle<MuonSystemAging> agingObj;
  iSetup.get<MuonSystemAgingRcd>().get(agingObj);

  const auto chambers = cscGeom->chambers();

  for ( const auto * ch : chambers)
  {

      CSCDetId  chId    = ch->id();
      unsigned int rawId = chId.rawIdMaker(chId.endcap(), chId.station(), chId.ring(), chId.chamber(), 0);
      float eff = 1.;
      int type = 0;
      int i = 0;
      for ( auto & agingPair : agingObj->m_CSCChambEffs)
      {
          if ( agingPair.first != rawId) continue;

          type = agingPair.second.first;
          eff = agingPair.second.second;
          m_CSCEffs[chId] = std::make_pair(type, eff);	 
          break;
      }

  }

}

  
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
CSCChamberMasker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  // desc.add<edm::InputTag>("digiTag", edm::InputTag("simMuonCSCDigis"));
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(CSCChamberMasker);
