// -*- C++ -*-
//
// Package:     L1CaloJetStudies
// Class:        L1CaloJetStudies
// 
/**\class L1CaloJetStudies L1CaloJetStudies.cc L1Trigger/L1EGRateStudies/src/L1CaloJetStudies.cc

 Description: [one line class summary]

 Implementation:
      [Notes on implementation]
*/
//
// Original Author:  Tyler Ruggles
//            Created:  Sept 2, 2018
// $Id$
//
//


// system include files
#include <memory>
#include <array>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TTree.h"
#include "TMath.h"

// Gen
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"

#include "DataFormats/Phase2L1CaloTrig/interface/L1CaloJet.h"
#include "DataFormats/Phase2L1CaloTrig/src/classes.h"

#include "FastSimulation/BaseParticlePropagator/interface/BaseParticlePropagator.h"

#include "FastSimulation/Particle/interface/RawParticle.h"

// Stage2
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/L1Trigger/interface/L1Candidate.h"


//
// class declaration
//
class L1CaloJetStudies : public edm::EDAnalyzer {
    typedef BXVector<l1t::EGamma> EGammaBxCollection;
    typedef std::vector<l1t::EGamma> EGammaCollection;

    public:
        explicit L1CaloJetStudies(const edm::ParameterSet&);
        ~L1CaloJetStudies();

        static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


    private:
        virtual void beginJob() ;
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob() ;

        virtual void beginRun(edm::Run const&, edm::EventSetup const&);

        // -- user functions
        void integrateDown(TH1F *);
        void fill_tree(const l1slhc::L1CaloJet& caloJet);
        void fill_tree_null();
        
        // ----------member data ---------------------------
        bool debug;
        
        double genMatchDeltaRcut;
        double genMatchRelPtcut;
        

        edm::EDGetTokenT<l1slhc::L1CaloJetsCollection> caloJetsToken_;
        l1slhc::L1CaloJetsCollection caloJets;
        edm::Handle<l1slhc::L1CaloJetsCollection> caloJetsHandle;        

        //edm::EDGetTokenT<reco::GenParticleCollection> genCollectionToken_;
        //reco::GenParticleCollection genParticles;
        //edm::Handle<reco::GenParticleCollection> genParticleHandle;

        edm::EDGetTokenT<reco::GenJet> genJetsToken_;
        reco::GenJet genJets;
        edm::Handle<reco::GenJet> genJetsHandle;

        // Stage2 Digis
        //edm::EDGetTokenT<BXVector<l1t::EGamma> > stage2egToken1_;
                
        // Crystal pt stuff
        TTree * tree;
        struct {
            double run;
            double lumi;
            double event;
            float ecal_pt;
            float ecal_eta;
            float ecal_phi;
            float ecal_mass;
            float ecal_energy;
            float hcal_pt;
            float hcal_eta;
            float hcal_phi;
            float hcal_mass;
            float hcal_energy;
            float jet_pt;
            float jet_eta;
            float jet_phi;
            float jet_mass;
            float jet_energy;
            float hovere;
            float hcal_dR0p05;
            float hcal_dR0p075;
            float hcal_dR0p1;
            float hcal_dR0p125;
            float hcal_dR0p15;
            float hcal_dR0p2;
            float hcal_dR0p3;
            float hcal_dR0p4;
            float hcal_dR0p5;
            float deltaR;
            float deltaPhi;
            float deltaEta;
            float gen_pt;
            float gen_eta;
            float gen_phi;
            float gen_energy;
            float gen_mass;
            float gen_charge;
        } treeinfo;

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
L1CaloJetStudies::L1CaloJetStudies(const edm::ParameterSet& iConfig) :
    debug(iConfig.getUntrackedParameter<bool>("debug", false)),
    genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.3)),
    genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
    caloJetsToken_(consumes<l1slhc::L1CaloJetsCollection>(iConfig.getParameter<edm::InputTag>("L1CaloJetsInputTag"))),
    genJetsToken_(consumes<reco::GenJet>(iConfig.getParameter<edm::InputTag>("genJets")))
    //stage2egToken1_(consumes<BXVector<l1t::EGamma>>(iConfig.getParameter<edm::InputTag>("Stage2EG1Tag")))
{

    edm::Service<TFileService> fs;

    tree = fs->make<TTree>("tree", "CaloJet values");
    tree->Branch("run", &treeinfo.run);
    tree->Branch("lumi", &treeinfo.lumi);
    tree->Branch("event", &treeinfo.event);
    tree->Branch("ecal_pt", treeinfo.ecal_pt);
    tree->Branch("ecal_eta", treeinfo.ecal_eta);
    tree->Branch("ecal_phi", treeinfo.ecal_phi);
    tree->Branch("ecal_mass", treeinfo.ecal_mass);
    tree->Branch("ecal_energy", treeinfo.ecal_energy);
    tree->Branch("hcal_pt", treeinfo.hcal_pt);
    tree->Branch("hcal_eta", treeinfo.hcal_eta);
    tree->Branch("hcal_phi", treeinfo.hcal_phi);
    tree->Branch("hcal_mass", treeinfo.hcal_mass);
    tree->Branch("hcal_energy", treeinfo.hcal_energy);
    tree->Branch("jet_pt", treeinfo.jet_pt);
    tree->Branch("jet_eta", treeinfo.jet_eta);
    tree->Branch("jet_phi", treeinfo.jet_phi);
    tree->Branch("jet_mass", treeinfo.jet_mass);
    tree->Branch("jet_energy", treeinfo.jet_energy);
    tree->Branch("hovere", treeinfo.hovere);
    tree->Branch("hcal_dR0p05", &treeinfo.hcal_dR0p05);
    tree->Branch("hcal_dR0p075", &treeinfo.hcal_dR0p075);
    tree->Branch("hcal_dR0p1", &treeinfo.hcal_dR0p1);
    tree->Branch("hcal_dR0p125", &treeinfo.hcal_dR0p125);
    tree->Branch("hcal_dR0p15", &treeinfo.hcal_dR0p15);
    tree->Branch("hcal_dR0p2", &treeinfo.hcal_dR0p2);
    tree->Branch("hcal_dR0p3", &treeinfo.hcal_dR0p3);
    tree->Branch("hcal_dR0p4", &treeinfo.hcal_dR0p4);
    tree->Branch("hcal_dR0p5", &treeinfo.hcal_dR0p5);
    tree->Branch("deltaR", &treeinfo.deltaR);
    tree->Branch("deltaPhi", &treeinfo.deltaPhi);
    tree->Branch("deltaEta", &treeinfo.deltaEta);
    tree->Branch("gen_pt", &treeinfo.gen_pt);
    tree->Branch("gen_eta", &treeinfo.gen_eta);
    tree->Branch("gen_phi", &treeinfo.gen_phi);
    tree->Branch("gen_energy", &treeinfo.gen_energy);
    tree->Branch("gen_mass", &treeinfo.gen_mass);
    tree->Branch("gen_charge", &treeinfo.gen_charge);
}


L1CaloJetStudies::~L1CaloJetStudies()
{
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1CaloJetStudies::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;


    // Record the standards
    treeinfo.run = iEvent.eventAuxiliary().run();
    treeinfo.lumi = iEvent.eventAuxiliary().luminosityBlock();
    treeinfo.event = iEvent.eventAuxiliary().event();


    // Get Phase-II CaloJet collection
    iEvent.getByToken(caloJetsToken_,caloJetsHandle);
    caloJets = (*caloJetsHandle.product());

    // Sort caloJets so we can always pick highest pt caloJet matching cuts
    std::sort(begin(caloJets), end(caloJets), [](const l1slhc::L1CaloJet& a, const l1slhc::L1CaloJet& b){return a.pt() > b.pt();});
        

    // Loop over all gen jets with pt > 10 GeV and match them to Phase-II CaloJets
    // Generator info (truth)
    iEvent.getByToken(genJetsToken_,genJetsHandle);
    genJets = *genJetsHandle.product();
    int cnt = 0;
    for (auto& genJet : genJets ) {
        // Skip lowest pT Jets
        if (genJet.pt() < 10) continue;
        // Skip high eta, keep things hear boundary for future study
        if ( fabs(genJet.eta())  > 2.0) continue;
        ++cnt;
        std::cout << cnt << " Gen pT: " << genJet.pt() << std::endl;

        //if ( fabs(genJet.pdgId()) != 11) {
        //      std::cout << "Event without electron as best gen.  Gen pdgId was: " << genJet.pdgId() <<std::endl;
        //      return;
        //}
    
    
        reco::Candidate::PolarLorentzVector genJetP4(genJet.pt(), genJet.eta(), genJet.phi(), genJet.mass() );
    
    
        //// Stage-2
        //edm::Handle<BXVector<l1t::EGamma>> stage2eg1Handle;
        //iEvent.getByToken(stage2egToken1_, stage2eg1Handle);
        //EGammaBxCollection stage2BXEGs;
        //EGammaCollection stage2EGs;
        //if ( stage2eg1Handle.isValid() )
        //{
        //    stage2BXEGs = *stage2eg1Handle.product();
        //    for(auto& eg : stage2BXEGs) {
        //        stage2EGs.push_back( eg );
        //    } 
        //    std::sort(begin(stage2EGs), end(stage2EGs), [](l1t::EGamma& a, l1t::EGamma& b){return a.pt() > b.pt();});
        //}
        //else std::cout << "No valid stage2 EGs (2)" << std::endl;
    
    
        // FIXME Not sure how this will work with caloJets
        //
        //// Get the particle position upon entering ECal
        //RawParticle particle(genJet.p4());
        //particle.setVertex(genJet.vertex().x(), genJet.vertex().y(), genJet.vertex().z(), 0.);
        ////particle.setID(genJet.pdgId());
        //// Skip setID requires some external libraries working well that
        //// define HepPDT::ParticleID
        //// in the end, setID sets the mass and charge of our particle.
        //// Try doing this by hand for the moment
    
        //// Electrons... mainly
        //particle.setMass(.511); // MeV
        //int pdgId = genJet.pdgId();
        //if (pdgId > 0) {
        //    particle.setCharge( -1.0 ); }
        //if (pdgId < 0) {
        //    particle.setCharge( 1.0 ); }
    
        //// Charged pions
        //if (pdgId == -211 || pdgId == 211) {
        //        particle.setCharge( genJet.charge() );
        //        particle.setMass(139.6); // MeV
        //}
    
        //BaseParticlePropagator prop(particle, 0., 0., 4.);
        //BaseParticlePropagator start(prop);
        //prop.propagateToEcalEntrance();
        //if(prop.getSuccess()!=0)
        //{
        //    genJet = reco::Candidate::PolarLorentzVector(prop.E()*sin(prop.vertex().theta()), prop.vertex().eta(), prop.vertex().phi(), 0.);
        //    if ( debug ) std::cout << "Propogated genParticle to ECal, position: " << prop.vertex() << " momentum = " << prop.momentum() << std::endl;
        //    if ( debug ) std::cout << "                              starting position: " << start.vertex() << " momentum = " << start.momentum() << std::endl;
        //    if ( debug ) std::cout << "                          genParticle position: " << genJet.vertex() << " momentum = " << genJet.p4() << std::endl;
        //    if ( debug ) std::cout << "         old pt = " << genJet.pt() << ", new pt = " << genJet.pt() << std::endl;
        //}
        //else
        //{
        //    // something failed?
        //    if ( debug ) std::cout << "Taking defaul, non-propagated gen object" << std::endl;
        //    genJet = genJet.polarP4();
        //}
    
    
    
        treeinfo.gen_pt = genJet.pt();
        treeinfo.gen_eta = genJet.eta();
        treeinfo.gen_phi = genJet.phi();
        treeinfo.gen_energy = genJet.energy();
        treeinfo.gen_mass = genJet.mass();
        treeinfo.gen_charge = genJet.charge();
    
        //std::cout << "    ---!!!--- L1EG Size: " << caloJets.size() << std::endl;
        if ( caloJets.size() > 0 )
        {
            for(const auto& caloJet : caloJets)
            {
                if ( reco::deltaR(caloJet, genJetP4) < genMatchDeltaRcut )
                      //&& fabs(caloJet.pt()-genJetP4.pt())/genJetP4.pt() < genMatchRelPtcut )
                {

                    if ( debug ) std::cout << "using caloJet dr = " << reco::deltaR(caloJet, genJetP4) << std::endl;
                    treeinfo.deltaR = reco::deltaR(caloJet, genJetP4);
                    treeinfo.deltaPhi = reco::deltaPhi(caloJet, genJetP4);
                    treeinfo.deltaEta = genJetP4.eta()-caloJet.eta();
                    
                    fill_tree(caloJet);
    
                } // end passes Pt and dR match
            } // end Calo Jets loop
        } // have CaloJets
        else // no CaloJets
        {
            // Fill tree with -1 to signify we lose a gen jet        
            fill_tree_null();
        }
    } // end GenJets loop
}


// ------------ method called once each job just before starting event loop  ------------
void 
L1CaloJetStudies::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1CaloJetStudies::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
L1CaloJetStudies::beginRun(edm::Run const& run, edm::EventSetup const& es)
{
    //edm::ESHandle<HepPDT::ParticleDataTable> pdt;
    //es.getData(pdt);
    //if ( !ParticleTable::instance() ) ParticleTable::instance(&(*pdt));
}

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1CaloJetStudies::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1CaloJetStudies::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1CaloJetStudies::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1CaloJetStudies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ user methods (ncsmith)
void 
L1CaloJetStudies::integrateDown(TH1F * hist) {
    // integral includes overflow and underflow bins
    double integral=0.;
    for(int i=hist->GetNbinsX()+1; i>=0; i--)
    {
        integral += hist->GetBinContent(i);
        hist->SetBinContent(i, integral);
    }
}

void
L1CaloJetStudies::fill_tree(const l1slhc::L1CaloJet& caloJet) {
    // As of 28 May 2018 caloJet_pt is post-calibration
    treeinfo.ecal_pt = caloJet.GetExperimentalParam("ecal_pt");
    treeinfo.ecal_eta = caloJet.GetExperimentalParam("ecal_eta");
    treeinfo.ecal_phi = caloJet.GetExperimentalParam("ecal_phi");
    treeinfo.ecal_mass = caloJet.GetExperimentalParam("ecal_mass");
    treeinfo.ecal_energy = caloJet.GetExperimentalParam("ecal_energy");
    treeinfo.hcal_pt = caloJet.GetExperimentalParam("hcal_pt");
    treeinfo.hcal_eta = caloJet.GetExperimentalParam("hcal_eta");
    treeinfo.hcal_phi = caloJet.GetExperimentalParam("hcal_phi");
    treeinfo.hcal_mass = caloJet.GetExperimentalParam("hcal_mass");
    treeinfo.hcal_energy = caloJet.GetExperimentalParam("hcal_energy");
    treeinfo.jet_pt = caloJet.GetExperimentalParam("jet_pt");
    treeinfo.jet_eta = caloJet.GetExperimentalParam("jet_eta");
    treeinfo.jet_phi = caloJet.GetExperimentalParam("jet_phi");
    treeinfo.jet_mass = caloJet.GetExperimentalParam("jet_mass");
    treeinfo.jet_energy = caloJet.GetExperimentalParam("jet_energy");
    treeinfo.hcal_dR0p05 = caloJet.GetExperimentalParam("hcal_dR0p05");
    treeinfo.hcal_dR0p075 = caloJet.GetExperimentalParam("hcal_dR0p075");
    treeinfo.hcal_dR0p1 = caloJet.GetExperimentalParam("hcal_dR0p1");
    treeinfo.hcal_dR0p125 = caloJet.GetExperimentalParam("hcal_dR0p125");
    treeinfo.hcal_dR0p15 = caloJet.GetExperimentalParam("hcal_dR0p15");
    treeinfo.hcal_dR0p2 = caloJet.GetExperimentalParam("hcal_dR0p2");
    treeinfo.hcal_dR0p3 = caloJet.GetExperimentalParam("hcal_dR0p3");
    treeinfo.hcal_dR0p4 = caloJet.GetExperimentalParam("hcal_dR0p4");
    treeinfo.hcal_dR0p5 = caloJet.GetExperimentalParam("hcal_dR0p5");
    tree->Fill();
}


void
L1CaloJetStudies::fill_tree_null() {
    // Fill with -1 with no CaloJet fround
    treeinfo.ecal_pt = -1;
    treeinfo.ecal_eta = -1;
    treeinfo.ecal_phi = -1;
    treeinfo.ecal_mass = -1;
    treeinfo.ecal_energy = -1;
    treeinfo.hcal_pt = -1;
    treeinfo.hcal_eta = -1;
    treeinfo.hcal_phi = -1;
    treeinfo.hcal_mass = -1;
    treeinfo.hcal_energy = -1;
    treeinfo.jet_pt = -1;
    treeinfo.jet_eta = -1;
    treeinfo.jet_phi = -1;
    treeinfo.jet_mass = -1;
    treeinfo.jet_energy = -1;
    treeinfo.hcal_dR0p05 = -1;
    treeinfo.hcal_dR0p075 = -1;
    treeinfo.hcal_dR0p1 = -1;
    treeinfo.hcal_dR0p125 = -1;
    treeinfo.hcal_dR0p15 = -1;
    treeinfo.hcal_dR0p2 = -1;
    treeinfo.hcal_dR0p3 = -1;
    treeinfo.hcal_dR0p4 = -1;
    treeinfo.hcal_dR0p5 = -1;
    tree->Fill();
}



//define this as a plug-in
DEFINE_FWK_MODULE(L1CaloJetStudies);
