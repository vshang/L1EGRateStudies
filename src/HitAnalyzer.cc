// -*- C++ -*-
//
// Package:    L1Trigger/L1EGRateStudies
// Class:      HitAnalyzer
// 
/**\class HitAnalyzer HitAnalyzer.cc L1Trigger/L1EGRateStudies/src/HitAnalyzer.cc

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
#include "TTree.h"

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

// HCAL RecHits
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalSourcePositionData.h"

// Gen Particles
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

//
// class declaration
//

class HitAnalyzer : public edm::EDAnalyzer {
   public:
      explicit HitAnalyzer(const edm::ParameterSet&);
      ~HitAnalyzer();

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
      bool useEcalTPs;
      bool hasGenInfo;

      edm::EDGetTokenT<EcalRecHitCollection> ecalRecHitEBToken_;
      edm::EDGetTokenT<EcalEBTrigPrimDigiCollection> ecalTPEBToken_;
      edm::EDGetTokenT<HBHERecHitCollection> hcalRecHitToken_;
      edm::EDGetTokenT<reco::GenParticleCollection> genCollectionToken_;
      reco::GenParticleCollection genParticles;


      TH1D *ecal_totalHits;
      TH1D *ecal_totalNonZeroHits;
      TH1D *ecal_TP_or_recHit_et;
      TH1D *ecal_TP_or_recHit_energy;
      TH1D *ecal_TP_or_recHit_eta;
      TH1D *ecal_TP_or_recHit_phi;
      TH1D *hcal_totalHits;
      TH1D *hcal_totalNonZeroHits;
      TH1D *hcal_TP_or_recHit_et;
      TH1D *hcal_TP_or_recHit_energy;
      TH1D *hcal_TP_or_recHit_eta;
      TH1D *hcal_TP_or_recHit_phi;

      TTree * hit_tree;
      struct {
        double run;
        double lumi;
        double event;
        std::vector< float > ecalHit_energy;
        std::vector< float > ecalHit_et;
        std::vector< float > ecalHit_eta;
        std::vector< float > ecalHit_phi;
        std::vector< float > ecalHit_iEta;
        std::vector< float > ecalHit_iPhi;
        std::vector< float > hcalHit_energy;
        std::vector< float > hcalHit_et;
        std::vector< float > hcalHit_eta;
        std::vector< float > hcalHit_phi;
        std::vector< float > hcalHit_iEta;
        std::vector< float > hcalHit_iPhi;
        std::vector< float > genParticle_energy;
        std::vector< float > genParticle_pt;
        std::vector< float > genParticle_eta;
        std::vector< float > genParticle_phi;
        std::vector< float > genParticle_pdgId;
      } treeinfo;

      // These will fill the ecalHit/hcalHits
      float energy;
      float et;
      float eta;
      float phi;
      float iPhi;
      float iEta;
      EBDetId id; // for getting iEta, iPhi

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
HitAnalyzer::HitAnalyzer(const edm::ParameterSet& iConfig) :
   useRecHits(iConfig.getParameter<bool>("useRecHits")),
   useEcalTPs(iConfig.getParameter<bool>("useEcalTPs")),
   hasGenInfo(iConfig.getParameter<bool>("hasGenInfo")),
   ecalRecHitEBToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("ecalRecHitEB"))),
   ecalTPEBToken_(consumes<EcalEBTrigPrimDigiCollection>(iConfig.getParameter<edm::InputTag>("ecalTPEB"))),
   hcalRecHitToken_(consumes<HBHERecHitCollection>(iConfig.getParameter<edm::InputTag>("hcalRecHit"))),
   genCollectionToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles")))
{
   //now do what ever initialization is needed

   edm::Service<TFileService> fs;
   ecal_totalHits = fs->make<TH1D>("ecal totalHits" , "ecal totalHits" , 200 , 0 , 20000 );
   ecal_totalNonZeroHits = fs->make<TH1D>("ecal totalNonZeroHits" , "ecal totalNonZeroHits" , 500 , 0 , 500 );
   ecal_TP_or_recHit_et = fs->make<TH1D>("ecal TP_or_recHit_et" , "ecal TP_or_recHit_et" , 300 , 0 , 30 );
   ecal_TP_or_recHit_energy = fs->make<TH1D>("ecal TP_or_recHit_energy" , "ecal TP_or_recHit_energy" , 200 , 0 , 50 );
   ecal_TP_or_recHit_eta = fs->make<TH1D>("ecal TP_or_recHit_eta" , "ecal TP_or_recHit_eta" , 40 , -2 , 2 );
   ecal_TP_or_recHit_phi = fs->make<TH1D>("ecal TP_or_recHit_phi" , "ecal TP_or_recHit_phi" , 70 , -3.5 , 3.5 );
   hcal_totalHits = fs->make<TH1D>("hcal totalHits" , "hcal totalHits" , 200 , 0 , 3000 );
   hcal_totalNonZeroHits = fs->make<TH1D>("hcal totalNonZeroHits" , "hcal totalNonZeroHits" , 500 , 0 , 500 );
   hcal_TP_or_recHit_et = fs->make<TH1D>("hcal TP_or_recHit_et" , "hcal TP_or_recHit_et" , 300 , 0 , 30 );
   hcal_TP_or_recHit_energy = fs->make<TH1D>("hcal TP_or_recHit_energy" , "hcal TP_or_recHit_energy" , 200 , 0 , 50 );
   hcal_TP_or_recHit_eta = fs->make<TH1D>("hcal TP_or_recHit_eta" , "hcal TP_or_recHit_eta" , 40 , -2 , 2 );
   hcal_TP_or_recHit_phi = fs->make<TH1D>("hcal TP_or_recHit_phi" , "hcal TP_or_recHit_phi" , 70 , -3.5 , 3.5 );

   // Make TTree too
   hit_tree = fs->make<TTree>("hit_tree","hit_tree");
   hit_tree->Branch("run", &treeinfo.run);
   hit_tree->Branch("lumi", &treeinfo.lumi);
   hit_tree->Branch("event", &treeinfo.event);
   hit_tree->Branch("ecalHit_energy", &treeinfo.ecalHit_energy);
   hit_tree->Branch("ecalHit_et", &treeinfo.ecalHit_et);
   hit_tree->Branch("ecalHit_eta", &treeinfo.ecalHit_eta);
   hit_tree->Branch("ecalHit_phi", &treeinfo.ecalHit_phi);
   hit_tree->Branch("ecalHit_iEta", &treeinfo.ecalHit_iEta);
   hit_tree->Branch("ecalHit_iPhi", &treeinfo.ecalHit_iPhi);
   hit_tree->Branch("hcalHit_energy", &treeinfo.hcalHit_energy);
   hit_tree->Branch("hcalHit_et", &treeinfo.hcalHit_et);
   hit_tree->Branch("hcalHit_eta", &treeinfo.hcalHit_eta);
   hit_tree->Branch("hcalHit_phi", &treeinfo.hcalHit_phi);
   hit_tree->Branch("hcalHit_iEta", &treeinfo.hcalHit_iEta);
   hit_tree->Branch("hcalHit_iPhi", &treeinfo.hcalHit_iPhi);
   hit_tree->Branch("genParticle_energy", &treeinfo.genParticle_energy);
   hit_tree->Branch("genParticle_pt", &treeinfo.genParticle_pt);
   hit_tree->Branch("genParticle_eta", &treeinfo.genParticle_eta);
   hit_tree->Branch("genParticle_phi", &treeinfo.genParticle_phi);
   hit_tree->Branch("genParticle_pdgId", &treeinfo.genParticle_pdgId);

}


HitAnalyzer::~HitAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
HitAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   // Make sure we are only running a single set of hits at a time
   assert(useRecHits * useEcalTPs == 0);

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

   int e_totTP = 0;
   int e_totNonZeroTP = 0;
   int h_totTP = 0;
   int h_totNonZeroTP = 0;
   GlobalVector position; // As opposed to GlobalPoint, so we can add them (for weighted average)
   //float highestPhi=-999;
   //float highestEta=-999;
   //float highestE=0;

   // Clear our possibly pre-filled vectors
   treeinfo.ecalHit_energy.clear();
   treeinfo.ecalHit_et.clear();
   treeinfo.ecalHit_eta.clear();
   treeinfo.ecalHit_phi.clear();
   treeinfo.ecalHit_iEta.clear();
   treeinfo.ecalHit_iPhi.clear();
   treeinfo.hcalHit_energy.clear();
   treeinfo.hcalHit_et.clear();
   treeinfo.hcalHit_eta.clear();
   treeinfo.hcalHit_phi.clear();
   treeinfo.hcalHit_iEta.clear();
   treeinfo.hcalHit_iPhi.clear();
   treeinfo.genParticle_energy.clear();
   treeinfo.genParticle_pt.clear();
   treeinfo.genParticle_eta.clear();
   treeinfo.genParticle_phi.clear();
   treeinfo.genParticle_pdgId.clear();

   treeinfo.run = iEvent.eventAuxiliary().run();
   treeinfo.lumi = iEvent.eventAuxiliary().luminosityBlock();
   treeinfo.event = iEvent.eventAuxiliary().event();

   // Retrieve the ecal barrel hits
   // using RecHits (https://cmssdt.cern.ch/SDT/doxygen/CMSSW_6_1_2_SLHC6/doc/html/d8/dc9/classEcalRecHit.html)
   if (useRecHits) {
      edm::Handle<EcalRecHitCollection> pcalohits;
      iEvent.getByToken(ecalRecHitEBToken_,pcalohits);
      for(auto& hit : *pcalohits.product())
      {
         e_totTP++;
         // Because we need position to calculate Et, skim a little first for Energy > 500 MeV
         // then figure out Et for comparison with ECAL TPs
         if(hit.energy() >= 0.2 && !hit.checkFlag(EcalRecHit::kOutOfTime) && !hit.checkFlag(EcalRecHit::kL1SpikeFlag))
         {
            auto cell = geometryHelper.getEcalBarrelGeometry()->getGeometry(hit.id());
            position = GlobalVector(cell->getPosition().x(), cell->getPosition().y(), cell->getPosition().z());
            energy = hit.energy();
            et = energy * sin(position.theta());
            if (et > 0.5) { // 0.6 to do a faux calibration comparison with Ecal TPs
               e_totNonZeroTP++;
               eta = cell->getPosition().eta();
               phi = cell->getPosition().phi();
               ecal_TP_or_recHit_et->Fill( et );
               ecal_TP_or_recHit_energy->Fill( energy );
               ecal_TP_or_recHit_eta->Fill( eta );
               ecal_TP_or_recHit_phi->Fill( phi );

               // Fill Tree
               id = hit.id();
               iEta = id.ieta();
               iPhi = id.iphi();
               treeinfo.ecalHit_energy.push_back( energy );
               treeinfo.ecalHit_et.push_back( et );
               treeinfo.ecalHit_eta.push_back( eta );
               treeinfo.ecalHit_phi.push_back( phi );
               treeinfo.ecalHit_iEta.push_back( iEta );
               treeinfo.ecalHit_iPhi.push_back( iPhi );

               //if (energy > highestE) {
               //   highestE = energy;
               //   highestPhi = phi;
               //   highestEta = eta;
               //}
            }
         }
      }
   }

   if (useEcalTPs) {
      edm::Handle<EcalEBTrigPrimDigiCollection> pcalohits;
      iEvent.getByToken(ecalTPEBToken_,pcalohits);
      for(auto& hit : *pcalohits.product())
      {
         e_totTP++;
         if(hit.encodedEt() > 0) // && !hit.l1aSpike()) // hit.encodedEt() returns an int corresponding to 8x the crystal Et, saturates at 128
         {
            e_totNonZeroTP++;
            auto cell = geometryHelper.getEcalBarrelGeometry()->getGeometry(hit.id());
            position = GlobalVector(cell->getPosition().x(), cell->getPosition().y(), cell->getPosition().z());
            et = hit.encodedEt()/8.;
            energy = et / sin(position.theta());
            eta = cell->getPosition().eta();
            phi = cell->getPosition().phi();
            ecal_TP_or_recHit_et->Fill( et );
            ecal_TP_or_recHit_energy->Fill( energy );
            ecal_TP_or_recHit_eta->Fill( eta );
            ecal_TP_or_recHit_phi->Fill( phi );

            // Fill Tree
            id = hit.id();
            iEta = id.ieta();
            iPhi = id.iphi();
            treeinfo.ecalHit_energy.push_back( energy );
            treeinfo.ecalHit_et.push_back( et );
            treeinfo.ecalHit_eta.push_back( eta );
            treeinfo.ecalHit_phi.push_back( phi );
            treeinfo.ecalHit_iEta.push_back( iEta );
            treeinfo.ecalHit_iPhi.push_back( iPhi );

            //if (energy > highestE) {
            //   highestE = energy;
            //   highestPhi = phi;
            //   highestEta = eta;
            //}
         }
      }
   }

   // Retrive HCAL hits 
   if (useRecHits) {
      edm::Handle<HBHERecHitCollection> pcalohits;
      iEvent.getByToken(hcalRecHitToken_,pcalohits);
      for(auto& hit : *pcalohits.product())
      {
         // We need to cut out the endcap HCAL here before counting raw total
         auto cell = geometryHelper.getHcalGeometry()->getGeometry(hit.id());
         position = GlobalVector(cell->getPosition().x(), cell->getPosition().y(), cell->getPosition().z());
         eta = cell->getPosition().eta();
         if (fabs(eta) > 1.5) continue;

         h_totTP++;
         // Because we need position to calculate Et, skim a little first for Energy > 500 MeV
         // then figure out Et for comparison with ECAL TPs
         if(hit.energy() > 0.2)
         {
            energy = hit.energy();
            et = energy * sin(position.theta());
            if (et > 0.5) {
               h_totNonZeroTP++;
               phi = cell->getPosition().phi();
               hcal_TP_or_recHit_et->Fill( et );
               hcal_TP_or_recHit_energy->Fill( energy );
               hcal_TP_or_recHit_eta->Fill( eta );
               hcal_TP_or_recHit_phi->Fill( phi );

               // Fill Tree
               id = hit.id();
               iEta = id.ieta();
               iPhi = id.iphi();
               treeinfo.hcalHit_energy.push_back( energy );
               treeinfo.hcalHit_et.push_back( et );
               treeinfo.hcalHit_eta.push_back( eta );
               treeinfo.hcalHit_phi.push_back( phi );
               treeinfo.hcalHit_iEta.push_back( iEta );
               treeinfo.hcalHit_iPhi.push_back( iPhi );

               //if (energy > highestE) {
               //   highestE = energy;
               //   highestPhi = phi;
               //   highestEta = eta;
               //}
            }
         }
      }
   }

   // Now fill
   ecal_totalHits->Fill( e_totTP ); 
   ecal_totalNonZeroHits->Fill( e_totNonZeroTP ); 
   hcal_totalHits->Fill( h_totTP ); 
   hcal_totalNonZeroHits->Fill( h_totNonZeroTP ); 


   if (hasGenInfo) {
      edm::Handle<reco::GenParticleCollection> genParticleHandle;
      iEvent.getByToken(genCollectionToken_,genParticleHandle);
      genParticles = *genParticleHandle.product();
      int hitNum = 0;
      for(auto& hit : genParticles)
      {
         // Currently memory use for gen particles is so low,
         // don't worry about filtering these out yet.
         //eta = hit.eta();
         //if (fabs(eta) > 1.5) continue;
         hitNum++;
         //std::cout << "genP hit " << hitNum << " pt: " << hit.pt() <<
         //       " eta: " << hit.eta() << " phi: " << hit.phi() << 
         //       " pdgId: " << hit.pdgId() << " status: " <<
         //       hit.status() << " fromHardProcFS " << 
         //       hit.fromHardProcessFinalState() << std::endl;

         treeinfo.genParticle_energy.push_back( hit.energy() );
         treeinfo.genParticle_pt.push_back( hit.pt() );
         treeinfo.genParticle_eta.push_back( hit.eta() );
         treeinfo.genParticle_phi.push_back( hit.phi() );
         treeinfo.genParticle_pdgId.push_back( hit.pdgId() );
      }
   }


   // Fill TTree
   hit_tree->Fill();

   //std::cout << treeinfo.event << ":  highest hit energy: " << highestE <<
   //     "  phi: " << highestPhi << "  eta: " << highestEta << std::endl;


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
HitAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HitAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
HitAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
HitAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
HitAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
HitAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
HitAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HitAnalyzer);

