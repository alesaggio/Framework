import FWCore.ParameterSet.Config as cms

default_configuration = cms.PSet(
        type = cms.string('muons'),
        prefix = cms.string('muon_'),
        enable = cms.bool(True),
        parameters = cms.PSet(
            src = cms.untracked.InputTag('slimmedMuons'),
            ea_R03 = cms.untracked.FileInPath('cp3_llbb/Framework/data/effAreaMuons_cone03_pfNeuHadronsAndPhotons.txt'),
            ea_R04 = cms.untracked.FileInPath('cp3_llbb/Framework/data/effAreaMuons_cone04_pfNeuHadronsAndPhotons.txt'),
            scale_factors = cms.untracked.PSet(
                tracking = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_tracking_BCDEFGH.json'),
                id_loose  = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_LooseID_genTracks_id_BCDEFGH_weighted.json'),
                id_medium = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_MediumID_genTracks_id_BCDEFGH_weighted.json'),
                id_medium2016 = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_MediumID2016_genTracks_id_BCDEFGH_weighted.json'),
                id_tight  = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_TightID_genTracks_id_BCDEFGH_weighted.json'),

                iso_loose_id_tight = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_LooseISO_TightID_iso_BCDEFGH_weighted.json'),
                iso_loose_id_medium = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_LooseISO_MediumID_iso_BCDEFGH_weighted.json'),
                iso_loose_id_loose = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_LooseISO_LooseID_iso_BCDEFGH_weighted.json'),
                iso_tight_id_tight = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_TightISO_TightID_iso_BCDEFGH_weighted.json'),
                iso_tight_id_medium = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_TightISO_MediumID_iso_BCDEFGH_weighted.json'),

                id_tight_hww = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_data_mc_TightID_Run2016_Run271036to276811_PTvsETA_HWW_weighted.json'),
                iso_tight_hww = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/Muon_data_mc_ISOTight_Run2016_Run271036to276811_PTvsETA_HWW_weighted.json'),

                )
            )
        )
