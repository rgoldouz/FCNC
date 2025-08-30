import datetime
import os
from os import path
import sys
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow, Dataset,ParentDataset, EmptyDataset
sys.path.append(os.path.abspath("."))

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

username = "rgoldouz"

production_tag = "combineFCNC"            # For 'full_production' setup

# Only run over lhe steps from specific processes/coeffs/runs
process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []  # (i.e. MG starting points)

master_label = '%s_%s' % (production_tag,timestamp_tag)

input_path   = "/store/user/"
output_path  = "/store/user/$USER/FullProduction/%s" % (production_tag)
workdir_path = "/tmpscratch/users/$USER/FullProduction/%s" % (production_tag)
plotdir_path = "~/www/lobster/FullProduction/%s" % (production_tag)

storage = StorageConfiguration(
    input=[
        "file:///users/",
        "file:///cms/cephfs/data/store/user/",
        "root://skynet013.crc.nd.edu//store/user/",
    ],
    output=[
        # Until a separate bug is fixed file://cms/cephfs needs to be the first output so the initial lobster validation passes.
        "file:///users/rgoldouz/FCNC/NanoAnalysis/combine/NllLobster/",
#        "file:///cms/cephfs/data"+output_path,
#        "root://skynet013.crc.nd.edu/"+output_path,
    ],
    disable_input_streaming=True,
)


#################################################################
# Worker Res.:
#   Cores:  12    | 4
#   Memory: 16000 | 8000
#   Disk:   13000 | 6500
#################################################################
gs_resources = Category(
    name='gs',
    cores=1,
    memory=2000,
    disk=1000,
    mode='max'
)
#################################################################
wf=[]
mypath = "/users/rgoldouz/FCNC/NanoAnalysis/combine/forLobster"

for entry in os.listdir(mypath):
    full_mypath = os.path.join(mypath, entry)
    if 'impact' in entry:
        continue
    if os.path.isdir(full_mypath):
        print(entry)
        Analysis = Workflow(
            label=entry,
            sandbox=cmssw.Sandbox(release='/users/rgoldouz/AnalyticAnomalousCoupling/CMSSW_14_1_0_pre4'),
            globaltag=False,
            command='python3.9 Lobster_check.py  @inputfiles',
            extra_inputs=[
                'CombinedFilesFCNC_v2/model_test_TU.root','CombinedFilesFCNC_v2/model_test_TC.root','Lobster_check.py',
            ],
            outputs=['combine.root'],
            dataset=Dataset(
               files=['rgoldouz/FCNC/NanoAnalysis/combine/forLobster/'+entry],
               files_per_task =1
            ),
            category=gs_resources
        )
        wf.append(Analysis)



config = Config(
    label=master_label,
    workdir=workdir_path,
    plotdir=plotdir_path,
    storage=storage,
    workflows=wf,
    advanced=AdvancedOptions(
        bad_exit_codes=[127, 160,137],
        osg_version='3.6',
        abort_threshold=100,
        abort_multiplier=100,
        full_monitoring=True,
        log_level=1,
        dump_core=True
    )
)
