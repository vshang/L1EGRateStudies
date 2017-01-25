import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoTest")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0067AD1C-3877-E611-949E-0CC47A4D768C.root', 
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/00DB3E49-E876-E611-968D-0CC47A4C8EA8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/02049990-EE76-E611-8EE5-0025905B85DE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/04AA9405-2677-E611-821B-0CC47A4D763C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/04F1F579-2C77-E611-93FC-0025905AA9CC.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/06D91E5E-D676-E611-894E-0025905A48E4.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/084FCBC0-E576-E611-B820-0025905A6134.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0C24421F-EC76-E611-B247-0CC47A78A42E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0C445DDC-4377-E611-B24B-0CC47A7C3572.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0CAAD682-D276-E611-AA45-0CC47A4D768E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0E2223CB-E176-E611-8CA3-0025905A48B2.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/10C424A4-4E77-E611-BFA8-0CC47A78A3E8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/14006BE9-3277-E611-95E8-0025905A60EE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/148E00A3-F176-E611-BFD8-0CC47A4D7614.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1A249F39-3977-E611-9E6C-0025905A6084.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1AB35B15-3577-E611-A8AF-0CC47A4D769C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1C578B27-DF76-E611-85B0-0CC47A4C8E3C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1E0E96BA-2377-E611-A1E4-0CC47A4D76B6.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/2C22CF47-D276-E611-A461-0CC47A4C8F12.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/3640DA17-6F77-E611-94D8-0025905A60BE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/38B352E9-4677-E611-AC34-0025905B8598.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/44E5D267-0577-E611-9105-0CC47A4C8E96.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/44F41F92-E876-E611-A42B-0025905B85DA.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/46031293-5277-E611-8B31-0025905A6122.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/46D53382-5B77-E611-AD53-0CC47A7C361E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/48DF2B5C-0F77-E611-AA7A-0025905A60B4.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4A63FF49-CD76-E611-852D-0025905A6092.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4AC2B378-3F77-E611-A57D-0025905A605E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/50F6B0E8-4C77-E611-A023-0CC47A4D76C0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/56790B87-1177-E611-9A1E-0025905A610C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/56AE1812-4E77-E611-A83B-0CC47A4C8E70.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/66085F10-3177-E611-AB5B-003048FFD798.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6C5C4288-EA76-E611-A870-0CC47A4C8F2C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6E782766-E676-E611-9786-0CC47A74524E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/72F787DB-5A77-E611-B7A1-0025905B8564.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/7CF212C9-3277-E611-90C5-0CC47A4D76C0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/80BF4EDC-5877-E611-BC5D-0CC47A4D764A.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/80D1C17B-1677-E611-A988-003048FFD79E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/84920845-3277-E611-B24B-0CC47A7C34A0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/86D68C04-2677-E611-A855-0CC47A4D7600.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/8E7BC14E-5E77-E611-8A77-0025905A6132.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/90703BEF-2977-E611-B9A8-0CC47A4C8E0E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/943506A7-2E77-E611-A08D-0CC47A78A468.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/94DFFA2E-2677-E611-BEB1-0025905B85DC.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9640AD73-1C77-E611-8236-0025905A60E4.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/98B2D03A-3177-E611-9414-0025905A6118.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9C09B739-2377-E611-8CCE-0025905B855C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A6B08DEC-3D77-E611-9D11-0025905B860E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A8B6F619-5977-E611-A65B-0025905B8562.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AA8DF969-2377-E611-B77E-0CC47A7C35E0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AE19B8C0-6477-E611-9758-0025905A60F8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AE55398C-5E77-E611-9AFA-0CC47A4D7664.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B4B41042-7177-E611-A7DE-0CC47A4D7632.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B87636C8-3177-E611-963E-0025905A60DE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B8BC7408-E176-E611-9317-0025905A48BC.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B8E8B622-E076-E611-9F91-0CC47A4C8E70.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/BA76FE20-2877-E611-A76F-0CC47A78A440.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C4163F0A-3177-E611-834C-0025905A610C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C851857D-6077-E611-8A6B-0CC47A78A30E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D0044C8E-2377-E611-91B0-0CC47A78A42C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D42C2DE2-1C77-E611-A2D3-0025905A605E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D8A8A5BB-0477-E611-8B01-0025905B856C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D8FA286F-2B77-E611-937E-0025905A608C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DE9244D7-4577-E611-8AFA-0025905A610C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DEF48CFB-3F77-E611-BAD5-0CC47A4D764A.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/EAFAEEB6-1A77-E611-A2B6-0CC47A4C8E14.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/ECF986F5-3D77-E611-A97D-0025905A48D8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/EE2E50CF-4577-E611-968B-0025905A6068.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F2510F4B-7577-E611-AB88-0CC47A4C8ED8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/FC78CFCC-6177-E611-B397-0CC47A4C8F0C.root'
    )
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'PH2_1K_FB_V3::All', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# Choose a 2030 geometry!
# The ones which don't work all replace the ECAL Endcap geometry with HGCal stuff
# Options in cmssw_810_pre16: (each also has an option without the Reco)
process.load('Configuration.Geometry.GeometryExtended2023D1Reco_cff') # Works
#process.load('Configuration.Geometry.GeometryExtended2023D2Reco_cff') # Works
#process.load('Configuration.Geometry.GeometryExtended2023D3Reco_cff') # HGCal stuff, doesn't work 
#process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff') # HGCal stuff, doesn't work 
#process.load('Configuration.Geometry.GeometryExtended2023D5Reco_cff') # Crashes geometryHelper, this is the default one used for ECAL TPs
#process.load('Configuration.Geometry.GeometryExtended2023D6Reco_cff') # Works

#process.load('Configuration.Geometry.GeometryExtended2023simReco_cff') # Has CaloTopology, but no ECal endcap, don't use!
#process.load('Configuration.Geometry.GeometryExtended2023GRecoReco_cff') # using this geometry because I'm not sure if the tilted geometry is vetted yet
#process.load('Configuration.Geometry.GeometryExtended2023D5Reco_cff') # using this geometry because it is what was used for ECAL TP production in 810_pre16, this one doesn't work with the geometryHelper
#process.load('Configuration.Geometry.GeometryExtended2023tiltedReco_cff') # this one good?

#process.load('Configuration.Geometry.GeometryExtended2023TTIReco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
#process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
#process.load('Geometry.TrackerGeometryBuilder.StackedTrackerGeometry_cfi')
#process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')
#process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')

#process.load('Configuration/StandardSequences/L1HwVal_cff')
#process.load('Configuration.StandardSequences.RawToDigi_cff')
#process.load("SLHCUpgradeSimulations.L1CaloTrigger.SLHCCaloTrigger_cff")

# bug fix for missing HCAL TPs in MC RAW
#from SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff import HcalTPGCoderULUT
#HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
#process.valRctDigis.hcalDigis             = cms.VInputTag(cms.InputTag('valHcalTriggerPrimitiveDigis'))
#process.L1CaloTowerProducer.HCALDigis =  cms.InputTag("valHcalTriggerPrimitiveDigis")
#
#process.slhccalo = cms.Path( process.RawToDigi + process.valHcalTriggerPrimitiveDigis+process.SLHCCaloTrigger)

# run L1Reco to produce the L1EG objects corresponding
# to the current trigger
#process.load('Configuration.StandardSequences.L1Reco_cff')
#process.L1Reco = cms.Path( process.l1extraParticles )

# producer for UCT2015 / Stage-1 trigger objects
#process.load("L1Trigger.UCT2015.emulationMC_cfi")
#process.load("L1Trigger.UCT2015.uctl1extraparticles_cfi")
#process.pUCT = cms.Path(
#    process.emulationSequence *
#    process.uct2015L1Extra
#)

# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

# first you need the ECAL RecHIts :
#process.load('Configuration.StandardSequences.Reconstruction_cff')
#process.reconstruction_step = cms.Path( process.calolocalreco )

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   debug = cms.untracked.bool(False),
   useECalEndcap = cms.bool(False),
   useRecHits = cms.bool(True),
   ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   hcalRecHit = cms.InputTag("hbhereco"),
   useTowerMap = cms.untracked.bool(False)
)

process.pSasha = cms.Path( process.L1EGammaCrystalsProducer )

# --------------------------------------------------------------------------------------------
#
# ----  Match the L1EG stage-2 objects created by the SLHCCaloTrigger sequence above
#   with the crystal-level clusters.
#   This produces a new collection of L1EG objects, starting from the original
#   L1EG collection. The eta and phi of the L1EG objects is corrected using the
#   information of the xtal level clusters.

#process.l1ExtraCrystalProducer = cms.EDProducer("L1ExtraCrystalPosition",
#   eGammaSrc = cms.InputTag("SLHCL1ExtraParticles","EGamma"),
#   eClusterSrc = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster")
#)
#process.egcrystal_producer = cms.Path(process.l1ExtraCrystalProducer)


# ----------------------------------------------------------------------------------------------
# 
# Do offline reconstruction step for electron matching
# First we need to run EcalSeverityLevelESProducer ES Producer

process.load('RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi')

process.load('RecoEcal.Configuration.RecoEcal_cff')
process.ecalClusters = cms.Path(process.ecalClustersNoPFBox)






# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1EGRateStudies',
   #L1EGammaInputTags = cms.VInputTag(
   #   # Old stage-2 trigger
   #   cms.InputTag("SLHCL1ExtraParticles","EGamma"),
   #   # 'dynamic clustering'
   #   cms.InputTag("SLHCL1ExtraParticlesNewClustering","EGamma"),
   #   # Run 1 algo.
   #   cms.InputTag("l1extraParticles", "Isolated"),
   #   cms.InputTag("l1extraParticles", "NonIsolated"),
   #   # UCT alg.
   #   cms.InputTag("l1extraParticlesUCT", "Isolated"),
   #   cms.InputTag("l1extraParticlesUCT", "NonIsolated"),
   #   # Crystal-level algo.
   #   cms.InputTag("L1EGammaCrystalsProducer","EGammaCrystal")
   #),
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster"),
   genParticles = cms.InputTag("genParticles"),
   OfflineRecoClustersInputTag = cms.InputTag("correctedHybridSuperClusters"),
   doEfficiencyCalc = cms.untracked.bool(True),
   #doEfficiencyCalc = cms.untracked.bool(False),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   turnOnThresholds = cms.untracked.vint32(20, 30, 16),
   histogramBinCount = cms.untracked.int32(60),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(50),
   histogramEtaBinCount = cms.untracked.int32(20),
   genMatchDeltaRcut = cms.untracked.double(0.25),
   genMatchRelPtcut = cms.untracked.double(0.5), # align the rec hits with ecal TP value
   debug = cms.untracked.bool(False)
)

process.panalyzer = cms.Path(process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("effTest_recHits.root"), 
   closeFileFast = cms.untracked.bool(True)
)


dump_file = open("dump_file.py", "w")
dump_file.write(process.dumpPython())



