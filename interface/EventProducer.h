#ifndef EVENT_PRODUCER
#define EVENT_PRODUCER

#include <cp3_llbb/Framework/interface/Producer.h>
#include <cp3_llbb/Framework/interface/PUReweighter.h>

#include <SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h>
#include <SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h>
#include <SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h>

#include <map>

// Uncomment to debug PDF uncertainties
// #define DEBUG_PDF

// If uncommented, LHE weights for LO samples will be read from the LHE file, otherwise, they will be computed directly using LHAPDF.
#define USE_LHE_WEIGHTS_FOR_LO

// If uncommented, the SCALUP value is used instead of originalXWGTUP to compute LHE weights on LO samples. It's a workaround to deal with a bug during the CMS generation of LO samples in 2015.
#define USE_SCALUP_FOR_LO_LHE_WEIGHTS

#ifndef USE_LHE_WEIGHTS_FOR_LO
#include <LHAPDF/LHAPDF.h>
#endif

class EventProducer: public Framework::Producer {
    public:
        EventProducer(const std::string& name, const ROOT::TreeGroup& tree, const edm::ParameterSet& config):
            Producer(name, tree, config)
        {

            if (config.getUntrackedParameter<bool>("compute_pu_weights", true))
                m_pu_reweighter = std::make_shared<Framework::PUReweighter>(config.getParameterSet("pu_reweighter"), Framework::PUProfile::Run2015_25ns);
                m_pu_reweighter_up = std::make_shared<Framework::PUReweighter>(config.getParameterSet("pu_reweighter_up"), Framework::PUProfile::Run2015_25ns);
                m_pu_reweighter_down = std::make_shared<Framework::PUReweighter>(config.getParameterSet("pu_reweighter_down"), Framework::PUProfile::Run2015_25ns);

        }

        virtual ~EventProducer() {}

        virtual void doConsumes(const edm::ParameterSet& config, edm::ConsumesCollector&& collector) override {
            m_rho_token = collector.consumes<double>(config.getUntrackedParameter<edm::InputTag>("rho", edm::InputTag("fixedGridRhoFastjetAll")));
            m_pu_info_token = collector.consumes<std::vector<PileupSummaryInfo>>(config.getUntrackedParameter<edm::InputTag>("pu_summary", edm::InputTag("addPileupInfo")));
            m_gen_info_token = collector.consumes<GenEventInfoProduct>(config.getUntrackedParameter<edm::InputTag>("gen_info", edm::InputTag("generator")));
            m_lhe_info_token = collector.consumes<LHEEventProduct>(config.getUntrackedParameter<edm::InputTag>("lhe_info", edm::InputTag("externalLHEProducer")));
        }

        virtual void beginRun(const edm::Run& run, const edm::EventSetup& eventSetup) override;
        virtual void produce(edm::Event& event, const edm::EventSetup& eventSetup) override;

        virtual void endJob(MetadataManager&) override;

    private:

        // Tokens
        edm::EDGetTokenT<double> m_rho_token;
        edm::EDGetTokenT<std::vector<PileupSummaryInfo>> m_pu_info_token;
        edm::EDGetTokenT<GenEventInfoProduct> m_gen_info_token;
        edm::EDGetTokenT<LHEEventProduct> m_lhe_info_token;

        float m_event_weight_sum = 0;
        float m_event_weight_sum_pdf_nominal = 0;
        float m_event_weight_sum_pdf_up = 0;
        float m_event_weight_sum_pdf_down = 0;
        std::vector<float> m_event_weight_sum_scales;

        std::shared_ptr<Framework::PUReweighter> m_pu_reweighter;
        std::shared_ptr<Framework::PUReweighter> m_pu_reweighter_up;
        std::shared_ptr<Framework::PUReweighter> m_pu_reweighter_down;

        std::vector<std::pair<uint32_t, size_t>> m_scale_variations_matching;
        std::vector<std::pair<uint32_t, size_t>> m_pdf_weights_matching;

        std::map<uint32_t, std::string> m_lo_pdf_set_strs {
            {263000, "NNPDF30_lo_as_0130"},
            {263400, "NNPDF30_lo_as_0130_nf_4"}
        };

        bool isLO = false;
        bool has_alphas_uncertainty = false;

#ifndef USE_LHE_WEIGHTS_FOR_LO
        std::vector<LHAPDF::PDF*> lhapdf_pdfs;
#endif

    public:
        // Tree members

        BRANCH(run, ULong64_t);
        BRANCH(lumi, ULong64_t);
        BRANCH(event, ULong64_t);
        BRANCH(is_data, bool);

        BRANCH(rho, float);

        BRANCH(npu, int);
        BRANCH(true_interactions, float);
        BRANCH(pu_weight, float);
        BRANCH(pu_weight_up, float);
        BRANCH(pu_weight_down, float);

        BRANCH(pt_hat, float);
        BRANCH(ht, float);
        BRANCH(weight, float);

        BRANCH(alpha_QCD, float);
        BRANCH(alpha_QED, float);
        BRANCH(q_scale, float);
        uint32_t& pdf_set = tree["pdf_set"].write<uint32_t>(false);
        BRANCH(pdf_id, std::pair<int, int>);
        BRANCH(pdf_x, std::pair<float, float>);
        BRANCH(pdf_weight, float);
        BRANCH(pdf_weight_up, float);
        BRANCH(pdf_weight_down, float);

        BRANCH(n_ME_partons, int);
        BRANCH(n_ME_partons_filtered, int);

        BRANCH(lhe_originalXWGTUP, float);
        BRANCH(lhe_SCALUP, float);
        TRANSIENT_BRANCH(lhe_weights, std::vector<std::pair<std::string, float>>);

        BRANCH(scale_weights, std::vector<float>);
};

#endif
