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
#include "TMath.h"

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
      size_t getRegionOf24(double eta, double phi);

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

      TH1D *NEvents;

      TH1D *L1EG_pt;
      TH1D *L1EG_energy;
      TH1D *L1EG_eta;
      TH1D *L1EG_phi;
      TH1D *L1EG_withCuts_pt;
      TH1D *L1EG_withCuts_energy;
      TH1D *L1EG_withCuts_eta;
      TH1D *L1EG_withCuts_phi;

      TH1D *Region;
      TH1D *TotalL1EG;
      TH1D *L1EGPerRegion;
      std::vector<size_t> l1egPerRegion; // position in vector is region, 0-23
      TH1D *TotalL1EG_withCuts;
      TH1D *L1EGPerRegion_withCuts;
      std::vector<size_t> l1egPerRegion_withCuts; // position in vector is region, 0-23
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
   NEvents = fs->make<TH1D>("NEvents" , "NEvents" , 1 , 0 , 1 );
   L1EG_pt = fs->make<TH1D>("L1EG_pt" , "L1EG_pt" , 50 , 0 , 50 );
   L1EG_energy = fs->make<TH1D>("L1EG_energy" , "L1EG_energy" , 100 , 0 , 100 );
   L1EG_eta = fs->make<TH1D>("L1EG_eta" , "L1EG_eta" , 40 , -2 , 2 );
   L1EG_phi = fs->make<TH1D>("L1EG_phi" , "L1EG_phi" , 70 , -3.5 , 3.5 );
   L1EG_withCuts_pt = fs->make<TH1D>("L1EG_withCuts_pt" , "L1EG_withCuts_pt" , 50 , 0 , 50 );
   L1EG_withCuts_energy = fs->make<TH1D>("L1EG_withCuts_energy" , "L1EG_withCuts_energy" , 100 , 0 , 100 );
   L1EG_withCuts_eta = fs->make<TH1D>("L1EG_withCuts_eta" , "L1EG_withCuts_eta" , 40 , -2 , 2 );
   L1EG_withCuts_phi = fs->make<TH1D>("L1EG_withCuts_phi" , "L1EG_withCuts_phi" , 70 , -3.5 , 3.5 );

   Region = fs->make<TH1D>("Region" , "Region" , 30 , 0 , 30 );
   TotalL1EG = fs->make<TH1D>("TotalL1EG" , "TotalL1EG" , 100 , 0 , 100 );
   L1EGPerRegion = fs->make<TH1D>("L1EGPerRegion" , "L1EGPerRegion" , 30 , 0 , 30 );
   TotalL1EG_withCuts = fs->make<TH1D>("TotalL1EG_withCuts" , "TotalL1EG_withCuts" , 60 , 0 , 60 );
   L1EGPerRegion_withCuts = fs->make<TH1D>("L1EGPerRegion_withCuts" , "L1EGPerRegion_withCuts" , 30 , 0 , 30 );

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

   NEvents->Fill( 0 );
   l1egPerRegion.clear();
   l1egPerRegion_withCuts.clear();
   for (size_t i = 0; i < 24; ++i) {
      l1egPerRegion.push_back( 0 );
      l1egPerRegion_withCuts.push_back( 0 );
   }
   size_t region;
   for(const auto& cluster : crystalClusters)
   {
      L1EG_pt->Fill( cluster.pt() );
      L1EG_energy->Fill( cluster.energy() );
      L1EG_eta->Fill( cluster.eta() );
      L1EG_phi->Fill( cluster.phi() );
      region = getRegionOf24( cluster.eta(), cluster.phi() );
      Region->Fill( region );
      l1egPerRegion[region] = l1egPerRegion[region]+1;
   }
   TotalL1EG->Fill( crystalClusters.size() );
   for (size_t i = 0; i < l1egPerRegion.size(); ++i) L1EGPerRegion->Fill( l1egPerRegion[i] );

   iEvent.getByToken(crystalClustersWithCutsToken_,crystalClustersWithCutsHandle);
   crystalClustersWithCuts = (*crystalClustersWithCutsHandle.product());

   for(const auto& cluster : crystalClustersWithCuts)
   {
      L1EG_withCuts_pt->Fill( cluster.pt() );
      L1EG_withCuts_energy->Fill( cluster.energy() );
      L1EG_withCuts_eta->Fill( cluster.eta() );
      L1EG_withCuts_phi->Fill( cluster.phi() );
      region = getRegionOf24( cluster.eta(), cluster.phi() );
      l1egPerRegion_withCuts[region] = l1egPerRegion_withCuts[region]+1;
   }
   TotalL1EG_withCuts->Fill( crystalClustersWithCuts.size() );
   for (size_t i = 0; i < l1egPerRegion_withCuts.size(); ++i) L1EGPerRegion_withCuts->Fill( l1egPerRegion_withCuts[i] );


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


// ------------ method to return which hardware card the L1EG object is associate to x / 24 cards ------
size_t
L1EGPreclusterAnalysis::getRegionOf24(double eta, double phi)
{

  double pi = TMath::Pi();
  double phiDeg = phi * 180. / pi;
  double absPhiDeg = fabs(phiDeg);
  size_t returnVal = 0;

  // Increment for eta side, Neg is cards 0-11, Pos = 12-23
  if (eta >= 0.0) returnVal += 12;
  // Increment for phi + / -
  if (phiDeg >= 0.0) returnVal += 6;
  // return with val associated with exact phi location
  if (absPhiDeg >= 0 && absPhiDeg < 30) return 0+returnVal;
  if (absPhiDeg >= 30 && absPhiDeg < 60) return 1+returnVal;
  if (absPhiDeg >= 60 && absPhiDeg < 90) return 2+returnVal;
  if (absPhiDeg >= 90 && absPhiDeg < 120) return 3+returnVal;
  if (absPhiDeg >= 30 && absPhiDeg < 150) return 4+returnVal;
  if (absPhiDeg >= 30 && absPhiDeg <= 180) return 5+returnVal;

  std::cout << "This is bad, shouldn't be here" << std::endl;

  return 29;

}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGPreclusterAnalysis);

