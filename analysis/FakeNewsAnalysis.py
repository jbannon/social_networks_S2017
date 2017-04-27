import sys
import numpy as np 
from numpy import *
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import product
from fnparameters import *
sns.set_style("white")


def permTest(data,labelColumn='Basic_Tag',dataColumn='Lex_Div', typeA='Real', typeB='Fake',nperm=200):
	# add in an argument to account for a different estimator type
	#       typeA mean minus typeB mean
	TDIFF = np.mean(data.ix[data[labelColumn]==typeA,:][dataColumn]) - np.mean(data.ix[data[labelColumn]==typeB][dataColumn])
	diff_array = np.empty((nperm))
	csum=0
	labs = data[labelColumn]
	for i in range(nperm):
		labs = np.random.permutation(labs)
		dfRelabeled = pd.concat([pd.Series(labs),data[dataColumn]],axis=1)
		dfRelabeled.columns = [labelColumn,dataColumn]
		dfNewA = dfRelabeled.ix[dfRelabeled[labelColumn]==typeA,:]
		dfNewB = dfRelabeled.ix[dfRelabeled[labelColumn]==typeB,:]
		perm_tdiff = np.mean(dfNewA[dataColumn]) - np.mean(dfNewB[dataColumn])
		diff_array[i] = perm_tdiff
		if perm_tdiff>=TDIFF:
			csum +=1
	return (csum/nperm), diff_array, TDIFF



if __name__=='__main__':
	if len(sys.argv)==1:
		Boostrap, B, perms, varlist, varmap= defParams
	elif len(sys.argv)>1:
		if sys.argv[1].lower() not in ["-m", "-b"]:
			print(helptext)
			sys.exit(0)
		else: 
			if sys.argv[1]=="-m":
				if(len(sys.argv))>3:
					print(helptext)
					sys.exit(0)
				mode = sys.argv[2].lower()
				if mode not in legit_modes:
					print(helptext)
					sys.exit(0)
				elif mode == "full":
					Boostrap, B, perms, varlist, varMap = fullParams
				elif mode =="min":
					Boostrap, B, perms, varlist, varMap = minParams
				elif mode =="def":
					Boostrap, B, perms, varlist, varMap = defParams
				elif mode =="med":
					Boostrap, B, perms, varlist, varMap = medParams
				elif mode =="small":
					Boostrap, B, perms, varlist, varMap = smallParams					
				elif mode =="large":
					Boostrap, B, perms, varlist, varMap = largeParams						
				else:
					Boostrap, B, perms, varlist, varMap = minParams
			if sys.argv[1]=="-b":
				print("hi")
				sys.exit(0)

	dfData = pd.DataFrame.from_csv("processed_articles.csv")
	dfData = dfData.dropna()
	dfData['Basic_Tag'] = np.vectorize(lambda x: 'Real' if x=='Least Biased' else 'Fake')(dfData['category'])
	if Boostrap:
		print("\n Running with nonparametric boostrap p-value estimation \n")
		print("\n Running with " + str(B) + " boostrap iterations")
		print("\t and "+str(perms) + " permuations per permutation test\n")
		for variable in varlist:
			print("\n\t-working on variable " + str(variable) + "\n")
			pvarr =np.zeros((B))
			for i in range(B):
				if i%int(B/4)==0:
					print("bootstrap iter " + str(i))
				pval, values, TDIFF = permTest(dfData,dataColumn = variable, nperm=perms)
				pvarr[i] =pval
				if i==B-1:
					#print("plotting difference in means")
					x = sns.distplot(values,bins=30,kde=False)
					picname = "./plots/meanDiffs/MeanDiffDist_" + str(variable) + "_"+str(i)+".png"
					x.set(xlabel="Difference In Means", ylabel="Binned Frequency",Title="Difference In Means For " +str(varMap[variable]) + "\n with " +str(perms) + "Permuations.\n Boostrap Iteration: " + str(i) + " p-value = " + str(pval))
					x.axvline(x=TDIFF)
					fig = x.get_figure()
					fig.savefig(picname)
					plt.close(fig)
			p_value_sns = sns.distplot(pvarr,hist=False,rug=True)
			p_value_sns.set(xlabel="p-value", ylabel ="Density", Title ="Boostrapped Distribution Over p-values For " +str(varMap[variable]) + "\n with " +str(B) +"Boostrap Iterations")
			p_value_plot = p_value_sns.get_figure()
			temp = pd.DataFrame(pvarr)
			E = np.mean(pvarr)
			p_value_sns.axvline(x=E)
			#temp.to_csv('pvalues_B.csv')
			p_value_plot.savefig("./plots/pvals/p-value_distribution_" + str(varMap[variable]) +".png")
			plt.close(p_value_plot)
	else:
		print("\n Running WITHOUT nonparametric boostrap p-value estimation \n")
		print("\n Running with " + str(perms) + " permutations per permutation test.")
		for variable in varlist:
			print("\n\t-working on variable " + str(variable) + "\n")
			pval,values,TDIFF = permTest(dfData, dataColumn= variable, nperm=perms)
			x = sns.distplot(values,bins=30,kde=False)
			x.set(xlabel="Difference In Means", ylabel="Binned Frequency",Title="Difference In Means For " + str(varMap[variable]) +"\n with " +str(perms) + " Permuations. \n p-value = " + str(pval))
			x.axvline(x=TDIFF)
			x.text(TDIFF,15,"Original Difference =\n " + str(np.round(TDIFF,2)))
			fig = x.get_figure()
			fig.savefig('./plots/meanDiffs/MeanDiffDist_' + str(variable) + '.png')
			plt.close(fig)
