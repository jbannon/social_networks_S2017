

helptext = """

FakeNewsAnalysis.py is a script designed to perform a permutation test.

You can invoke it in three ways:
	1) no command line arguments:
			python FakeNewsAnalysis.py
		This will run the program in minimal mode, meaning it will be 
		default to the minimum mode parameters (see below).
		This will do a basic single permutation test on lexical diversity.
	
	2) bespoke:
			python FakeNewsAnalysis.py -b BoostBool BoostIter Numperms Columns Names
	
		This allows you to customize your analysis. See the parameter description below.


	3) mode toggled:
			python FakeNewsAnalysis.py -m [def| full | min | small | med | large] 

		This selects between default, full, and minimal modes. These are 
		predetermined parameter sets for the parameters described below. The parameter
		sets are:

			<paramName> = BoostBool | BoostIter | Numperms | Columns | Names
			----------------------------------------------------------------
			----------------------------------------------------------------
			
			* def = True | 481 | 1024 | Lex_Div | Lexical\ Diversity

			* full = True | 500 | 8192 | Lex_Div,Sent_Score,Num_Ex,Num_AllCaps, FK_Grade, Title_Lex_Div, Title_FK_Grade | 
				Lexical\ Diversity,Sentiment\ Score,Number\ Exclamation\ Points,All\ Cap\ Count
							
			* min = False | 0 | 200 | Lex_Div | Lexical\ Diversity

			* small = True | 481 | 200 | Lex_Div | Lexical\ Diversity

			* med =  True  | 500 | 1024 | Lex_Div,Sent_Score | Lexical\ Diversity,Sentiment\ Score 

			* large = True | 500 | 8192 | Lex_Div,Sent_Score,Num_Ex | 
									Lexical\ Diversity,Sentiment\ Score,Number\ Exclamation\ Points

			
	
			
	It's recommended to run using the -m flag.
	The -b flag is not yet implemented.

	******************************************************************
	*	Parameter Descriptions:				         *	
	******************************************************************

	BoostBool := Boolean that indicates whether or not you want to 
						 bootstrap a distribution over p values
	BoostIter := The number of bootstrap iterations you want to perform
						 It's ignored if BoostBool is false. 
	Numperms  := How many permutations you want to use for each permuation test

	Columns   := The NAMES of the columns in your dataset that you want to test 
						 These should be quantitative columns. These should be 
						 separated by commas and spaces should be escaped, for example:
						 		Lex_Div,Column\ A,ColumnB

						 There should NOT be spaces between the column names.

	Names     := The TITLES you want to give your columns when you plot them. This exists
						 because often you want to call something one thing
						 in a data set but something else when referring to
						 it in written language.




"""

## PARAMS
## add file to read in maybe
##
legit_modes = ['def', 'full','min', 'small', 'med', 'large']
defParams = [True, 481, 1024,['Lex_Div'],{'Lex_Div':"Lexical Diversity"}]
fullParams = [True, 500, 2048, ['Lex_Div','Sent_Score','Num_Ex', 'Num_AllCaps','FK_Grade', 'Title_Lex_Div', 'Title_FK_Grade'],{'Lex_Div': 'Lexical Diversity', 'Sent_Score' : 'Sentiment Score', 'Num_Ex':'Number Exclamation Points', 'Num_AllCaps':'All Cap Count', 'FK_Grade':'FK Grade Level ', 'Title_Lex_Div': 'Lexical Diversity (Title)', 'Title_FK_Grade': 'FK Grade (Title)'}]
minParams =  [False, 0, 200, ['Lex_Div'], {'Lex_Div':"Lexical Diversity"}]
smallParams = [True, 481, 200,['Lex_Div'],{'Lex_Div':"Lexical Diversity"}]
medParams =   [True, 481, 200,['Lex_Div','Sent_Score'],{'Lex_Div':"Lexical Diversity",'Sent_Score' : 'Sentiment Score'}]
largeParams = [True, 4, 1024,['Lex_Div','Sent_Score','Num_Ex'],{'Lex_Div': 'Lexical Diversity', 'Sent_Score' : 'Sentiment Score', 'Num_Ex':'Number Exclamation Points'}]
estTitleMap = {"mean": "Difference In Means"}
