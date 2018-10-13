# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from collections import defaultdict
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def wh_corr_col(test_dt, maincol, ind_col):

    def tree(): return defaultdict(tree)
    
    cus_info = test_dt[maincol][0].columns[:ind_col]
    fin_info = test_dt[maincol][0].columns[ind_col:]
    W_col = defaultdict(tree)
    cnt = 0
    ant = 0
    M_ttest_col = [i for i in cus_info if len(set(test_dt[maincol][0][i])) <= 2 ]        
    M_anova_col = [i for i in cus_info if len(set(test_dt[maincol][0][i])) > 2 ]        
       
    
    def ttest():
        nonlocal cnt; #nonlocal M_ttest_col 
        
        for ttest_col in M_ttest_col:
            for incnt in range(len(test_dt[maincol])):
                for cp in fin_info:
                    
                    p_value = stats.ttest_ind(test_dt[maincol][incnt][ttest_col], test_dt[maincol][incnt][cp])
                    check_pv = (0.0 < p_value[1]) & (p_value[1] <= 0.05)
                    
                    if check_pv: 
                        cnt +=1
                        if cp not in W_col[maincol][ttest_col].keys():
                            W_col[maincol][ttest_col][cp] = 1
                        else:
                            W_col[maincol][ttest_col][cp] += 1
    
    
    def anova_test():
        nonlocal ant; #nonlocal M_anova_col
        
        for an_cp in fin_info:
            for an_incnt in range(len(test_dt[maincol])):
                for anova_col in M_anova_col:    
                        
                    ols_to = '{} ~ C({})'.format(an_cp, anova_col)
                    an_p_value = anova_lm(ols(ols_to, test_dt[maincol][an_incnt]).fit()) 
                    
                    check_pv = (0.0 < an_p_value.iloc[0,4]) & (an_p_value.iloc[0,4] <= 0.05)
                    
                    if check_pv: 
                        ant +=1
                        if an_cp not in W_col[maincol][anova_col].keys():
                            W_col[maincol][anova_col][an_cp] = 1

                        else:
                           # if isinstance(W_col[maincol][anova_col][an_cp], int):
                           W_col[maincol][anova_col][an_cp] += 1
    
    ttest(); anova_test(); 
    return W_col, ant , cnt
