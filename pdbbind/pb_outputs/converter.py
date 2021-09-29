import pandas as pd

#read file names into an array
file_names=[]
with open('names.txt') as my_file:
	file_names=my_file.read().splitlines()

main_df=pd.DataFrame()
for i in file_names:
	f = open(i, "r")
	data = {}
	for l in f:
    		data.update({l.split('=')[0].replace(' ', ''): [float(l.split('=')[1].replace(' ', '').replace('EDI','').replace('\n', ''))]})

	df = pd.DataFrame.from_dict(data)
	df['name']=i
	main_df=main_df.append(df)
main_df.to_csv('gb_outputs.csv')