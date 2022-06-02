import pandas as pd
from matplotlib.pyplot import pie, axis, show
df = pd.read_csv ('db_election.csv')
sums = df.groupby(df["DISTRICT"])["RUNNERUPPERCENTAGE"].sum()
axis('equal');
pie(sums, labels=sums.index);
show()