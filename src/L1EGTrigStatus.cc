// -*- C++ -*-
//
// Package:    L1Trigger/L1EGRateStudies
// Class:      L1EGPreclusterAnalysis
// 
/**\class L1EGPreclusterAnalysis L1EGPreclusterAnalysis.cc L1Trigger/L1EGRateStudies/src/L1EGPreclusterAnalysis.cc

 Description: [save a few hists showing distributions of all L1EG TPs]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Tyler Ruggles
//         Created:  Wed, 11 Jan 2017
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"

#include "DataFormats/Phase2L1CaloTrig/interface/L1EGCrystalCluster.h"

//
// class declaration
//

class L1EGPreclusterAnalysis : public edm::EDAnalyzer {
   public:
      explicit L1EGPreclusterAnalysis(const edm::ParameterSet&);
      ~L1EGPreclusterAnalysis();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------

      //edm::InputTag L1CrystalClustersInputTag;

      edm::EDGetTokenT<l1slhc::L1EGCrystalClusterCollection> crystalClustersToken_;
      l1slhc::L1EGCrystalClusterCollection crystalClusters;
      edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersHandle;      

      edm::EDGetTokenT<l1slhc::L1EGCrystalClusterCollection> crystalClustersWithCutsToken_;
      l1slhc::L1EGCrystalClusterCollection crystalClustersWithCuts;
      edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersWithCutsHandle;

      TH1D *L1EG_pt;
      TH1D *L1EG_energy;
      TH1D *L1EG_eta;
      TH1D *L1EG_phi;
      TH1D *L1EG_withCuts_pt;
      TH1D *L1EG_withCuts_energy;
      TH1D *L1EG_withCuts_eta;
      TH1D *L1EG_withCuts_phi;
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
L1EGPreclusterAnalysis::L1EGPreclusterAnalysis(const edm::ParameterSet& iConfig) :
   crystalClustersToken_(consumes<l1slhc::L1EGCrystalClusterCollection>(iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag"))),
   crystalClustersWithCutsToken_(consumes<l1slhc::L1EGCrystalClusterCollection>(iConfig.getParameter<edm::InputTag>("L1CrystalClustersWithCutsInputTag")))
{
   //now do what ever initialization is needed

   edm::Service<TFileService> fs;
   L1EG_pt = fs->make<TH1D>("L1EG_pt" , "L1EG_pt" , 50 , 0 , 50 );
   L1EG_energy = fs->make<TH1D>("L1EG_energy" , "L1EG_energy" , 100 , 0 , 100 );
   L1EG_eta = fs->make<TH1D>("L1EG_eta" , "L1EG_eta" , 40 , -2 , 2 );
   L1EG_phi = fs->make<TH1D>("L1EG_phi" , "L1EG_phi" , 70 , -3.5 , 3.5 );
   L1EG_withCuts_pt = fs->make<TH1D>("L1EG_withCuts_pt" , "L1EG_withCuts_pt" , 50 , 0 , 50 );
   L1EG_withCuts_energy = fs->make<TH1D>("L1EG_withCuts_energy" , "L1EG_withCuts_energy" , 100 , 0 , 100 );
   L1EG_withCuts_eta = fs->make<TH1D>("L1EG_withCuts_eta" , "L1EG_withCuts_eta" , 40 , -2 , 2 );
   L1EG_withCuts_phi = fs->make<TH1D>("L1EG_withCuts_phi" , "L1EG_withCuts_phi" , 70 , -3.5 , 3.5 );

}


L1EGPreclusterAnalysis::~L1EGPreclusterAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1EGPreclusterAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   iEvent.getByToken(crystalClustersToken_,crystalClustersHandle);
   crystalClusters = (*crystalClustersHandle.product());

   for(const auto& cluster : crystalClusters)
   {
      L1EG_pt->Fill( cluster.pt() );
      L1EG_energy->Fill( cluster.energy() );
      L1EG_eta->Fill( cluster.eta() );
      L1EG_phi->Fill( cluster.phi() );
   }

   iEvent.getByToken(crystalClustersWithCutsToken_,crystalClustersWithCutsHandle);
   crystalClustersWithCuts = (*crystalClustersWithCutsHandle.product());

   for(const auto& cluster : crystalClustersWithCuts)
   {
      L1EG_withCuts_pt->Fill( cluster.pt() );
      L1EG_withCuts_energy->Fill( cluster.energy() );
      L1EG_withCuts_eta->Fill( cluster.eta() );
      L1EG_withCuts_phi->Fill( cluster.phi() );
   }


#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
L1EGPreclusterAnalysis::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1EGPreclusterAnalysis::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
L1EGPreclusterAnalysis::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1EGPreclusterAnalysis::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1EGPreclusterAnalysis::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1EGPreclusterAnalysis::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1EGPreclusterAnalysis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGPreclusterAnalysis);

