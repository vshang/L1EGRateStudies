// -*- C++ -*-
//
// Package:    SLHCUpgradeSimulations/L1EGRateStudies
// Class:      EcalTPAnalyzer
// 
/**\class EcalTPAnalyzer EcalTPAnalyzer.cc SLHCUpgradeSimulations/L1EGRateStudies/src/EcalTPAnalyzer.cc

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
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"

// All for Calo geometry for getting energy/pt/eta/phi per crystal
#include "FastSimulation/CaloGeometryTools/interface/CaloGeometryHelper.h"
#include "Geometry/CaloTopology/interface/CaloTopology.h"
#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/EcalAlgo/interface/EcalBarrelGeometry.h"

// ECAL TPs
#include "SimCalorimetry/EcalEBTrigPrimProducers/plugins/EcalEBTrigPrimProducer.h"
#include "DataFormats/EcalDigi/interface/EcalEBTriggerPrimitiveDigi.h"

// ECAL RecHits
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"

//
// class declaration
//

class EcalTPAnalyzer : public edm::EDAnalyzer {
   public:
      explicit EcalTPAnalyzer(const edm::ParameterSet&);
      ~EcalTPAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      CaloGeometryHelper geometryHelper;
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------

      bool useRecHits;

      edm::EDGetTokenT<EcalRecHitCollection> ecalRecHitEBToken_;
      edm::EDGetTokenT<EcalEBTrigPrimDigiCollection> ecalTPEBToken_;

      TH1D *totalHits;
      TH1D *totalNonZeroHits;
      TH1D *TP_or_recHit_et;
      TH1D *TP_or_recHit_energy;
      TH1D *TP_or_recHit_eta;
      TH1D *TP_or_recHit_phi;
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
EcalTPAnalyzer::EcalTPAnalyzer(const edm::ParameterSet& iConfig) :
   useRecHits(iConfig.getParameter<bool>("useRecHits")),
   ecalRecHitEBToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("ecalRecHitEB"))),
   ecalTPEBToken_(consumes<EcalEBTrigPrimDigiCollection>(iConfig.getParameter<edm::InputTag>("ecalTPEB")))
{
   //now do what ever initialization is needed

   edm::Service<TFileService> fs;
   totalHits = fs->make<TH1D>("totalHits" , "totalHits" , 200 , 0 , 20000 );
   totalNonZeroHits = fs->make<TH1D>("totalNonZeroHits" , "totalNonZeroHits" , 500 , 0 , 500 );
   TP_or_recHit_et = fs->make<TH1D>("TP_or_recHit_et" , "TP_or_recHit_et" , 300 , 0 , 30 );
   TP_or_recHit_energy = fs->make<TH1D>("TP_or_recHit_energy" , "TP_or_recHit_energy" , 200 , 0 , 50 );
   TP_or_recHit_eta = fs->make<TH1D>("TP_or_recHit_eta" , "TP_or_recHit_eta" , 40 , -2 , 2 );
   TP_or_recHit_phi = fs->make<TH1D>("TP_or_recHit_phi" , "TP_or_recHit_phi" , 70 , -3.5 , 3.5 );

}


EcalTPAnalyzer::~EcalTPAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
EcalTPAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   if ( geometryHelper.getEcalBarrelGeometry() == nullptr )
   {
      edm::ESHandle<CaloTopology> theCaloTopology;
      iSetup.get<CaloTopologyRecord>().get(theCaloTopology);
      edm::ESHandle<CaloGeometry> pG;
      iSetup.get<CaloGeometryRecord>().get(pG);
      double bField000 = 4.;
      if ( !pG.isValid() || !theCaloTopology.isValid() ) { std::cout << "Bad times" << std::endl;
        return;}
      else {
      geometryHelper.setupGeometry(*pG);
      geometryHelper.setupTopology(*theCaloTopology);
      std::cout << "Pre-Initialize Geometry Helper" << std::endl;
      geometryHelper.initialize(bField000);
      std::cout << "Post-Initialize Geometry Helper" << std::endl;
      }
   }
   using namespace edm;

   int totTP = 0;
   int totNonZeroTP = 0;
   float energy;
   float et;
   float eta;
   float phi;
   GlobalVector position; // As opposed to GlobalPoint, so we can add them (for weighted average)
   float highestPhi=-999;
   float highestEta=-999;
   float highestE=0;
   double long event = iEvent.eventAuxiliary().event();

   // Retrieve the ecal barrel hits
   // using RecHits (https://cmssdt.cern.ch/SDT/doxygen/CMSSW_6_1_2_SLHC6/doc/html/d8/dc9/classEcalRecHit.html)
   if (useRecHits) {
      edm::Handle<EcalRecHitCollection> pcalohits;
      iEvent.getByToken(ecalRecHitEBToken_,pcalohits);
      for(auto& hit : *pcalohits.product())
      {
         totTP++;
         // Because we need position to calculate Et, skim a little first for Energy > 500 MeV
         // then figure out Et for comparison with ECAL TPs
         if(hit.energy() >= 0.2 && !hit.checkFlag(EcalRecHit::kOutOfTime) && !hit.checkFlag(EcalRecHit::kL1SpikeFlag))
         {
            auto cell = geometryHelper.getEcalBarrelGeometry()->getGeometry(hit.id());
            position = GlobalVector(cell->getPosition().x(), cell->getPosition().y(), cell->getPosition().z());
            energy = hit.energy();
            et = energy * sin(position.theta());
            if (et > 0.6) {
               totNonZeroTP++;
               eta = cell->getPosition().eta();
               phi = cell->getPosition().phi();
               TP_or_recHit_et->Fill( et );
               TP_or_recHit_energy->Fill( energy );
               TP_or_recHit_eta->Fill( eta );
               TP_or_recHit_phi->Fill( phi );
               if (energy > highestE) {
                  highestE = energy;
                  highestPhi = phi;
                  highestEta = eta;
               }
            }
         }
      }
   }

   else {
      edm::Handle<EcalEBTrigPrimDigiCollection> pcalohits;
      iEvent.getByToken(ecalTPEBToken_,pcalohits);
      for(auto& hit : *pcalohits.product())
      {
         totTP++;
         if(hit.compressedEt() > 0) // && !hit.l1aSpike()) // hit.compressedEt() returns an int corresponding to 2x the crystal Et
         {
            totNonZeroTP++;
            auto cell = geometryHelper.getEcalBarrelGeometry()->getGeometry(hit.id());
            position = GlobalVector(cell->getPosition().x(), cell->getPosition().y(), cell->getPosition().z());
            et = hit.compressedEt()/2.;
            energy = et / sin(position.theta());
            eta = cell->getPosition().eta();
            phi = cell->getPosition().phi();
            TP_or_recHit_et->Fill( et );
            TP_or_recHit_energy->Fill( energy );
            TP_or_recHit_eta->Fill( eta );
            TP_or_recHit_phi->Fill( phi );
            if (energy > highestE) {
               highestE = energy;
               highestPhi = phi;
               highestEta = eta;
            }
         }
      }
   }
   // Now fill
   totalHits->Fill( totTP ); 
   totalNonZeroHits->Fill( totNonZeroTP ); 

   std::cout << event << ":  highest hit energy: " << highestE <<
        "  phi: " << highestPhi << "  eta: " << highestEta << std::endl;


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
EcalTPAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EcalTPAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
EcalTPAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
EcalTPAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
EcalTPAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
EcalTPAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EcalTPAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(EcalTPAnalyzer);

