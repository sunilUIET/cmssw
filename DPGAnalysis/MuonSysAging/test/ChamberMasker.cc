// -*- C++ -*-
//
// Class:      ChamberMasker
// 
//
// Original Author:  Sunil Bansal
//         Created:  Wed, 29 Jun 2016 16:27:31 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/IOVSyncValue.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/MuonSystemAging/interface/MuonSystemAging.h"
#include "CondCore/DBOutputService/interface/PoolDBOutputService.h"
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class ChamberMasker : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit ChamberMasker(const edm::ParameterSet&);
      ~ChamberMasker();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      std::vector<int> m_maskedRPCIDs;
      std::vector<std::string> m_maskedDTIDs;
      double m_ineffCSC;      

      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
ChamberMasker::ChamberMasker(const edm::ParameterSet& iConfig)

{  
   m_ineffCSC = iConfig.getParameter<double>("CSCineff"); 
   for ( auto rpc_ids : iConfig.getParameter<std::vector<int>>("maskedRPCIDs"))
    {
      m_maskedRPCIDs.push_back(rpc_ids);
      std::cout<<rpc_ids<<std::endl;
    }

    for ( auto regStr : iConfig.getParameter<std::vector<std::string>>("maskedChRegEx") )
    {
    m_maskedDTIDs.push_back(regStr);

    }


   //now do what ever initialization is needed
   usesResource("TFileService");

}


ChamberMasker::~ChamberMasker()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
ChamberMasker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

 MuonSystemAging* pList = new MuonSystemAging();
 for(unsigned int i = 0; i < m_maskedRPCIDs.size();++i){
 pList->m_RPCchambers.push_back(m_maskedRPCIDs.at(i));
 }
 for(unsigned int i = 0; i < m_maskedDTIDs.size();++i){
 pList->m_DTchambers.push_back(std::string(m_maskedDTIDs.at(i)));
 }
 pList->m_CSCineff = m_ineffCSC; 
 edm::Service<cond::service::PoolDBOutputService> poolDbService;
 if( poolDbService.isAvailable() ) poolDbService->writeOne( pList, poolDbService->currentTime(),"MuonSystemAgingRcd" );

}


// ------------ method called once each job just before starting event loop  ------------
void 
ChamberMasker::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ChamberMasker::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
ChamberMasker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ChamberMasker);
