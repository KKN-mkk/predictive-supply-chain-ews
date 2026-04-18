import pandas as pd
# Load the big file locally
df = pd.read_csv('DataCoSupplyChainDataset.csv', encoding='ISO-8859-1')
# Calculate the risk once and save it as a tiny 1KB file
pivot = df.pivot_table(index='Order Region', columns='Shipping Mode', values='delivery status', aggfunc=lambda x: (x == 'Late delivery').mean() * 100)
pivot.to_csv('heatmap_data.csv')
print("Tiny heatmap file created!")