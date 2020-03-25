text = open("covid_19_merged_dataset_updated_now.csv", "r")
text = ''.join([i for i in text]) \
    .replace("/", "-")
print('Replaced')
x = open("output.csv","w")
x.writelines(text)
x.close()
