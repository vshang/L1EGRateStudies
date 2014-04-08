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
      std::vector<l1slhc::L1EGCrystalClusterTest> ecalhits;
      std::vector<l1slhc::L1EGCrystalClusterTest> hcalhits;
      bool DEBUG;
      bool First = true;
      TH2F * heatmap;
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
   heatmap = fs->make<TH2F>("heatmap", "Heatmap;d#eta;d#phi", 50, -0.3, 0.3, 50, -0.3, 0.3);
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
   
   if (First) {
      edm::ESHandle<CaloTopology> theCaloTopology;
      iSetup.get<CaloTopologyRecord>().get(theCaloTopology);       
      edm::ESHandle<CaloGeometry> pG;
      iSetup.get<CaloGeometryRecord>().get(pG);     
      // Setup the tools
      double bField000 = 4.;
      myGeometry.setupGeometry(*pG);
      myGeometry.setupTopology(*theCaloTopology);
      myGeometry.initialize(bField000);
      First = false ;
   }

   // Retrieve the SimHits.
   // Sasha's FAMOS :
   //edm::Handle<edm::PCaloHitContainer> pcalohits;
   //iEvent.getByLabel("famosSimHits","EcalHitsEB",pcalohits);
   // using RecHits :
   edm::Handle<EcalRecHitCollection> pcalohits;
   iEvent.getByLabel("ecalRecHit","EcalRecHitsEB",pcalohits);
   // Geant's pcaloHits :
   //// edm::Handle<edm::PCaloHitContainer> pcalohits;
   //// iEvent.getByLabel("g4SimHits","EcalHitsEB",pcalohits);

   for(auto hit : *pcalohits.product())
   {
      if(hit.energy() > 0.2)
      {
         EBDetId EBid = EBDetId(hit.id()) ;
         auto cell = myGeometry.getEcalBarrelGeometry()->getGeometry(hit.id());
         double theta =  cell->getPosition().theta() ;
         double phi =  cell->getPosition().phi() ;
         double eta = -1.*log(tan(theta/2.)) ;
         l1slhc::L1EGCrystalClusterTest cluster_hit;
         cluster_hit.et = (hit.energy())*sin(theta) ;
         cluster_hit.eta = eta ;
         cluster_hit.phi = phi ;
         cluster_hit.e = hit.energy() ;
         cluster_hit.x = cell->getPosition().x() ;
         cluster_hit.y = cell->getPosition().y() ;
         cluster_hit.z = cell->getPosition().z() ;
         ecalhits.push_back(cluster_hit);
         if (DEBUG) std::cout << " EB Hits " <<  hit.energy() <<  " phi " << phi << " eta " << eta << " eta1 " << EBid.ieta() << " theta " << theta << std::endl;
      }
   }

   //iEvent.getByLabel("famosSimHits","EcalHitsEE",pcalohits);
   iEvent.getByLabel("ecalRecHit","EcalRecHitsEE",pcalohits);
   // iEvent.getByLabel("g4SimHits","EcalHitsEE",pcalohits);

   for(auto hit : *pcalohits.product())
   {
      if(hit.energy() > 0.2)
      {
         double theta =  myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().theta() ;
         double phi =  myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().phi() ;
         double eta = -1.*log(tan(theta/2.)) ;
         l1slhc::L1EGCrystalClusterTest cluster_hit;
         cluster_hit.et = (hit.energy())*sin(theta);
         cluster_hit.eta = eta ;
         cluster_hit.phi = phi ;
         cluster_hit.e = (hit.energy()) ;
         cluster_hit.x = myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().x() ;
         cluster_hit.y = myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().y() ;
         cluster_hit.z = myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().z() ;
         ecalhits.push_back(cluster_hit);
         if (DEBUG) std::cout << " EE Hits " << " energy " << hit.energy() << " phi " << phi << " eta " << eta <<  std::endl;
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
   
   // Find a cluster that 
   // matches to gen particle
   edm::Handle<reco::GenParticleCollection> genParticleHandle;
   iEvent.getByLabel("genParticles", genParticleHandle);
   reco::GenParticleCollection genParticles = *genParticleHandle.product();
   float Etmax = 0 ;
   while( Etmax != 2.)
   {
      Etmax = 2. ;
      auto centerhit = std::begin(ecalhits);
      for(auto ecalhit=std::begin(ecalhits); ecalhit!=std::end(ecalhits); ecalhit++)
      {
         if( !ecalhit->marked && ecalhit->et > Etmax)
         {
            Etmax = ecalhit->et;
            centerhit = ecalhit;
         }
      } 

      if( Etmax != 2. )
      {
         float Total_E = 0;
         float Weightedx = 0;
         float Weightedy = 0;
         float Weightedz = 0;
         for(auto ecalhit : ecalhits)
         {
            if ( !ecalhit.marked && fabs(centerhit->eta-ecalhit.eta) < 0.08 && fabs(centerhit->phi-ecalhit.phi) < 0.1 )
            {
               Total_E = Total_E + ecalhit.e ;
               Weightedx = Weightedx + ecalhit.x*ecalhit.e;
               Weightedy = Weightedy + ecalhit.y*ecalhit.e;
               Weightedz = Weightedz + ecalhit.z*ecalhit.e;
               ecalhit.marked = true;
            }
         }
         l1slhc::L1EGCrystalClusterTest cluster;
         cluster.e = Total_E ;
         cluster.x = Weightedx/Total_E ;
         cluster.y = Weightedy/Total_E ;
         cluster.z = Weightedz/Total_E ;
         TVector3 tmp(cluster.x,cluster.y,cluster.z) ;
         cluster.phi = tmp.Phi() ;
         cluster.eta = tmp.PseudoRapidity() ;
         cluster.et = Total_E*sin(tmp.Theta()) ;
         if (DEBUG) {
            std::cout << " clusters " << Total_E << " et " << cluster.et << " phi " << cluster.phi << " eta " << cluster.eta <<  std::endl ;
         }

         // calculate isolation and pileup-corrected et (where is this defined?)
         Total_E = 0. ;
         Weightedx = 0 ;
         Weightedy = 0 ;
         Weightedz = 0 ;
         double isoSum = 0;
         for(auto ecalhit : ecalhits)
         {
            if ( !ecalhit.marked && ecalhit.et > 0.05 && fabs(centerhit->eta-ecalhit.eta) < 0.25 && fabs(centerhit->phi-ecalhit.phi) < 0.25 )
            {
               TVector3 tmp(ecalhit.x,ecalhit.y,ecalhit.z);
               isoSum += ecalhit.e*sin(tmp.Theta());
            }
            if ( !ecalhit.marked && ecalhit.et > 0.05 && ecalhit.et < 5. && fabs(centerhit->eta-ecalhit.eta) < 0.12 && fabs(centerhit->phi-ecalhit.phi) < 1. )
            {
               Total_E = Total_E + ecalhit.e ;
               Weightedx = Weightedx + ecalhit.x*ecalhit.e;
               Weightedy = Weightedy + ecalhit.y*ecalhit.e;
               Weightedz = Weightedz + ecalhit.z*ecalhit.e;
            }
         }
         cluster.ECALiso = isoSum/cluster.et ;

         TVector3 tmp1(Weightedx/Total_E,Weightedy/Total_E,Weightedz/Total_E) ;
         cluster.ECALetPUcorr = cluster.et-Total_E*sin(tmp1.Theta())/19. ;

         // calculate hovere
         Total_E = 0 ;
         for(auto hcalhit : hcalhits)
         {
            if ( fabs(centerhit->eta-hcalhit.eta) < 0.15 && fabs(centerhit->phi-hcalhit.phi) < 0.15 )
            {
               Total_E = Total_E + hcalhit.e ;
            }
         }
         cluster.hovere = Total_E/cluster.e ;
         
         reco::Candidate::PolarLorentzVector clusterP4(cluster.et, cluster.eta, cluster.phi, 0.);
         if ( reco::deltaR(clusterP4, genParticles[0].polarP4()) < 0.1 && cluster.et > genParticles[0].pt()/2 ) {
            // quite likely that this is the electron
            
            for(auto ecalhit : ecalhits)
            {
               if ( fabs(centerhit->eta-ecalhit.eta) < 0.08 && fabs(centerhit->phi-ecalhit.phi) < 0.1 )
               {
                  heatmap->Fill(ecalhit.eta, ecalhit.phi);
               }
            }
         }
      }
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
