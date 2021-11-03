import pandas as pd

terror_org_clean_url = '/Users/edcarron/DataSets/FacebookStuff/bannedList/organisations/terror_org_clean.csv'
military_org_dirty_url = '/Users/edcarron/DataSets/FacebookStuff/bannedList/organisations/militias_org.csv'

df = pd.read_csv(military_org_dirty_url)

df

def cleanCouncil(row):
    row[1] = 'Terror'
    return row

df = df.apply(lambda x: cleanCouncil(x), axis=1)

df.fillna('not known', inplace=True)

df.to_csv(terror_org_clean_url)