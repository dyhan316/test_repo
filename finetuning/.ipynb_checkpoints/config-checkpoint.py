from cmath import nan

PRETRAINING = 0
FINE_TUNING = 1

class Config:

    def __init__(self, mode, task):
        assert mode in {PRETRAINING, FINE_TUNING}, "Unknown mode: %i"%mode
            

        self.mode = mode

        if self.mode == PRETRAINING:
            raise NotImplementedError("shouldn't use this as pretarining part of this code is wrong ")

        
        ##trash values (only for debugging)
        elif self.mode == FINE_TUNING:
            ## We assume a classification task here
            ##default, true for all
            self.nb_epochs_per_saving = 10
            self.pin_mem = True
            self.num_cpu_workers = 8 #tested and found that whether I use 1 or 2 doesn'tr matter (the bottle neck isn't in the number of cpu workers)(persistent workers 써도 여전히 느리더라, 그냥 스킵하잨ㅋ)
            self.nb_epochs = 300 # ADNI #####
            print("changed nb_epochs to sth else more longer after hyperparam finetuning is done!!!")
            self.cuda = True
            self.task = task # for future reference

            ##training hyperparams
            self.tf = 'cutout' # ADNI #option for none? 
            self.model = 'DenseNet' # 'UNet'
            self.patience = 100 # ADNI
            self.valid_ratio = 0.25 # ADNI (valid set ratio compared to training set)
            
            ###special, must change by the weights we use 
            
            #self.resize_method = 'reshape'    #"padcrop", None (three cases, resizing or pad/cropping or none)        
            #self.input_size = (1, 80, 80, 80) 
            
            #these are now deifned in parser
            #self.batch_size = 32            
            #self.lr = 1e1 #1e-4
            #self.weight_decay = 5e-5
            
            if task == "test":
                self.nb_epochs = 100
                self.data = '/hpcgpfs01/scratch/dyhan316/VAE_ADHD_data/ADNI_T1_data_SAMPLE_for_try'  #use only subset with like 180 samples#'./adni_t1s_baseline' # 
                self.label = './csv/fsdat_try_sample.csv' #'./csv/fsdat_baseline.csv' # where the label file is 
                self.task_type = 'cls' # ADNI # 'cls' or 'reg' #####
                self.label_name = 'Dx.new' # ADNI # `Dx.new` #####
                self.num_classes = 2 # ADNI - AD vs CN or MCI vs CN or AD vs MCI or reg #####
                self.task_name = "AD/CN"
                self.iter_strat_label = {"binary" : ['PTGENDER'], "multiclass" : [] ,"continuous" : ["PTAGE"]} #MUST BE IN LIST FORM 
                
            elif task == "test_age":
                self.nb_epochs = 3
                self.data = '/hpcgpfs01/scratch/dyhan316/VAE_ADHD_data/ADNI_T1_data_SAMPLE_for_try' #'./adni_t1s_baseline' # 
                self.label = './csv/fsdat_try_sample.csv' # where the label file is 
                self.task_type = 'reg' # ADNI # 'cls' or 'reg' #####
                self.label_name = 'PTAGE' # ADNI # `Dx.new` #####
                self.num_classes = 1 # ADNI - AD vs CN or MCI vs CN or AD vs MCI or reg #####
                self.task_name = "AGE"

            ###task 정해주기###
            elif "ADNI" in task: #i.e. if ADNI
                raise NotImplementedError("ADNI iter strat labels not decided yet!!")
                ### ADNI
                self.data = '/hpcgpfs01/scratch/dyhan316/VAE_ADHD_data/ADNI_T1_data' #'./adni_t1s_baseline' # ADNI #ADNI dataset path 
                self.label = './csv/fsdat_baseline.csv' # where the label file is 
                
                if task == "ADNI_ALZ_ADCN":
                    self.task_type = 'cls' # ADNI # 'cls' or 'reg' #####
                    self.label_name = 'Dx.new' # ADNI # `Dx.new` #####
                    self.num_classes = 2 # ADNI - AD vs CN or MCI vs CN or AD vs MCI or reg #####
                    self.task_name = "AD/CN"
                    
                elif task == "ADNI_ALZ_ADMCI":
                    self.task_type = 'cls' # ADNI # 'cls' or 'reg' #####
                    self.label_name = 'Dx.new' # ADNI # `Dx.new` #####
                    self.num_classes = 2 # ADNI - AD vs CN or MCI vs CN or AD vs MCI or reg #####
                    self.task_name = "AD/MCI"
                    
                elif task == "ADNI_ALZ_CNMCI":
                    self.task_type = 'cls' # ADNI # 'cls' or 'reg' #####
                    self.label_name = 'Dx.new' # ADNI # `Dx.new` #####
                    self.num_classes = 2 # ADNI - AD vs CN or MCI vs CN or AD vs MCI or reg #####
                    self.task_name = "CN/MCI"
                ###could get more variants here###    
                elif task == "ADNI_sex":
                    self.task_type = 'cls' # ADNI # 'cls' or 'reg' #####
                    self.label_name = 'PTGENDER' # ADNI # `Dx.new` #####
                    self.num_classes = 2 # ADNI - AD vs CN or MCI vs CN or AD vs MCI or reg #####
                    self.task_name = "M/F"
                #not sure if it works, but whatever haha 
                elif task == "ADNI_age":
                    self.task_type = 'reg'
                    self.label_name = "PTAGE"
                    self.num_classes = 1
                    self.task_name = "AGE"
                    
            
            ##possible ABCD options
            ##not sure if doing it like this is a good idea!! but whatever !
            #"ABCD" + "HC" (or not) + "sex" or "ADHD" (이들의 조합으로 만들기 가능)
            elif "ABCD" in task : #if ABCD task 
                raise NotImplementedError("update ABCD with the new data with all the subjects!!")
                self.iter_strat_label = {"binary" : ['sex'], "multiclass" : [] ,"continuous" : ["age", "nihtbx_totalcomp_uncorrected"]} 
                print("\n======\n=======reshape will be used, but since should make it so that the method depends on whether we use BT or yAware!!!!\n======\n=======")
                if "HC" in task : #i.e. if including healthy subs only
                    ###
                    raise NotImplementedError("healthy only version notimplemented yet")
                else : #i.e. include all subjects,
                    self.data = '/hpcgpfs01/scratch/dyhan316/VAE_ADHD_data/ABCD_MNI_CROP'              
                    #self.data = '/scratch/connectome/3DCNN/data/1.ABCD/1.sMRI_fmriprep/preprocessed_masked' #local server
                #'/scratch/connectome/3DCNN/data/1.ABCD/1.sMRI_fmriprep/preprocessed_masked'
                    self.label = '/sdcc/u/dyhan316/VAE_ADHD/barlowtwins/csv/updated_ABCD.csv'
                if "sex" in task : #i.e. if sex classification
                    self.task_type = 'cls'
                    self.label_name = 'sex'
                    self.num_classes = 2
                    self.task_name = "M/W"
                if "ADHD" in task : 
                    self.task_type = 'cls'
                    self.label_name = 'HCvsADHD'
                    self.num_classes = 2
                    #self.task_name = "SecHC"
                    raise NotImplementedError("ADHD not implemented yet ")
                    
            elif "UKB" in task : 
                self.data = '/hpcgpfs01/scratch/dyhan316/VAE_ADHD_data/UKB_MNI_CROP'
                raise NotImplementedError("UKB not done yet, also BT, yAware weights에 따라 resize method등등 다르게 해서 하기!")
                
            else:
                raise NotImplementedError(f"not implemented for {task}")
                    
                    
                
    
                #self.pretrained_path = './weights/BHByAa64c.pth' # ADNI #####
                #self.layer_control = 'tune_all' # ADNI # 'freeze' or 'tune_diff' (whether to freeze pretrained layers or not) #####
            
         #below : for barlow twins (where the input_size is different)
        """elif self.mode == FINE_TUNING:
            ## We assume a classification task here
            self.batch_size = 8
            self.nb_epochs_per_saving = 10
            self.pin_mem = True
            self.num_cpu_workers = 1
            self.nb_epochs = 100 # ADNI #####
            self.cuda = True
            # Optimizer
            self.lr = 1e-4
            self.weight_decay = 5e-5
            self.tf = 'cutout' # ADNI
            self.model = 'DenseNet' # 'UNet'
            ### ADNI
            self.data = '/scratch/connectome/study_group/VAE_ADHD/data' #'./adni_t1s_baseline' # ADNI
            self.label = './csv/fsdat_baseline.csv' # ADNI
            self.valid_ratio = 0.25 # ADNI (valid set ratio compared to training set)
            self.input_size = (1, 99, 117, 95) # ADNI

            self.task_type = 'cls' # ADNI # 'cls' or 'reg' #####
            self.label_name = 'Dx.new' # ADNI # `Dx.new` #####
            self.num_classes = 2 # ADNI - AD vs CN or MCI vs CN or AD vs MCI or reg #####

            #self.pretrained_path = './weights/BHByAa64c.pth' # ADNI #####
            #self.layer_control = 'tune_all' # ADNI # 'freeze' or 'tune_diff' (whether to freeze pretrained layers or not) #####
            self.patience = 20 # ADNI
       """
