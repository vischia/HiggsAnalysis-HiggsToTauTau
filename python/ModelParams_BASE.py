from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_Hp_xsec_tools
from HiggsAnalysis.HiggsToTauTau.tools.feyn_higgs_mssm import feyn_higgs_mssm
from HiggsAnalysis.HiggsToTauTau.MODEL_PARAMS import MODEL_PARAMS
from os import getenv
from sys import exit

class ModelParams_BASE:
    """
    Description:

    Basic class for determination of model parameters.
    This class takes as input mA and tanb and and additional parameter for the model.
    It then determines the parameter of the model and stores them in a variable of type
    MODEL_PARAMS.
    The main functions to be used for creation of the MODEL_PARAMS are 'setup_model' and  'create_model_params'
    """
    def __init__(self, mA, tanb):
        self.mA = mA
        self.tanb = tanb
   
    def setup_model(self, period, modelpath='mhmax-mu+200', modeltype='mssm_xsec'):
        """
        Function to setup the model for the determination of crossection and brnachingratios
        arguments as period, modelpath and modeltype
        periode is one of '7TeV', '8TeV'
        modelpath corresponds to the file to be used for the model specified in modeltype
          - feyn_higgs_mssm : modelpath is the name of the model to be used (e.g. mhmax)
          - mssm_xsec_tools : modelpath is the name of the model to be used including uncerts (e.g mhmax-mu+200)
        modeltype can be 'mssm_xsec' or 'feyn_higgs' or 'mssm_Hp_xsec'
        """
        if modelpath == 'mssm_Hp_xsec' :
            modeltype = modelpath
        print "[ModelParams_BASE] Self:  ", self
        print "[ModelParams_BASE] Period:  ", period
        print "[ModelParams_BASE] Modelpath:  ", modelpath
        print "[ModelParams_BASE] Modeltype:  ", modeltype 
        self.model = modeltype
        print "[ModelParams_BASE] self.model after: ", self.model
        if modeltype == 'mssm_xsec':
            if float(self.tanb) < 1:
                tanbregion = 'tanbLow'
            else:
                tanbregion = 'tanbHigh'
            mssm_xsec_tools_path = getenv('CMSSW_BASE')+'/src/auxiliaries/models/out.'+modelpath+'-'+period+'-'+tanbregion+'-nnlo.root'
            print "File opened: ", mssm_xsec_tools_path 
            scan = mssm_xsec_tools(mssm_xsec_tools_path)
            self.htt_query = scan.query(self.mA, self.tanb)
        if modeltype == 'mssm_Hp_xsec':
            if float(self.tanb) < 1:
                exit('ERROR: Modeltype \'%s\' not supported for low tan(beta) values '%modeltype)
            else:
                tanbregion = 'tanbHigh'
            mssm_xsec_tools_path = getenv('CMSSW_BASE')+'/src/auxiliaries/models/out.'+modelpath+'-'+period+'-'+tanbregion+'-nlodbcorr.root'    
            scan = mssm_Hp_xsec_tools(mssm_xsec_tools_path)
            # Let's call it htt_query for now. Must check if it's just historical name or if I should create another self.hp_query or so on  
            self.htt_query = scan.query(self.mA, self.tanb)

    def create_model_params(self, period, channel, decay, uncert=''):
        """
        Main function to be used for creating a object of type MODEL_PARAMS for a given period,
        production channel, decay channel and model.
        periode is one of '7TeV', '8TeV'
        channel is of type ggH
        decay is of type [h,H,A]tt
        uncert specifies the uncertainty to be used. It can be 'mu+', 'mu-', 'pdf+', 'pdf-' or ''
        The trailing +/- corresponds to an up/down fluctuation of the uncertainty.
        '' specifies no uncertainty to be used.
        """
        self.uncert = uncert
        print "SELF FUCKING UNCERTAINTY: ", self.uncert 
        model_params = MODEL_PARAMS()
        if self.model == 'feyn_higgs':
            self.use_feyn_higgs(modelpath, period, channel, decay, model_params)
        elif self.model == 'mssm_xsec':
            self.use_mssm_xsec(self.htt_query, channel, decay, model_params)
        elif self.model == 'mssm_Hp_xsec':
            model_params.list_of_higgses = ['Hp']
            print "[ModelParams_BASE] use_mssm_Hp_xsec called with parameters: "
            print self.htt_query
            print channel
            print decay
            print model_params
            print "--------------------------------"
            self.use_mssm_Hp_xsec(self.htt_query, channel, decay, model_params)
        else:
            exit('ERROR: modeltype \'%s\' not supported'%modeltype)
        print "The model param chosen is:"+self.model+"and the uncertainties are "+ uncert
        return model_params

    def use_feyn_higgs(self, path, period, channel, decay, model_params):
        """
        This functions takes the input from create_model_params and uses feyn_higgs_mssm to determine the masses, cross-sections
        and branchingratios for the given production and decay channels
        """
        scan = feyn_higgs_mssm(self.mA, self.tanb, 'sm', path, period) #consider using variable for 'sm', 'mssm'
        for higgs in model_params.list_of_higgses:
            if higgs == 'A': model_params.masses[higgs] = self.mA
            if higgs == 'h': model_params.masses[higgs] = scan.get_mh()
            if higgs == 'H': model_params.masses[higgs] = scan.get_mH()
            xsecs = scan.get_xs(channel[:-1]+higgs)
            model_params.xsecs[higgs] = xsecs
            brs = scan.get_br(higgs+decay[1:])
            model_params.brs[higgs] = brs

    def use_mssm_xsec(self, query, channel, decay, model_params):
        """
        This function takes the input from create_model_params and uses mssm_xsec_tools to determine the masses,
        cross-sections and branchingratios for the given production and decay channels
        """
        for higgs in model_params.list_of_higgses:
            model_params.masses[higgs] = self.query_masses(higgs, query)
            model_params.xsecs[higgs] = self.query_xsec(higgs, channel, query)
            model_params.brs[higgs] = self.query_br(higgs, decay, query)

    def use_mssm_Hp_xsec(self, query, channel, decay, model_params):
        """
        This function takes the input from create_model_params and uses mssm_xsec_tools to determine the masses,
        cross-sections and branchingratios for the given production and decay channels
        """
        # FIXME: nunca se sabe
        model_params.list_of_higgses = [ 'Hp' ]
        for higgs in model_params.list_of_higgses:
            model_params.masses[higgs] = self.query_masses(higgs, query)
            model_params.xsecs[higgs] = self.query_xsec(higgs, channel, query)
            model_params.brs[higgs] = self.query_br(higgs, decay, query, channel)

    def query_masses(self, higgs, query):
        """
        Determine the mass of the higgs given as input. This function uses the
        mssm_xsec_tools.
        """
        if higgs == 'A': return self.mA
        return query['higgses'][higgs]['mass']

    def query_xsec(self, higgs, channel, query):
        """
        Determine the cross-section of the specified production channel for a given higgs.
        This function uses the mssm_xsec_tools.
        Currently only 'ggH', 'bbH', 'TBH' and 'HTB' are supported
        Please ignore the shameful acronym 'sam' for charged higgs santander matching
        """
        channels = {'ggH':'ggF', 'bbH':'santander', 'TBH':'TBH', 'HTB':'HTB'}
        #        # Temp hack for testing. No physics
        #        if channel == 'TBH' : channel = 'ggH'
        #        if channel == 'HTB' : channel = 'bbH'
        #        # End of temp hack for testing 
        if channel not in channels:
            exit('ERROR: Production channel \'%s\' not supported'%channel)
        print "self.uncert:",self.uncert,"CCCC"    
        if self.uncert =='mssm_Hp_xsec-' :
            return
        if self.uncert =='mssm_Hp_xsec+' :
            return
        if self.uncert == '':
            print "QUERY: ", higgs, channel 
            return query['higgses'][higgs]['xsec'][channels[channel]]
        elif self.uncert[-1] == '+':
            return query['higgses'][higgs][self.uncert[:-1]][channels[channel]][1]
        elif self.uncert[-1] == '-':
            return query['higgses'][higgs][self.uncert[:-1]][channels[channel]][-1]
        else:
            exit("ERROR: uncertainty %s is not supported"%(self.uncert))

    def query_br(self, higgs, decay, query, channel=''):
        """
        Determine the branching ratio of the specified decay channel for a given higgs.
        This function uses the mssm_xsec_tools.
        Currently only htt, hbb and hmm are supported.
        """
        print "Higgs: ", higgs
        print "DECAY: ", decay
        print "DECAY1: ", decay[1:]
        print "QUERYbr: ", query
        if channel == 'HTB' :
            if higgs == 'A' :
                return
            brname = {'tt':'BR-tb' } 
            if decay[1:] not in brname:
                exit('ERROR: Decay channel \'%s\' not supported'%decay)
            return query['higgses'][higgs][brname[decay[1:]]]
        if channel == 'TBH' :
            if higgs == 'A' :
                return
            brname = {'tt':'BR-taunu' } 
            if decay[1:] not in brname:
                exit('ERROR: Decay channel \'%s\' not supported'%decay)
            return query['higgses'][higgs][brname[decay[1:]]]

        brname = {'tt':'BR','bb':'BR-bb', 'mm' : 'BR-mumu', '' : 'BR-tb' , 'TBH' : 'BR-taunu' }
        if decay[1:] not in brname:
            exit('ERROR: Decay channel \'%s\' not supported'%decay)
        return query['higgses'][higgs][brname[decay[1:]]]
