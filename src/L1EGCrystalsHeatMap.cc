// -*- C++ -*-
//
// Package:    L1EGCrystalsHeatMap
// Class:      L1EGCrystalsHeatMap
// 
/**\class L1EGCrystalsHeatMap L1EGCrystalsHeatMap.cc SLHCUpgradeSimulations/L1EGCrystalsHeatMap/src/L1EGCrystalsHeatMap.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Nick Smith
//         Created:  Mon Apr  7 19:20:22 CDT 2014
// $Id$
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

#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "SimDataFormats/CaloHit/interface/PCaloHitContainer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/EcalAlgo/interface/EcalBarrelGeometry.h"
#include "Geometry/EcalAlgo/interface/EcalEndcapGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include <iostream>

#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "FastSimulation/CaloGeometryTools/interface/CaloGeometryHelper.h"
#include "SimDataFormats/SLHC/interface/L1EGCrystalCluster.h"
#include "Geometry/CaloTopology/interface/CaloTopology.h"

#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "SimDataFormats/CaloTest/interface/HcalTestNumbering.h"
#include "DataFormats/HcalDetId/interface/HcalSubdetector.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalSourcePositionData.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"
#include "TVector3.h"

//
// Define some structs
//
namespace l1slhc {
   class L1EGCrystalClusterTest {
      public:
         float et ;
         float eta ;
         float phi ;
         float e ;
         float x ;
         float y ;
         float z ;
         float hovere ;

         float ECALiso ;
         float ECALetPUcorr;
         bool marked=false;
         bool isoMarked=false;
   };
}

//
// class declaration
//

class L1EGCrystalsHeatMap : public edm::EDAnalyzer {
   public:
      explicit L1EGCrystalsHeatMap(const edm::ParameterSet&);
      ~L1EGCrystalsHeatMap();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      //virtual void endRun(edm::Run const&, edm::EventSetup const&);
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------
      CaloGeometryHelper myGeometry;
      bool DEBUG;
      int nEvents = 0;
      std::vector<TH2F*> heatmaps;
      std::vector<int> heatmap_nevents;
      class EcalHit{
         public:
            EBDetId id;
            GlobalPoint position;
            double energy=0.;
            inline double pt(){return energy*sin(position.theta());};
            inline double deta(EcalHit& other){return position.eta() - other.position.eta();};
            int dieta(EcalHit& other){
               // int indices do not contain zero
               // Logic from EBDetId::distanceEta() without the abs()
               if (id.ieta() * other.id.ieta() > 0)
                  return id.ieta()-other.id.ieta();
               return id.ieta()-other.id.ieta()-1;
            };
            inline double dphi(EcalHit& other){return reco::deltaPhi(position.phi(), other.position.phi());};
            inline int diphi(EcalHit& other){
               // Logic from EBDetId::distancePhi() without the abs()
               int PI = 180;
               int  result = id.iphi() - other.id.iphi();
               while  (result > PI)    result -= 2*PI;
               while  (result <= -PI)  result += 2*PI;
               return result;
            };
            bool operator==(EcalHit& other) {
               if ( id == other.id &&
                    position == other.position &&
                    energy == other.energy ) {
                  return true;
               }
               return false;
            };
      };
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
L1EGCrystalsHeatMap::L1EGCrystalsHeatMap(const edm::ParameterSet& iConfig)
{
   DEBUG = iConfig.getParameter<bool>("DEBUG");
   
   edm::Service<TFileService> fs;

   heatmaps.resize(5);
   heatmap_nevents.resize(5);
   for(int i=0; i<5; i++) {
      double ptlow = i*10;
      double pthigh = (i+1)*10;
      std::string name = "heatmap_pt"+std::to_string(i);
      std::stringstream title;
      title << "Single-electron pt Heatmap (" << ptlow << "<pt<" << pthigh << ");d#eta (int.);d#phi (int.)";
      heatmaps[i] = fs->make<TH2F>(name.c_str(), title.str().c_str(), 21, -11, 11, 21, -11, 11);
      heatmap_nevents[i] = 0;
   }
}


L1EGCrystalsHeatMap::~L1EGCrystalsHeatMap()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1EGCrystalsHeatMap::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   
   if (nEvents == 0) {
      edm::ESHandle<CaloTopology> theCaloTopology;
      iSetup.get<CaloTopologyRecord>().get(theCaloTopology);       
      edm::ESHandle<CaloGeometry> pG;
      iSetup.get<CaloGeometryRecord>().get(pG);     
      // Setup the tools
      double bField000 = 4.;
      myGeometry.setupGeometry(*pG);
      myGeometry.setupTopology(*theCaloTopology);
      myGeometry.initialize(bField000);
   }
   nEvents++;

   std::vector<EcalHit> ecalhits;
   std::vector<l1slhc::L1EGCrystalClusterTest> hcalhits;

   // Retrieve the SimHits.
   // Sasha's FAMOS :
   // edm::Handle<edm::PCaloHitContainer> pcalohits;
   // iEvent.getByLabel("famosSimHits","EcalHitsEB",pcalohits);
   // using RecHits (https://cmssdt.cern.ch/SDT/doxygen/CMSSW_6_1_2_SLHC6/doc/html/d8/dc9/classEcalRecHit.html)
   edm::Handle<EcalRecHitCollection> pcalohits;
   iEvent.getByLabel("ecalRecHit","EcalRecHitsEB",pcalohits);
   // Geant's pcaloHits :
   // edm::Handle<edm::PCaloHitContainer> pcalohits;
   // iEvent.getByLabel("g4SimHits","EcalHitsEB",pcalohits);

   for(auto hit : *pcalohits.product())
   {
      if(hit.energy() > 0.2)
      {
         auto cell = myGeometry.getEcalBarrelGeometry()->getGeometry(hit.id());
         EcalHit ehit;
         ehit.id = hit.id();
         ehit.position = cell->getPosition();
         ehit.energy = hit.energy();
         ecalhits.push_back(ehit);
         //std::cout << " EB Hits " <<  hit.energy() <<  " iphi " << hit.id.iphi() << " ieta " << hit.id.ieta() << " eta " << ehit.position.eta() << std::endl;
      }
   }

   edm::ESHandle<CaloGeometry> pG1;
   iSetup.get<CaloGeometryRecord>().get(pG1);
   const CaloGeometry* geometry = pG1.product();

   edm::Handle<HBHERecHitCollection> hbhecoll;
   iEvent.getByLabel("hbheprereco", hbhecoll);

   for (HBHERecHitCollection::const_iterator j=hbhecoll->begin(); j != hbhecoll->end(); j++) {
      HcalDetId cell(j->id());
      const CaloCellGeometry* cellGeometry = geometry->getSubdetectorGeometry(cell)->getGeometry(cell);
      if ( j->energy() > 0.1 )
      {
         l1slhc::L1EGCrystalClusterTest cluster_hit;
         cluster_hit.e = (j->energy()) ;      
         cluster_hit.eta = cellGeometry->getPosition().eta() ;
         cluster_hit.phi = cellGeometry->getPosition().phi() ;
         hcalhits.push_back(cluster_hit);
         if(DEBUG && cluster_hit.e > 10) std::cout << " id " << cell << " Energy " << j->energy() << " eta " << cluster_hit.eta << " phi " << cluster_hit.phi <<  std::endl ;
      }
   }
   
   // Get generated electron
   edm::Handle<reco::GenParticleCollection> genParticleHandle;
   iEvent.getByLabel("genParticles", genParticleHandle);
   reco::GenParticleCollection genParticles = *genParticleHandle.product();
   if ( fabs(genParticles[0].eta()) > 1.46 ) {
      // Don't consider generated electrons in the endcap
      nEvents--;
      return;
   }
   
   // Find closest crystal
   double dRmin = 999.;
   EcalHit centerhit;
   for(auto ecalhit : ecalhits)
   {
      if ( reco::deltaR(ecalhit.position, genParticles[0].polarP4()) < dRmin )
      {
         dRmin = reco::deltaR(ecalhit.position, genParticles[0].polarP4());
         centerhit = ecalhit;
      }
   }

   // Fill heatmap
   for(int i=0; i<5; i++)
   {
      double ptlow = i*10;
      double pthigh = (i+1)*10;
      if ( genParticles[0].pt() > ptlow && genParticles[0].pt() <= pthigh )
      {
         heatmap_nevents[i]++;
         for(auto ecalhit : ecalhits)
         {
            if ( fabs(ecalhit.deta(centerhit)) < 0.2 && fabs(ecalhit.dphi(centerhit)) < 0.2 )
            {
               heatmaps[i]->Fill(ecalhit.dieta(centerhit), ecalhit.diphi(centerhit), ecalhit.pt());
            }
         }
      }
   }
   
   // Make a cluster
   std::vector<EcalHit> cluster;
   for(auto ecalhit : ecalhits)
   {
      if ( fabs(ecalhit.dieta(centerhit)) < 3 && fabs(ecalhit.diphi(centerhit)) < 5 )
      {
         cluster.push_back(ecalhit);
      }
   }
   
   // Print cluster
   std::sort(std::begin(cluster), std::end(cluster), [](EcalHit a, EcalHit b){return a.pt() > b.pt();});
   std::cout << "Cluster around genParticle with pT=" << genParticles[0].pt() << ", eta=" << genParticles[0].eta() << ", phi=" << genParticles[0].phi() << std::endl;
   for(auto hit : cluster)
   {
      if ( hit == centerhit )
         std::cout << "\x1B[32m"; // green hilight
      std::cout << "\tCrystal (" << hit.dieta(centerhit) << "," << hit.diphi(centerhit) << ") pt=" << hit.pt() << ", eta=" << hit.position.eta() << ", phi=" << hit.position.phi() << "\x1B[0m" << std::endl;
   }
}

// ------------ method called once each job just before starting event loop  ------------
void 
L1EGCrystalsHeatMap::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1EGCrystalsHeatMap::endJob() 
{
   // Scale heatmaps by # events added
   for(int i=0; i<5; i++)
   {
      if ( heatmap_nevents[i] > 0 )
         heatmaps[i]->Scale(1./heatmap_nevents[i]);
   }
}

// ------------ method called when starting to processes a run  ------------
/*
void 
L1EGCrystalsHeatMap::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1EGCrystalsHeatMap::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1EGCrystalsHeatMap::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1EGCrystalsHeatMap::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1EGCrystalsHeatMap::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGCrystalsHeatMap);
