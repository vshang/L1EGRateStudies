import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoAnalysis")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:l1egCrystalTest.root',

        # Single Photon 500 MeV
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-0002F9D6-332A-E711-B686-E0071B7AF7C0/round1_condor_cfg-0002F9D6-332A-E711-B686-E0071B7AF7C0.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-04C9A479-3C26-E711-A6AE-90B11C08AD7D/round1_condor_cfg-04C9A479-3C26-E711-A6AE-90B11C08AD7D.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-061446A2-1626-E711-9269-001E67A42026/round1_condor_cfg-061446A2-1626-E711-9269-001E67A42026.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-08903BA9-472A-E711-A444-5065F37D50E2/round1_condor_cfg-08903BA9-472A-E711-A444-5065F37D50E2.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-0AFF0653-3E2A-E711-A62A-5065F381F1C1/round1_condor_cfg-0AFF0653-3E2A-E711-A62A-5065F381F1C1.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-1017D103-2D2A-E711-B2EA-5065F381C1D1/round1_condor_cfg-1017D103-2D2A-E711-B2EA-5065F381C1D1.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-10EBF2C2-5D26-E711-9D19-0242AC130004/round1_condor_cfg-10EBF2C2-5D26-E711-9D19-0242AC130004.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-12F0A1E7-4126-E711-BF95-0242AC130005/round1_condor_cfg-12F0A1E7-4126-E711-BF95-0242AC130005.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-18B638AE-322A-E711-A0EE-4C79BA3201DF/round1_condor_cfg-18B638AE-322A-E711-A0EE-4C79BA3201DF.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-1C9E1A06-5226-E711-84B2-0242AC130005/round1_condor_cfg-1C9E1A06-5226-E711-84B2-0242AC130005.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-1CC12D7A-5C26-E711-AC13-001517FB1D0C/round1_condor_cfg-1CC12D7A-5C26-E711-AC13-001517FB1D0C.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-1E82EFF5-4D2A-E711-AB46-E0071B741D70/round1_condor_cfg-1E82EFF5-4D2A-E711-AB46-E0071B741D70.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-247F92AE-1626-E711-B8AB-A4BF01011BF7/round1_condor_cfg-247F92AE-1626-E711-B8AB-A4BF01011BF7.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-24A9C5C1-3D2A-E711-AE18-24BE05CE1E31/round1_condor_cfg-24A9C5C1-3D2A-E711-AE18-24BE05CE1E31.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-2CACC611-412A-E711-A3C8-4C79BA18131B/round1_condor_cfg-2CACC611-412A-E711-A3C8-4C79BA18131B.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-2E16A174-3C26-E711-A7B3-14187741212B/round1_condor_cfg-2E16A174-3C26-E711-A7B3-14187741212B.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-2E3D94D0-2F26-E711-B722-001E675A67BB/round1_condor_cfg-2E3D94D0-2F26-E711-B722-001E675A67BB.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-328EF9DB-332A-E711-B429-24BE05C3CBE1/round1_condor_cfg-328EF9DB-332A-E711-B429-24BE05C3CBE1.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-347BF4D4-4026-E711-AE2D-0242AC130002/round1_condor_cfg-347BF4D4-4026-E711-AE2D-0242AC130002.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-38B733DA-3F2A-E711-9679-24BE05C626C1/round1_condor_cfg-38B733DA-3F2A-E711-9679-24BE05C626C1.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-3A8353EF-412A-E711-9F64-5065F38182E1/round1_condor_cfg-3A8353EF-412A-E711-9F64-5065F38182E1.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-4059ACD3-462A-E711-B4E3-5065F381E151/round1_condor_cfg-4059ACD3-462A-E711-B4E3-5065F381E151.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-4274FF9B-542A-E711-B648-E0071B7A6850/round1_condor_cfg-4274FF9B-542A-E711-B648-E0071B7A6850.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-42A80D69-362A-E711-810B-24BE05C4D851/round1_condor_cfg-42A80D69-362A-E711-810B-24BE05C4D851.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-48F03B67-3826-E711-BD67-1866DAEEB358/round1_condor_cfg-48F03B67-3826-E711-BD67-1866DAEEB358.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-4A1DA91D-3C2A-E711-B288-5065F3812201/round1_condor_cfg-4A1DA91D-3C2A-E711-B288-5065F3812201.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-4CDA54CA-3226-E711-B8F9-FA163EE840E2/round1_condor_cfg-4CDA54CA-3226-E711-B8F9-FA163EE840E2.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-4E731FF8-402A-E711-AC91-5065F37DC062/round1_condor_cfg-4E731FF8-402A-E711-AC91-5065F37DC062.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-522A24C4-462A-E711-85E4-5065F3812261/round1_condor_cfg-522A24C4-462A-E711-85E4-5065F3812261.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-56C006F9-4E2A-E711-9DCE-5065F382C2B1/round1_condor_cfg-56C006F9-4E2A-E711-9DCE-5065F382C2B1.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-5C160DC6-472A-E711-99A5-A0000420FE80/round1_condor_cfg-5C160DC6-472A-E711-99A5-A0000420FE80.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-5CF5BECE-2F26-E711-ACAC-001517FA7A98/round1_condor_cfg-5CF5BECE-2F26-E711-ACAC-001517FA7A98.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-60458A40-B22B-E711-A055-E0071B7A8570/round1_condor_cfg-60458A40-B22B-E711-A055-E0071B7A8570.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-62F80A72-3C26-E711-BBA8-0242AC130003/round1_condor_cfg-62F80A72-3C26-E711-BBA8-0242AC130003.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-6811BEED-352A-E711-9930-E0071B7A8570/round1_condor_cfg-6811BEED-352A-E711-9930-E0071B7A8570.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-6A0DF802-2E26-E711-8E71-001E67A3F8A8/round1_condor_cfg-6A0DF802-2E26-E711-8E71-001E67A3F8A8.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-6A32ACCF-4626-E711-A42C-842B2B42B584/round1_condor_cfg-6A32ACCF-4626-E711-A42C-842B2B42B584.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-6EBE682E-422A-E711-B3F9-A0000420FE80/round1_condor_cfg-6EBE682E-422A-E711-B3F9-A0000420FE80.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-70989F84-1E26-E711-B1A8-A4BF01013F33/round1_condor_cfg-70989F84-1E26-E711-B1A8-A4BF01013F33.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-785DFA28-4326-E711-A7BC-D4AE527EEA1F/round1_condor_cfg-785DFA28-4326-E711-A7BC-D4AE527EEA1F.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-78676EC9-432A-E711-BA89-5065F37D8102/round1_condor_cfg-78676EC9-432A-E711-BA89-5065F37D8102.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-78BF8897-262A-E711-B95E-5065F37DD491/round1_condor_cfg-78BF8897-262A-E711-B95E-5065F37DD491.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-804407BB-332A-E711-9520-24BE05C63741/round1_condor_cfg-804407BB-332A-E711-9520-24BE05C63741.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-80EFF128-442A-E711-AC83-E0071B7A9810/round1_condor_cfg-80EFF128-442A-E711-AC83-E0071B7A9810.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-86797BA7-472A-E711-B785-5065F3810301/round1_condor_cfg-86797BA7-472A-E711-B785-5065F3810301.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-8827A08C-5026-E711-A79D-0242AC130004/round1_condor_cfg-8827A08C-5026-E711-A79D-0242AC130004.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-888AAF75-2726-E711-A049-0242AC130003/round1_condor_cfg-888AAF75-2726-E711-A049-0242AC130003.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-8EAC120F-362A-E711-8706-24BE05C4D801/round1_condor_cfg-8EAC120F-362A-E711-8706-24BE05C4D801.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-9075783D-2626-E711-BA28-90B11C0BCBD7/round1_condor_cfg-9075783D-2626-E711-BA28-90B11C0BCBD7.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-946B4CAA-3626-E711-A1B0-FA163ED2C408/round1_condor_cfg-946B4CAA-3626-E711-A1B0-FA163ED2C408.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-960DDF72-2E2A-E711-88B7-5065F37D0182/round1_condor_cfg-960DDF72-2E2A-E711-88B7-5065F37D0182.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-982AD4C3-4526-E711-A011-001E67A3F70E/round1_condor_cfg-982AD4C3-4526-E711-A011-001E67A3F70E.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-9CA59DE4-372A-E711-98DB-24BE05CE1E51/round1_condor_cfg-9CA59DE4-372A-E711-98DB-24BE05CE1E51.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-A216FA5F-4226-E711-ACD6-0242AC130004/round1_condor_cfg-A216FA5F-4226-E711-ACD6-0242AC130004.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-A40E60C1-5D26-E711-A0E3-0242AC130006/round1_condor_cfg-A40E60C1-5D26-E711-A0E3-0242AC130006.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-A6221FEA-1F2A-E711-97A9-5065F37DD491/round1_condor_cfg-A6221FEA-1F2A-E711-97A9-5065F37DD491.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-A6F5D92B-462A-E711-8B55-5065F37DD491/round1_condor_cfg-A6F5D92B-462A-E711-8B55-5065F37DD491.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-AE240DAD-3B26-E711-AE82-141877410340/round1_condor_cfg-AE240DAD-3B26-E711-AE82-141877410340.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-AE9C003C-292A-E711-9CFF-5065F381D2B2/round1_condor_cfg-AE9C003C-292A-E711-9CFF-5065F381D2B2.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-B2A721BB-3226-E711-8511-FA163E18625A/round1_condor_cfg-B2A721BB-3226-E711-8511-FA163E18625A.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-B4DE8DE9-4526-E711-80A1-0242AC130002/round1_condor_cfg-B4DE8DE9-4526-E711-80A1-0242AC130002.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-B696CE51-432A-E711-869D-E0071B6C9DF0/round1_condor_cfg-B696CE51-432A-E711-869D-E0071B6C9DF0.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-BE9CFECD-332A-E711-A038-24BE05CE1E11/round1_condor_cfg-BE9CFECD-332A-E711-A038-24BE05CE1E11.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-C020BD60-3826-E711-9CE2-0242AC130004/round1_condor_cfg-C020BD60-3826-E711-9CE2-0242AC130004.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-C05DC1F3-1227-E711-A87E-0CC47AA53D92/round1_condor_cfg-C05DC1F3-1227-E711-A87E-0CC47AA53D92.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-C60F84C9-462A-E711-BE4E-E0071B740D80/round1_condor_cfg-C60F84C9-462A-E711-BE4E-E0071B740D80.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-C6C882F0-3F2A-E711-B916-A0000420FE80/round1_condor_cfg-C6C882F0-3F2A-E711-B916-A0000420FE80.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-CCDB53CF-2526-E711-A33A-001E67E0061C/round1_condor_cfg-CCDB53CF-2526-E711-A33A-001E67E0061C.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-CE3D3F58-302A-E711-B3ED-E0071B73B6B0/round1_condor_cfg-CE3D3F58-302A-E711-B3ED-E0071B73B6B0.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-CEA33787-4726-E711-8F88-549F3525C380/round1_condor_cfg-CEA33787-4726-E711-8F88-549F3525C380.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-D43CD70F-1D2A-E711-B4C0-E0071B7A18F0/round1_condor_cfg-D43CD70F-1D2A-E711-B4C0-E0071B7A18F0.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-D67C4FBF-1626-E711-AE2B-A4BF010256DF/round1_condor_cfg-D67C4FBF-1626-E711-AE2B-A4BF010256DF.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-DAE6FED1-232A-E711-BAB8-5065F3812201/round1_condor_cfg-DAE6FED1-232A-E711-BAB8-5065F3812201.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-DAFD6DFF-3226-E711-93C0-FA163E167377/round1_condor_cfg-DAFD6DFF-3226-E711-93C0-FA163E167377.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-DEE9C081-2726-E711-A36C-0242AC130002/round1_condor_cfg-DEE9C081-2726-E711-A36C-0242AC130002.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-E2BF21F3-2B2A-E711-A5EF-24BE05C616A2/round1_condor_cfg-E2BF21F3-2B2A-E711-A5EF-24BE05C616A2.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-E8216484-5D26-E711-95A7-0242AC130003/round1_condor_cfg-E8216484-5D26-E711-95A7-0242AC130003.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-E82A17F6-4326-E711-B403-001E675A6A63/round1_condor_cfg-E82A17F6-4326-E711-B403-001E675A6A63.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-EC10AF05-2C2A-E711-AA33-4C79BA180C95/round1_condor_cfg-EC10AF05-2C2A-E711-AA33-4C79BA180C95.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-EE283DA3-1726-E711-90B0-001E67E6920C/round1_condor_cfg-EE283DA3-1726-E711-90B0-001E67E6920C.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-F4513C72-4C26-E711-89FE-0242AC130002/round1_condor_cfg-F4513C72-4C26-E711-89FE-0242AC130002.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-F4E55E37-1D2A-E711-83E4-E0071B7B2320/round1_condor_cfg-F4E55E37-1D2A-E711-83E4-E0071B7B2320.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-FA32901D-5226-E711-834C-0242AC130003/round1_condor_cfg-FA32901D-5226-E711-834C-0242AC130003.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-FA92B1BF-3326-E711-A8D7-0242AC130002/round1_condor_cfg-FA92B1BF-3326-E711-A8D7-0242AC130002.root',
        'file:/data/truggles/phaseII_singlePhoton_20170524v2-round1_condor_cfg/round1_condor_cfg-FE199C58-302A-E711-B83C-A0000420FE80/round1_condor_cfg-FE199C58-302A-E711-B83C-A0000420FE80.root', 
    )
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')

# Choose a 2030 geometry!
# The ones which don't work all replace the ECAL Endcap geometry with HGCal stuff
# Options in cmssw_810_pre16: (each also has an option without the Reco)
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff') # D7 works, D4 is the choosen config by Phase-2 L1Trig


process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')




# -------------------------------------------------------------------------------------------
#
### Mini-analyzer for L1EG TPs
process.TPAnalyzer = cms.EDAnalyzer('L1EGPreclusterAnalysis',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts"),
   L1CrystalClustersWithCutsInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterWithCuts")
)

# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1EGRateStudies',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts"),
   genParticles = cms.InputTag("genParticles"),
   L1TrackInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"),
   L1TrackPrimaryVertexTag = cms.InputTag("L1TkPrimaryVertex"),
   Stage2EG1Tag = cms.InputTag("simCaloStage2Digis", "", "HLT"),
   doEfficiencyCalc = cms.untracked.bool(True),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   doTracking = cms.untracked.bool(True),
   isPhoton = cms.untracked.bool(True),
   turnOnThresholds = cms.untracked.vint32(20, 30, 40),
   histogramBinCount = cms.untracked.int32(100),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(100),
   histogramEtaBinCount = cms.untracked.int32(20),
   genMatchDeltaRcut = cms.untracked.double(0.25),
   genMatchRelPtcut = cms.untracked.double(0.5),
   debug = cms.untracked.bool(False)
   #debug = cms.untracked.bool(True)
)

process.panalyzer = cms.Path(process.TPAnalyzer+process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("r2_phase2_singlePhoton_v8.root"), 
   closeFileFast = cms.untracked.bool(True)
)

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


