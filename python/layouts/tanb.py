import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("CMS Preliminary,  H^{#pm}#rightarrow#tau#nu tb),  19.7 fb^{-1} at 8 TeV"),
    #dataset = cms.string("CMS Preliminary,  H#rightarrow#tau#tau,  18.3 fb^{-1} at 8 TeV"),
    ## x-axis title
    xaxis = cms.string("m_{H^{#pm}} [GeV]"),
    ## x-axis title
    yaxis = cms.string("#bf{tan#beta}"),
    ## theory label 
    theory = cms.string("MSSM m_{h}^{modp} scenario"),
    ## min for plotting
    min = cms.double(0.01),
    ## max for plotting
    max = cms.double(60),
    ## min for plotting
    log = cms.int32(1),
    ## print to C (for fixing graphics)
    c = cms.bool(True),
    ## print to png
    png = cms.bool(True),
    ## print to pdf
    pdf = cms.bool(True),
    ## print to txt
    txt = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## define verbosity level
    verbosity = cms.uint32(10),
    ## define output label
    outputLabel = cms.string("mHp-tanb"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
#     90.
#   ,100.
   #,110.
#   ,120.
#   ,130.
#   ,140.
   #,150.
#   ,160.
   #,170.
   180.
   #,190.
   ,200.
   #,210.
   ,220.
   #,230.
   #,240.
#   ,250.  
   ,300.
#   ,350.
#   ,400.
#   ,450.
#   ,500.
#   ,600.
#   ,700.
 #  ,800.
 #  ,900.
 #  ,1000.
     ),
    ## is this mssm?
    mssm = cms.bool(True),
    ## plot transparent?
    transparent = cms.bool(False),
    ## print the 2-sigma band
    outerband = cms.bool(True),
    ## plot expected only
    expectedOnly = cms.bool(False),
    ## print constraints from mH=125GeV
    higgs125 = cms.bool(False),
    ## add arXiv-1211-6956 (ATLAS) to plot
    arXiv_1211_6956 = cms.bool(False),
    ## add arXiv-1204-2760 (ATLAS) to plot
    arXiv_1204_2760 = cms.bool(False),
    ## add arXiv-1302-2892
    arXiv_1302_2892 = cms.bool(False),
    ## add arXiv-1205-5736
    arXiv_1205_5736 = cms.bool(False),
    ## add HIG-12-052
    HIG_12_052 = cms.bool(False),
)
