import sys 
import os 
import subprocess 
import readline 
import string 

UL17={
"UL18_ZZTo2L2Nu":[[], 'mc', 'none', '2018', 'none', '0.564', '59.83', '0', '0', '1'],
"UL17_BNV_TT_TSUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_tW_NoFullyHadronicDecays":[[], 'mc', 'none', '2017', 'none', '19.47', '41.48', '0', '0', '1'],
"UL18_tbarW_NoFullyHadronicDecays":[[], 'mc', 'none', '2018', 'none', '19.47', '59.83', '0', '0', '1'],
"UL16postVFP_tW_NoFullyHadronicDecays":[[], 'mc', 'none', '2016postVFP', 'none', '19.47', '16.81', '0', '0', '1'],
"UL18_BNV_ST_TBUE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16preVFP_DY10to50":[[], 'mc', 'none', '2016preVFP', 'none', '18610', '19.52', '0', '0', '1'],
"UL18_TTW":[[], 'mc', 'none', '2018', 'none', '0.2043', '59.83', '0', '0', '1'],
"UL17_DY10to50_v9":[[], 'mc', 'none', '2017', 'none', '18610', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_TT_TBUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_TT_TBUMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL17_BNV_TT_TBUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_BNV_TT_TDUE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_WZZ_v9":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_BNV_TT_TDUMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_TTW":[[], 'mc', 'none', '2017', 'none', '0.2043', '41.48', '0', '0', '1'],
"UL16postVFP_TTTo2L2Nu_sys_TuneCP5down":[[], 'mc', 'none', '2016postVFP', 'none', '87.31', '16.81', '0', '0', '1'],
"UL16preVFP_tbarW_NoFullyHadronicDecays":[[], 'mc', 'none', '2016preVFP', 'none', '19.47', '19.52', '0', '0', '1'],
"UL16postVFP_WWZ_4F":[[], 'mc', 'none', '2016postVFP', 'none', '0.1651', '16.81', '0', '0', '1'],
"UL16preVFP_BNV_ST_TDUMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_ST_TDUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_TTTo2L2Nu_sys_hdampDOWN":[[], 'mc', 'none', '2016postVFP', 'none', '87.31', '16.81', '0', '0', '1'],
"UL17_TTZToLLNuNu_M_10_v9":[[], 'mc', 'none', '2017', 'none', '0.2529', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_TT_TBCE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL18_WZTo3LNu":[[], 'mc', 'none', '2018', 'none', '4.43', '59.83', '0', '0', '1'],
"UL17_WWW_4F":[[], 'mc', 'none', '2017', 'none', '0.2086', '41.48', '0', '0', '1'],
"UL18_BNV_TT_TBUE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_BNV_ST_TSUE_DAS":[['rgoldouz/NanoAodPostProcessingUL/UL17/v1/UL17_BNV_ST_TSUE_DAS'], 'mc', 'none', '2017', 'none', '1', '41.48', '494000.0', '0', '648'],
"UL18_BNV_ST_TSCE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16postVFP_WWW_4F":[[], 'mc', 'none', '2016postVFP', 'none', '0.2086', '16.81', '0', '0', '1'],
"UL18_ZZZ":[[], 'mc', 'none', '2018', 'none', '0.01398', '59.83', '0', '0', '1'],
"UL16postVFP_TTTo2L2Nu_sys_hdampUP":[[], 'mc', 'none', '2016postVFP', 'none', '87.31', '16.81', '0', '0', '1'],
"UL16preVFP_BNV_ST_TSUMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_WJetsToLNu":[[], 'mc', 'none', '2017', 'none', '61526.7', '41.48', '0', '0', '1'],
"UL18_WZZ":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_tbarW_NoFullyHadronicDecays":[[], 'mc', 'none', '2017', 'none', '19.47', '41.48', '0', '0', '1'],
"UL17_TTTo2L2Nu_sys_hdampUP":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL16preVFP_WZZ":[[], 'mc', 'none', '2016preVFP', 'none', '1', '19.52', '0', '0', '1'],
"UL16preVFP_BNV_ST_TDCMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TSCMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_TTTo2L2Nu_sys_TuneCP5down":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL18_BNV_ST_TSCMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16preVFP_BNV_TT_TSUMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_TT_TDCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_TTTo2L2Nu_sys_hdampDOWN":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL18_TTTo2L2Nu_sys_hdampDOWN":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL18_BNV_ST_TDUE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_BNV_TT_TDCE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_TT_TBCMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_BNV_ST_TBUMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16preVFP_WWTo2L2Nu":[[], 'mc', 'none', '2016preVFP', 'none', '12.178', '19.52', '0', '0', '1'],
"UL18_WWTo2L2Nu":[[], 'mc', 'none', '2018', 'none', '12.178', '59.83', '0', '0', '1'],
"UL16postVFP_BNV_ST_TDUMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16postVFP_BNV_TT_TSUE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16preVFP_ZZTo2L2Nu":[[], 'mc', 'none', '2016preVFP', 'none', '0.564', '19.52', '0', '0', '1'],
"UL17_BNV_ST_TDUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_tuFCNC_tllProduction":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_WWZ_4F":[[], 'mc', 'none', '2018', 'none', '0.1651', '59.83', '0', '0', '1'],
"UL18_TTTo2L2Nu_sys_CR1":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL17_TTTo2L2Nu_sys_erdON":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL17_WWZ_4F":[[], 'mc', 'none', '2017', 'none', '0.1651', '41.48', '0', '0', '1'],
"UL17_ZZTo4L":[[], 'mc', 'none', '2017', 'none', '1.256 ', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_TT_TDUMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_BNV_ST_TDCE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16postVFP_WWTo2L2Nu":[[], 'mc', 'none', '2016postVFP', 'none', '12.178', '16.81', '0', '0', '1'],
"UL16postVFP_ZZZ":[[], 'mc', 'none', '2016postVFP', 'none', '0.01398', '16.81', '0', '0', '1'],
"UL18_TTTo2L2Nu_sys_hdampUP":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL16preVFP_BNV_TT_TSCMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_tbarW_NoFullyHadronicDecays":[[], 'mc', 'none', '2016postVFP', 'none', '19.47', '16.81', '0', '0', '1'],
"UL17_BNV_TT_TBCE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_TT_TDCMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_ST_TSCMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_TT_TBCMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16preVFP_BNV_ST_TBCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_ST_TDCMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL17_BNV_ST_TSCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_ZZTo4L_v9":[[], 'mc', 'none', '2017', 'none', '1.256 ', '41.48', '0', '0', '1'],
"UL18_TTTo2L2Nu_sys_TuneCP5down":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL18_BNV_ST_TDCMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_BNV_ST_TDCMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_ST_TSUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_TT_TDUMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16postVFP_BNV_TT_TDUE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL17_BNV_TT_TSCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_TT_TBUE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16preVFP_BNV_TT_TBUMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_tW_NoFullyHadronicDecays":[[], 'mc', 'none', '2016preVFP', 'none', '19.47', '19.52', '0', '0', '1'],
"UL16postVFP_BNV_ST_TDUE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16postVFP_WJetsToLNu":[[], 'mc', 'none', '2016postVFP', 'none', '61526.7', '16.81', '0', '0', '1'],
"UL18_TTTo2L2Nu_sys_TuneCP5up":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL16preVFP_BNV_ST_TDCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_BNV_ST_TBCE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_BNV_ST_TBCE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_TT_TDCMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL18_WJetsToLNu":[[], 'mc', 'none', '2018', 'none', '61526.7', '59.83', '0', '0', '1'],
"UL17_BNV_TT_TSUMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_ST_TDCE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16postVFP_BNV_TT_TDCE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16preVFP_DY50":[[], 'mc', 'none', '2016preVFP', 'none', '6077.22', '19.52', '0', '0', '1'],
"UL17_TTTo2L2Nu_sys_CR1":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL18_DY10to50":[[], 'mc', 'none', '2018', 'none', '18610', '59.83', '0', '0', '1'],
"UL18_BNV_TT_TBCMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_TTZToLLNuNu_M_10":[[], 'mc', 'none', '2017', 'none', '0.2529', '41.48', '0', '0', '1'],
"UL17_DY10to50":[[], 'mc', 'none', '2017', 'none', '18610', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_TT_TSCE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16postVFP_TTTo2L2Nu":[[], 'mc', 'none', '2016postVFP', 'none', '87.31', '16.81', '0', '0', '1'],
"UL17_BNV_ST_TSCE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_WJetsToLNu":[[], 'mc', 'none', '2016preVFP', 'none', '61526.7', '19.52', '0', '0', '1'],
"UL17_ZZZ":[[], 'mc', 'none', '2017', 'none', '0.01398', '41.48', '0', '0', '1'],
"UL16preVFP_WWW_4F":[[], 'mc', 'none', '2016preVFP', 'none', '0.2086', '19.52', '0', '0', '1'],
"UL18_BNV_TT_TBUMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_TTTo2L2Nu_sys_CR2":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL18_ZZTo4L":[[], 'mc', 'none', '2018', 'none', '1.256 ', '59.83', '0', '0', '1'],
"UL16preVFP_BNV_ST_TSCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_WWZ_4F":[[], 'mc', 'none', '2016preVFP', 'none', '0.1651', '19.52', '0', '0', '1'],
"UL16preVFP_BNV_TT_TSCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_TTW_v9":[[], 'mc', 'none', '2017', 'none', '0.2043', '41.48', '0', '0', '1'],
"UL18_BNV_ST_TSUE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16postVFP_BNV_ST_TSUE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16postVFP_BNV_ST_TBCMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL17_WWTo2L2Nu":[[], 'mc', 'none', '2017', 'none', '12.178', '41.48', '0', '0', '1'],
"UL18_WWW_4F":[[], 'mc', 'none', '2018', 'none', '0.2086', '59.83', '0', '0', '1'],
"UL17_tuFCNC_tHProduction":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_TTTo2L2Nu_sys_TuneCP5down":[[], 'mc', 'none', '2016preVFP', 'none', '87.31', '19.52', '0', '0', '1'],
"UL18_BNV_ST_TSUMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL18_BNV_TT_TSCMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16postVFP_BNV_TT_TSCMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL18_BNV_TT_TSUE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16postVFP_BNV_ST_TSCMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16postVFP_BNV_ST_TBUMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL17_BNV_ST_TDUMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_WZTo3LNu":[[], 'mc', 'none', '2016postVFP', 'none', '4.43', '16.81', '0', '0', '1'],
"UL17_BNV_TT_TSCE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_ST_TDUE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_DY50":[[], 'mc', 'none', '2017', 'none', '6077.22', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_ST_TSCMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_ZZTo2L2Nu_v9":[[], 'mc', 'none', '2017', 'none', '0.564', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TDUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TDUMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_DY50":[[], 'mc', 'none', '2018', 'none', '6077.22', '59.83', '0', '0', '1'],
"UL16preVFP_BNV_TT_TSUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_tuFCNC_uHDecay":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_ST_TBUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_ST_TSUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_ST_TBCE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL18_TTTo2L2Nu":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL16postVFP_ZZTo2L2Nu":[[], 'mc', 'none', '2016postVFP', 'none', '0.564', '16.81', '0', '0', '1'],
"UL17_BNV_TT_TSUE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_ST_TBUEMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_ST_TBUE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL17_ZZTo2L2Nu":[[], 'mc', 'none', '2017', 'none', '0.564', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TDUE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_BNV_TT_TDCE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL18_BNV_ST_TDUMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16preVFP_ZZZ":[[], 'mc', 'none', '2016preVFP', 'none', '0.01398', '19.52', '0', '0', '1'],
"UL17_TTTo2L2Nu":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL18_BNV_ST_TBCMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL18_TTTo2L2Nu_sys_CR2":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL18_BNV_TT_TSUMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL16postVFP_BNV_TT_TSUMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16preVFP_BNV_TT_TBCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_TTTo2L2Nu_sys_CR1":[[], 'mc', 'none', '2016postVFP', 'none', '87.31', '16.81', '0', '0', '1'],
"UL16preVFP_BNV_ST_TBCMu":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_ST_TSUMu":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL17_BNV_ST_TBUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_BNV_TT_TDUE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_WWTo2L2Nu_v9":[[], 'mc', 'none', '2017', 'none', '12.178', '41.48', '0', '0', '1'],
"UL18_TTTo2L2Nu_sys_erdON":[[], 'mc', 'none', '2018', 'none', '87.31', '59.83', '0', '0', '1'],
"UL18_TTZToLLNuNu_M_10":[[], 'mc', 'none', '2018', 'none', '0.2529', '59.83', '0', '0', '1'],
"UL17_BNV_ST_TDCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL18_BNV_TT_TDCMu":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL17_BNV_ST_TDCE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16postVFP_TTTo2L2Nu_sys_CR2":[[], 'mc', 'none', '2016postVFP', 'none', '87.31', '16.81', '0', '0', '1'],
"UL17_BNV_TT_TBUMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_WZTo3LNu":[[], 'mc', 'none', '2017', 'none', '4.43', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TBCMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_ST_TSUMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TBCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TDCMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_tuFCNC_ullDecay":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_TTTo2L2Nu_sys_erdON":[[], 'mc', 'none', '2016preVFP', 'none', '87.31', '19.52', '0', '0', '1'],
"UL17_BNV_TT_TDCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_ST_TBCE":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_TTTo2L2Nu_sys_TuneCP5up":[[], 'mc', 'none', '2017', 'none', '87.31', '41.48', '0', '0', '1'],
"UL16postVFP_BNV_ST_TSCE":[[], 'mc', 'none', '2016postVFP', 'none', '1', '16.81', '0', '0', '1'],
"UL16preVFP_TTTo2L2Nu_sys_hdampDOWN":[[], 'mc', 'none', '2016preVFP', 'none', '87.31', '19.52', '0', '0', '1'],
"UL18_tW_NoFullyHadronicDecays":[[], 'mc', 'none', '2018', 'none', '19.47', '59.83', '0', '0', '1'],
"UL17_BNV_ST_TBCMu_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_TTTo2L2Nu_sys_CR1":[[], 'mc', 'none', '2016preVFP', 'none', '87.31', '19.52', '0', '0', '1'],
"UL17_BNV_ST_TBUE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL17_BNV_TT_TBUE_DAS":[[], 'mc', 'none', '2017', 'none', '1', '41.48', '0', '0', '1'],
"UL16preVFP_TTTo2L2Nu_sys_CR2":[[], 'mc', 'none', '2016preVFP', 'none', '87.31', '19.52', '0', '0', '1'],
"UL16preVFP_TTTo2L2Nu":[[], 'mc', 'none', '2016preVFP', 'none', '87.31', '19.52', '0', '0', '1'],
"UL16postVFP_DY50":[[], 'mc', 'none', '2016postVFP', 'none', '6077.22', '16.81', '0', '0', '1'],
"UL17_WZTo2L2Q":[[], 'mc', 'none', '2017', 'none', '5.595', '41.48', '0', '0', '1'],
"UL18_BNV_TT_TSCE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],
"UL18_BNV_TT_TBCE":[[], 'mc', 'none', '2018', 'none', '1', '59.83', '0', '0', '1'],

 
"data_UL17_E_DoubleMuon":[[], 'data', 'DoubleMuon', '2017', 'E', '1', '41.48', '1', '0', '1'],
"data_UL17_C_MuonEG":[[], 'data', 'MuonEG', '2017', 'C', '1', '41.48', '1', '0', '1'],
"data_UL16postVFP_F_SingleElectron":[[], 'data', 'SingleElectron', '2016postVFP', 'F', '1', '16.81', '1', '0', '1'],
"data_UL16postVFP_H_MuonEG":[[], 'data', 'MuonEG', '2016postVFP', 'H', '1', '16.81', '1', '0', '1'],
"data_UL16preVFP_Bv1_MuonEG":[[], 'data', 'MuonEG', '2016preVFP', 'Bv1', '1', '19.52', '1', '0', '1'],
"data_UL18_C_DoubleMuon":[[], 'data', 'DoubleMuon', '2018', 'C', '1', '59.83', '1', '0', '1'],
"data_UL17_C_DoubleMuon":[[], 'data', 'DoubleMuon', '2017', 'C', '1', '41.48', '1', '0', '1'],
"data_UL17_E_DoubleEG":[[], 'data', 'DoubleEG', '2017', 'E', '1', '41.48', '1', '0', '1'],
"data_UL16postVFP_H_SingleElectron":[[], 'data', 'SingleElectron', '2016postVFP', 'H', '1', '16.81', '1', '0', '1'],
"data_UL18_A_EGamma":[[], 'data', 'EGamma', '2018', 'A', '1', '59.83', '1', '0', '1'],
"data_UL16postVFP_H_SingleMuon":[[], 'data', 'SingleMuon', '2016postVFP', 'H', '1', '16.81', '1', '0', '1'],
"data_UL16preVFP_Bv1_DoubleMuon":[[], 'data', 'DoubleMuon', '2016preVFP', 'Bv1', '1', '19.52', '1', '0', '1'],
"data_UL16postVFP_G_MuonEG":[[], 'data', 'MuonEG', '2016postVFP', 'G', '1', '16.81', '1', '0', '1'],
"data_UL17_F_MuonEG":[[], 'data', 'MuonEG', '2017', 'F', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_F_DoubleEG":[[], 'data', 'DoubleEG', '2016preVFP', 'F', '1', '19.52', '1', '0', '1'],
"data_UL17_F_DoubleEG":[[], 'data', 'DoubleEG', '2017', 'F', '1', '41.48', '1', '0', '1'],
"data_UL17_D_DoubleEG":[[], 'data', 'DoubleEG', '2017', 'D', '1', '41.48', '1', '0', '1'],
"data_UL16postVFP_F_DoubleEG":[[], 'data', 'DoubleEG', '2016postVFP', 'F', '1', '16.81', '1', '0', '1'],
"data_UL16preVFP_C_DoubleMuon":[[], 'data', 'DoubleMuon', '2016preVFP', 'C', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_C_DoubleEG":[[], 'data', 'DoubleEG', '2016preVFP', 'C', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_E_MuonEG":[[], 'data', 'MuonEG', '2016preVFP', 'E', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_D_DoubleMuon":[[], 'data', 'DoubleMuon', '2016preVFP', 'D', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_D_DoubleEG":[[], 'data', 'DoubleEG', '2016preVFP', 'D', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_Bv1_DoubleEG":[[], 'data', 'DoubleEG', '2016preVFP', 'Bv1', '1', '19.52', '1', '0', '1'],
"data_UL16postVFP_G_SingleMuon":[[], 'data', 'SingleMuon', '2016postVFP', 'G', '1', '16.81', '1', '0', '1'],
"data_UL16preVFP_E_DoubleMuon":[[], 'data', 'DoubleMuon', '2016preVFP', 'E', '1', '19.52', '1', '0', '1'],
"data_UL17_F_SingleMuon":[[], 'data', 'SingleMuon', '2017', 'F', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_C_MuonEG":[[], 'data', 'MuonEG', '2016preVFP', 'C', '1', '19.52', '1', '0', '1'],
"data_UL17_F_DoubleMuon":[[], 'data', 'DoubleMuon', '2017', 'F', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_F_SingleElectron":[[], 'data', 'SingleElectron', '2016preVFP', 'F', '1', '19.52', '1', '0', '1'],
"data_UL17_B_SingleMuon":[[], 'data', 'SingleMuon', '2017', 'B', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_F_DoubleMuon":[[], 'data', 'DoubleMuon', '2016preVFP', 'F', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_Bv2_SingleElectron":[[], 'data', 'SingleElectron', '2016preVFP', 'Bv2', '1', '19.52', '1', '0', '1'],
"data_UL17_B_DoubleMuon":[[], 'data', 'DoubleMuon', '2017', 'B', '1', '41.48', '1', '0', '1'],
"data_UL17_D_MuonEG":[[], 'data', 'MuonEG', '2017', 'D', '1', '41.48', '1', '0', '1'],
"data_UL17_E_SingleElectron":[[], 'data', 'SingleElectron', '2017', 'E', '1', '41.48', '1', '0', '1'],
"data_UL18_B_EGamma":[[], 'data', 'EGamma', '2018', 'B', '1', '59.83', '1', '0', '1'],
"data_UL18_B_MuonEG":[[], 'data', 'MuonEG', '2018', 'B', '1', '59.83', '1', '0', '1'],
"data_UL18_A_SingleMuon":[[], 'data', 'SingleMuon', '2018', 'A', '1', '59.83', '1', '0', '1'],
"data_UL17_C_SingleMuon":[[], 'data', 'SingleMuon', '2017', 'C', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_E_SingleElectron":[[], 'data', 'SingleElectron', '2016preVFP', 'E', '1', '19.52', '1', '0', '1'],
"data_UL18_D_EGamma":[[], 'data', 'EGamma', '2018', 'D', '1', '59.83', '1', '0', '1'],
"data_UL16preVFP_Bv2_MuonEG":[[], 'data', 'MuonEG', '2016preVFP', 'Bv2', '1', '19.52', '1', '0', '1'],
"data_UL17_C_SingleElectron":[[], 'data', 'SingleElectron', '2017', 'C', '1', '41.48', '1', '0', '1'],
"data_UL18_C_SingleMuon":[[], 'data', 'SingleMuon', '2018', 'C', '1', '59.83', '1', '0', '1'],
"data_UL18_A_DoubleMuon":[[], 'data', 'DoubleMuon', '2018', 'A', '1', '59.83', '1', '0', '1'],
"data_UL17_B_SingleElectron":[[], 'data', 'SingleElectron', '2017', 'B', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_E_DoubleEG":[[], 'data', 'DoubleEG', '2016preVFP', 'E', '1', '19.52', '1', '0', '1'],
"data_UL16postVFP_G_DoubleMuon":[[], 'data', 'DoubleMuon', '2016postVFP', 'G', '1', '16.81', '1', '0', '1'],
"data_UL18_B_SingleMuon":[[], 'data', 'SingleMuon', '2018', 'B', '1', '59.83', '1', '0', '1'],
"data_UL16postVFP_H_DoubleMuon":[[], 'data', 'DoubleMuon', '2016postVFP', 'H', '1', '16.81', '1', '0', '1'],
"data_UL16preVFP_Bv2_SingleMuon":[[], 'data', 'SingleMuon', '2016preVFP', 'Bv2', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_C_SingleMuon":[[], 'data', 'SingleMuon', '2016preVFP', 'C', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_C_SingleElectron":[[], 'data', 'SingleElectron', '2016preVFP', 'C', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_Bv2_DoubleMuon":[[], 'data', 'DoubleMuon', '2016preVFP', 'Bv2', '1', '19.52', '1', '0', '1'],
"data_UL18_A_MuonEG":[[], 'data', 'MuonEG', '2018', 'A', '1', '59.83', '1', '0', '1'],
"data_UL18_C_MuonEG":[[], 'data', 'MuonEG', '2018', 'C', '1', '59.83', '1', '0', '1'],
"data_UL16preVFP_Bv1_SingleMuon":[[], 'data', 'SingleMuon', '2016preVFP', 'Bv1', '1', '19.52', '1', '0', '1'],
"data_UL17_B_DoubleEG":[[], 'data', 'DoubleEG', '2017', 'B', '1', '41.48', '1', '0', '1'],
"data_UL16postVFP_F_MuonEG":[[], 'data', 'MuonEG', '2016postVFP', 'F', '1', '16.81', '1', '0', '1'],
"data_UL18_D_DoubleMuon":[[], 'data', 'DoubleMuon', '2018', 'D', '1', '59.83', '1', '0', '1'],
"data_UL17_E_MuonEG":[[], 'data', 'MuonEG', '2017', 'E', '1', '41.48', '1', '0', '1'],
"data_UL16postVFP_H_DoubleEG":[[], 'data', 'DoubleEG', '2016postVFP', 'H', '1', '16.81', '1', '0', '1'],
"data_UL17_D_DoubleMuon":[[], 'data', 'DoubleMuon', '2017', 'D', '1', '41.48', '1', '0', '1'],
"data_UL18_D_SingleMuon":[[], 'data', 'SingleMuon', '2018', 'D', '1', '59.83', '1', '0', '1'],
"data_UL18_C_EGamma":[[], 'data', 'EGamma', '2018', 'C', '1', '59.83', '1', '0', '1'],
"data_UL16preVFP_D_SingleMuon":[[], 'data', 'SingleMuon', '2016preVFP', 'D', '1', '19.52', '1', '0', '1'],
"data_UL16postVFP_F_DoubleMuon":[[], 'data', 'DoubleMuon', '2016postVFP', 'F', '1', '16.81', '1', '0', '1'],
"data_UL16postVFP_F_SingleMuon":[[], 'data', 'SingleMuon', '2016postVFP', 'F', '1', '16.81', '1', '0', '1'],
"data_UL16postVFP_G_DoubleEG":[[], 'data', 'DoubleEG', '2016postVFP', 'G', '1', '16.81', '1', '0', '1'],
"data_UL16preVFP_Bv1_SingleElectron":[[], 'data', 'SingleElectron', '2016preVFP', 'Bv1', '1', '19.52', '1', '0', '1'],
"data_UL17_B_MuonEG":[[], 'data', 'MuonEG', '2017', 'B', '1', '41.48', '1', '0', '1'],
"data_UL17_C_DoubleEG":[[], 'data', 'DoubleEG', '2017', 'C', '1', '41.48', '1', '0', '1'],
"data_UL18_D_MuonEG":[[], 'data', 'MuonEG', '2018', 'D', '1', '59.83', '1', '0', '1'],
"data_UL17_D_SingleMuon":[[], 'data', 'SingleMuon', '2017', 'D', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_Bv2_DoubleEG":[[], 'data', 'DoubleEG', '2016preVFP', 'Bv2', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_F_SingleMuon":[[], 'data', 'SingleMuon', '2016preVFP', 'F', '1', '19.52', '1', '0', '1'],
"data_UL17_E_SingleMuon":[[], 'data', 'SingleMuon', '2017', 'E', '1', '41.48', '1', '0', '1'],
"data_UL16postVFP_G_SingleElectron":[[], 'data', 'SingleElectron', '2016postVFP', 'G', '1', '16.81', '1', '0', '1'],
"data_UL17_D_SingleElectron":[[], 'data', 'SingleElectron', '2017', 'D', '1', '41.48', '1', '0', '1'],
"data_UL18_B_DoubleMuon":[[], 'data', 'DoubleMuon', '2018', 'B', '1', '59.83', '1', '0', '1'],
"data_UL16preVFP_E_SingleMuon":[[], 'data', 'SingleMuon', '2016preVFP', 'E', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_D_SingleElectron":[[], 'data', 'SingleElectron', '2016preVFP', 'D', '1', '19.52', '1', '0', '1'],
"data_UL16preVFP_D_MuonEG":[[], 'data', 'MuonEG', '2016preVFP', 'D', '1', '19.52', '1', '0', '1'],
"data_UL17_F_SingleElectron":[[], 'data', 'SingleElectron', '2017', 'F', '1', '41.48', '1', '0', '1'],
"data_UL16preVFP_F_MuonEG":[[], 'data', 'MuonEG', '2016preVFP', 'F', '1', '19.52', '1', '0', '1'],
}