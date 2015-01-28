// -*- C++ -*-
//
// Package:    L1EGCrystalsHeatMap
// Class:      L1EGCrystalsHeatMap
// 
/**\class L1EGCrystalsHeatMap L1EGCrystalsHeatMap.cc SLHCUpgradeSimulations/L1EGRateStudies/src/L1EGCrystalsHeatMap.cc

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

#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"
#include "TH1.h"
#include "TH2.h"
#include "TVector3.h"
#include "TRandom3.h"

#include "FastSimulation/BaseParticlePropagator/interface/BaseParticlePropagator.h"
#include "FastSimulation/Particle/interface/ParticleTable.h"

#include "DataFormats/EcalDigi/interface/EcalDigiCollections.h"
//
// class declaration
//

class L1EGCrystalsHeatMap : public edm::EDAnalyzer {
   public:
      explicit L1EGCrystalsHeatMap(const edm::ParameterSet&);
      ~L1EGCrystalsHeatMap();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      class SimpleCaloHit
      {
         public:
            EBDetId id;
            GlobalPoint position;
            double energy=0.;
            inline double pt() const{return energy*sin(position.theta());};
            inline double deta(SimpleCaloHit& other){return position.eta() - other.position.eta();};
            int dieta(SimpleCaloHit& other) const
            {
               // int indices do not contain zero
               // Logic from EBDetId::distanceEta() without the abs()
               if (id.ieta() * other.id.ieta() > 0)
                  return id.ieta()-other.id.ieta();
               return id.ieta()-other.id.ieta()-1;
            };
            inline double dphi(SimpleCaloHit& other){return reco::deltaPhi(position.phi(), other.position.phi());};
            inline int diphi(SimpleCaloHit& other) const
            {
               // Logic from EBDetId::distancePhi() without the abs()
               int PI = 180;
               int  result = id.iphi() - other.id.iphi();
               while  (result > PI)    result -= 2*PI;
               while  (result <= -PI)  result += 2*PI;
               return result;
            };
            bool operator==(SimpleCaloHit& other)
            {
               if ( id == other.id &&
                    position == other.position &&
                    energy == other.energy
                  ) return true;
                  
               return false;
            };
      };
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      bool cluster_passes_cuts(const l1slhc::L1EGCrystalCluster& cluster);
      void fillHeatmap(std::string name, SimpleCaloHit &centerHit);
      SimpleCaloHit& findClosestHit(reco::Candidate &cluster);
      SimpleCaloHit& findClosestHit(l1slhc::L1EGCrystalCluster &cluster);

      // ----------member data ---------------------------
      CaloGeometryHelper geometryHelper;
      int range_;
      bool useEndcap;
      bool useOfflineClusters;
      bool kDebug;
      bool kUseGenMatch;
      bool kSaveAllClusters;
      double kClusterPtCut; 
      edm::InputTag L1CrystalClustersInputTag;
      std::vector<edm::InputTag> L1EGammaOtherAlgs;
      std::map<std::string, TH2F*> heatmaps_;
      TH1I * fakeStatus;
      TH2F * crystalTowerComparison;
      std::map<std::string, int> heatmap_nevents_;
      std::vector<SimpleCaloHit> ecalhits_;
      std::vector<SimpleCaloHit> hcalhits_;
      std::unique_ptr<TRandom3> rng;
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
L1EGCrystalsHeatMap::L1EGCrystalsHeatMap(const edm::ParameterSet& iConfig):
   range_(iConfig.getUntrackedParameter<int>("range", 10)),
   useEndcap(iConfig.getUntrackedParameter<bool>("useEndcap", false)),
   useOfflineClusters(iConfig.getUntrackedParameter<bool>("useOfflineClusters", false)),
   kDebug(iConfig.getUntrackedParameter<bool>("debug", false)),
   kUseGenMatch(iConfig.getUntrackedParameter<bool>("useGenMatch", true)),
   kSaveAllClusters(iConfig.getUntrackedParameter<bool>("saveAllClusters", false)),
   kClusterPtCut(iConfig.getUntrackedParameter<double>("clusterPtCut", 10.))
{
   L1CrystalClustersInputTag = iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag");
   L1EGammaOtherAlgs = iConfig.getParameter<std::vector<edm::InputTag>>("L1EGammaOtherAlgs");
   edm::Service<TFileService> fs;
   fakeStatus = fs->make<TH1I>("fakeStatus", "Fake statuses", 10, 0, 9);
   crystalTowerComparison = fs->make<TH2F>("crystalTowerComparison", "Crystal cluster pt vs. nearest tower pt", 50, 0., 50., 50, 0., 50.);
   rng= std::move(std::unique_ptr<TRandom3>(new TRandom3()));
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

   if ( geometryHelper.getEcalBarrelGeometry() == nullptr )
   {
      edm::ESHandle<CaloTopology> theCaloTopology;
      iSetup.get<CaloTopologyRecord>().get(theCaloTopology);
      edm::ESHandle<CaloGeometry> pG;
      iSetup.get<CaloGeometryRecord>().get(pG);
      double bField000 = 4.;
      geometryHelper.setupGeometry(*pG);
      geometryHelper.setupTopology(*theCaloTopology);
      geometryHelper.initialize(bField000);
   }

   ecalhits_.clear();
   hcalhits_.clear();

   // Retrieve the ecal barrel hits
   // using RecHits (https://cmssdt.cern.ch/SDT/doxygen/CMSSW_6_1_2_SLHC6/doc/html/d8/dc9/classEcalRecHit.html)
   edm::Handle<EcalRecHitCollection> pcalohits;
   iEvent.getByLabel("ecalRecHit","EcalRecHitsEB",pcalohits);
   for(auto hit : *pcalohits.product())
   {
      if(hit.energy() > 0.2)
      {
         auto cell = geometryHelper.getEcalBarrelGeometry()->getGeometry(hit.id());
         SimpleCaloHit ehit;
         ehit.id = hit.id();
         ehit.position = cell->getPosition();
         ehit.energy = hit.energy();
         ecalhits_.push_back(ehit);
      }
   }

   // Retrive hcal hits
   edm::Handle<HBHERecHitCollection> hbhecoll;
   iEvent.getByLabel("hbheprereco", hbhecoll);
   for (auto hit : *hbhecoll.product())
   {
      if ( hit.energy() > 0.1 )
      {
         auto cell = geometryHelper.getHcalGeometry()->getGeometry(hit.id());
         SimpleCaloHit hhit;
         hhit.id = hit.id();
         hhit.position = cell->getPosition();
         hhit.energy = hit.energy();
         hcalhits_.push_back(hhit);
      }
   }
   
   // Load EG Crystal clusters
   l1slhc::L1EGCrystalClusterCollection crystalClusters;
   edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersHandle;      
   iEvent.getByLabel(L1CrystalClustersInputTag,crystalClustersHandle);
   crystalClusters = (*crystalClustersHandle.product());
   std::sort(begin(crystalClusters), end(crystalClusters), [](const l1slhc::L1EGCrystalCluster& a, const l1slhc::L1EGCrystalCluster& b){return a.pt() > b.pt();});

   // Load other algorithm products
   l1extra::L1EmParticleCollection EGClusters;
   for(const auto& tag : L1EGammaOtherAlgs)
   {
      edm::Handle<l1extra::L1EmParticleCollection> EGClustersHandle;
      iEvent.getByLabel(tag, EGClustersHandle);
      EGClusters.insert(begin(EGClusters), begin(*EGClustersHandle.product()), end(*EGClustersHandle.product()));
   }
   std::sort(begin(EGClusters), end(EGClusters), [](const l1extra::L1EmParticle& a, const l1extra::L1EmParticle& b){return a.pt() > b.pt();});

   reco::Candidate::PolarLorentzVector trueElectron;
   if (kUseGenMatch) {
      // Get generated electron
      edm::Handle<reco::GenParticleCollection> genParticleHandle;
      reco::GenParticleCollection genParticles;
      iEvent.getByLabel("genParticles", genParticleHandle);
      genParticles = *genParticleHandle.product();

      // Get the particle position upon entering ECal
      RawParticle particle(genParticles[0].p4());
      particle.setVertex(genParticles[0].vertex().x(), genParticles[0].vertex().y(), genParticles[0].vertex().z(), 0.);
      particle.setID(genParticles[0].pdgId());
      BaseParticlePropagator prop(particle, 0., 0., 4.);
      BaseParticlePropagator start(prop);
      prop.propagateToEcalEntrance();
      if(prop.getSuccess()!=0)
      {
         trueElectron = reco::Candidate::PolarLorentzVector(prop.E()*sin(prop.vertex().theta()), prop.vertex().eta(), prop.vertex().phi(), 0.);
         if ( kDebug ) std::cout << "Propogated genParticle to ECal, position: " << prop.vertex() << " momentum = " << prop.momentum() << std::endl;
         if ( kDebug ) std::cout << "                       starting position: " << start.vertex() << " momentum = " << start.momentum() << std::endl;
         if ( kDebug ) std::cout << "                    genParticle position: " << genParticles[0].vertex() << " momentum = " << genParticles[0].p4() << std::endl;
         if ( kDebug ) std::cout << "       old pt = " << genParticles[0].pt() << ", new pt = " << trueElectron.pt() << std::endl;
      }
      else
      {
         // something failed?
         trueElectron = genParticles[0].polarP4();
      }
      
      if ( !useEndcap && fabs(trueElectron.eta()) > 1.479 )
      {
         // Don't consider generated electrons in the endcap
         return;
      }

      for(auto& cluster : crystalClusters)
      {
         if ( reco::deltaR(trueElectron, cluster) < 0.1 )
         {
            if ( cluster.pt() < 20. && trueElectron.pt() > 20. )
            {
               std::cout << "find_me!" << std::endl;
               fillHeatmap("cluster_pt<20,gen_pt>20", findClosestHit(cluster));
            }
            if ( cluster.pt() < 20. && trueElectron.pt() > 20. && trueElectron.pt() < 30. )
               fillHeatmap("cluster_pt<20,20<gen_pt<30", findClosestHit(cluster));
            if ( kSaveAllClusters && (cluster.GetExperimentalParam("uncorrectedPt")/trueElectron.pt() < 0.6) && cluster.pt() > 15. )
               fillHeatmap("evt"+std::to_string(iEvent.id().event())+"_cluster"+std::to_string(reco::deltaR(trueElectron, cluster))+"_pt"+std::to_string(cluster.pt())+"_nCrystals"+std::to_string(cluster.GetExperimentalParam("crystalCount")), findClosestHit(cluster));
            break;
         }
      }
   }
   else // !kUseGenMatch
   {
      int clusterIndex = -1;
      for(auto& cluster : crystalClusters)
      {
         clusterIndex++;
         if ( cluster.pt() < kClusterPtCut ) continue;
         bool otherAlgMatchFound = false;
         l1extra::L1EmParticle run1Cand;
         for(const auto& candidate : EGClusters)
         {
            if ( reco::deltaR(candidate, cluster) < 0.25 )
            {
               otherAlgMatchFound = true;
               run1Cand = candidate;
               break;
            }
         }
         if ( cluster_passes_cuts(cluster) && !otherAlgMatchFound )
         {
            trueElectron = cluster.polarP4();
            std::cout << "No match in old algs for crystal alg pt: " << cluster.pt() << " eta: " << cluster.eta() << " phi: " << cluster.phi() << std::endl;

            // Look at tpgs
            edm::Handle<EcalTrigPrimDigiCollection> tpgH;
            iEvent.getByLabel(edm::InputTag("ecalDigis:EcalTriggerPrimitives"), tpgH);
            EcalTrigPrimDigiCollection tpgs = *tpgH.product();
            auto &seedHit = findClosestHit(cluster);
            for(const auto& tpg : tpgs)
            {
               if ( seedHit.id.tower() == tpg.id() )
               {
                  std::cout << "Found tower for seed hit, et: " << tpg.compressedEt()*0.5 << std::endl;
                  crystalTowerComparison->Fill(cluster.pt(), tpg.compressedEt()*0.5);                  
                  if ( tpg.compressedEt() == 0 )
                  {
                     fillHeatmap("crystal_notowerEt", seedHit);
                     fakeStatus->Fill(1);
                  }
                  else
                  {
                     fillHeatmap("crystal_towerEt", seedHit);
                     fakeStatus->Fill(2);
                  }
                  double etSum = 0.;
                  for(const auto& hit : ecalhits_)
                  {
                     if ( hit.id.tower() == tpg.id() )
                     {
                        etSum += hit.pt();
                        std::cout << "   hit in tower, et: " << hit.pt() << std::endl;
                     }
                  }
                  std::cout << "Total et found in tower: " << etSum << std::endl;
               }
            }
            break;
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
   // Scale heatmaps_ by # events added
   for(auto& pair : heatmaps_)
   {
      auto& name = pair.first;
      std::cout << "Heatmap " << name << " has " << heatmap_nevents_[name] << " events." << std::endl;
      if ( heatmap_nevents_[name] > 0 )
         heatmaps_[name]->Scale(1./heatmap_nevents_[name]);
   }
}

// ------------ method called when starting to processes a run  ------------
void 
L1EGCrystalsHeatMap::beginRun(edm::Run const& iRun, edm::EventSetup const& es)
{
   edm::ESHandle<HepPDT::ParticleDataTable> pdt;
   es.getData(pdt);
   if ( !ParticleTable::instance() ) ParticleTable::instance(&(*pdt));
}

void
L1EGCrystalsHeatMap::fillHeatmap(std::string name, SimpleCaloHit &centerHit)
{
   if ( heatmap_nevents_[name] == 0)
   {
      edm::Service<TFileService> fs;
      heatmaps_[name] = fs->make<TH2F>(name.c_str(), name.c_str(), 2*range_+1, -range_-.5, range_+.5, 2*range_+1, -range_-.5, range_+.5);
   }
   heatmap_nevents_[name]++;
   for(const auto& ecalhit : ecalhits_)
   {
      if ( abs(ecalhit.dieta(centerHit)) <= range_ && abs(ecalhit.diphi(centerHit)) <= range_ )
      {
         heatmaps_[name]->Fill(ecalhit.dieta(centerHit), ecalhit.diphi(centerHit), ecalhit.pt());
      }
   }
}

L1EGCrystalsHeatMap::SimpleCaloHit&
L1EGCrystalsHeatMap::findClosestHit(reco::Candidate &cluster)
{
   double dRmin = 999.;
   SimpleCaloHit *centerhit = &ecalhits_[0];
   for(auto& ecalhit : ecalhits_)
   {
      if ( reco::deltaR(ecalhit.position, cluster) < dRmin )
      {
         dRmin = reco::deltaR(ecalhit.position, cluster);
         centerhit = &ecalhit;
      }
   }
   // centerhit should never be null as long as ecalhits_ has entries
   return *centerhit;
}

L1EGCrystalsHeatMap::SimpleCaloHit&
L1EGCrystalsHeatMap::findClosestHit(l1slhc::L1EGCrystalCluster &cluster)
{
   SimpleCaloHit *centerhit = &ecalhits_[0];
   for(auto& ecalhit : ecalhits_)
   {
      if ( ecalhit.id == cluster.seedCrystal() )
      {
         centerhit = &ecalhit;
      }
   }
   // centerhit should never be null as long as ecalhits_ has entries
   return *centerhit;
}

bool
L1EGCrystalsHeatMap::cluster_passes_cuts(const l1slhc::L1EGCrystalCluster& cluster) {
   if ( cluster.hovere() < 14./cluster.pt()+0.05
        && cluster.isolation() < 40./cluster.pt()+0.1
        && (cluster.GetCrystalPt(4)/(cluster.GetCrystalPt(0)+cluster.GetCrystalPt(1)) < ( (cluster.pt() < 20) ? 0.08:0.08*(1+(cluster.pt()-20)/25.) ) )
        && ((cluster.pt() > 10) ? (cluster.GetCrystalPt(4)/(cluster.GetCrystalPt(0)+cluster.GetCrystalPt(1)) > 0.):true) )
   {
      return true;
   }
   return false;
}


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
