import pandas as pd
import requests
import time
import json

df = pd.read_csv('/Users/edcarron/DataSets/LA_and_Regional_Spreadsheet_1920_rev.xlsx - Table_1.csv')

for col in df.columns:
    print(col)





def reject(row):
    return (row['Local authority collected - estimated rejects (tonnes)'] / row['Total local authority collected waste (tonnes)']) * 100


df['% rejected'] = df.apply (lambda row: reject(row), axis=1)

df = df.sort_values(by='% rejected', ascending=False)

df




df = pd.read_csv('/Users/edcarron/DataSets/lordsExpenses/allowances-expenses-2021-22-month2-may.csv')

for col in df.columns:
    print(col)

dfleast = df[df['No of Days Attended'] == df['No of Days Attended'].min()]

dfbiggestincome = df[df['Supplementary Allowance'] == df['Supplementary Allowance'].max()]

df

def clean(row):
    for i in range(5, len(row)):
        row[i] = row[i].replace('Nil', '0')
        row[i] = row[i].replace(',', '')
    return row

df = df.apply(lambda x: clean(x), axis=1)

for i in range(5, len(df.columns)):
    df[df.columns[i]] = df[df.columns[i]].astype(float)



file = open('/Users/edcarron/DataSets/Police/cally_crime_data.json', "r")

crime_data = json.load(file)

file.close()

csv_data = []

for year_month, crimes in crime_data.items():
    for crime in crimes:

        if crime['outcome_status'] is not None:
            crime['outcome_status'] = crime['outcome_status']['category']

        crime['longitude'] = crime['location']['longitude']
        crime['latitude'] = crime['location']['latitude']
        crime['street'] = crime['location']['street']['name']
        crime['street_id'] = crime['location']['street']['id']

        crime.pop('location')

        csv_data.append(crime)

crime_data_df = pd.DataFrame.from_records(csv_data, index=None)




url = 'https://data.police.uk/api/crimes-street/all-crime?poly=51.545063362217,-0.12633592882205:51.545413477166,-0.12511611344467:51.545716101282,-0.12401462322378:51.546080058258,-0.12276780878853:51.546589577866,-0.12100051485952:51.546734705333,-0.12046059920389:51.546793201737,-0.12012934596506:51.546813816139,-0.11984162477126:51.546846246739,-0.11944957107652:51.546837028126,-0.11887447789204:51.546824198102,-0.11807453640763:51.54685386489,-0.11751947096626:51.547250783017,-0.1167008706356:51.547932669301,-0.11531705736655:51.548217930722,-0.11471116561283:51.548126349889,-0.11461110482357:51.547603884419,-0.11399664970142:51.546794586679,-0.11304360075384:51.546325308808,-0.11254942810236:51.545959961361,-0.11209293168644:51.545519129739,-0.11174038228255:51.54499929948,-0.111290299459:51.544490669948,-0.11086572252633:51.544438325195,-0.11108292620422:51.544092725926,-0.11245580373106:51.543830951386,-0.11368241492522:51.543284664704,-0.11332298056677:51.543099375488,-0.11331766774504:51.542349011095,-0.11340322857451:51.541857839085,-0.11345123988755:51.540612311274,-0.11356333927138:51.538977859214,-0.11369844141876:51.538685590853,-0.11375119636689:51.536854956407,-0.11388315035059:51.536812805463,-0.11388748916623:51.536768725592,-0.11388931219153:51.536806473091,-0.1146681489216:51.536898881417,-0.11560868119009:51.536945963682,-0.11658310106301:51.53693886087,-0.11658598996066:51.536474620835,-0.11668173028331:51.536438746904,-0.11669056572351:51.535526095706,-0.11691858813083:51.5347833596,-0.11709330099273:51.534505231676,-0.11713636070454:51.534240697829,-0.1171775609619:51.533546675672,-0.11736193263984:51.533366276956,-0.11738408582574:51.533247484707,-0.11737860760444:51.5331301951,-0.11735749530188:51.533013620135,-0.1173220792338:51.532873259536,-0.11725866393249:51.532090919392,-0.11715124332677:51.531135789717,-0.11697699468478:51.53099384631,-0.11933758438828:51.530939386697,-0.11987011832988:51.530849967064,-0.121193034754:51.530791448089,-0.12196968102771:51.530727578606,-0.12253027871078:51.530831808536,-0.12252771890841:51.531109847324,-0.12253790200547:51.532738691881,-0.12243884882618:51.534044528198,-0.1223349168962:51.534568524479,-0.12231464305859:51.534588226329,-0.12231512968341:51.535520828584,-0.12231307192429:51.535823635396,-0.12230320092613:51.536070264539,-0.12231467632386:51.536311501593,-0.12232637380519:51.536886913325,-0.12237492640932:51.537363650665,-0.12249502752395:51.537621323887,-0.12258132170529:51.537920772129,-0.12269877489825:51.538500209145,-0.12304956030714:51.538644807354,-0.12315046333958:51.538893535265,-0.1233522061912:51.539239970326,-0.12370870030863:51.5395166876,-0.12402437342731:51.539815511913,-0.1242716523531:51.540596095303,-0.12483527206031:51.54085933821,-0.12498322223464:51.541117673523,-0.12506042416837:51.541194265228,-0.12506722549154:51.541461427198,-0.12524097587492:51.541760640201,-0.12545364600793:51.542112964904,-0.12566413572477:51.542481626651,-0.12571517601166:51.54273929738,-0.12580149725403:51.542919329299,-0.12587456991666:51.543048620961,-0.12591252068756:51.543188449019,-0.12588384285614:51.5435566987,-0.12596821721674:51.544195010428,-0.12612932334269:51.545063362217,-0.12633592882205&date={date}'

current_month = 8
current_year = 2021


def generate_month():
    return '{year}-{month}'.format(year=current_year, month=current_month)


def go_back_month(month, year):
    if month == 1:
        month = 12
        year = year - 1

    else:
        month = month - 1

    return month, year


go = True

counter = 0

data = {}

while go:

        response = requests.get(url=url.format(date=generate_month()))

        if response.status_code != 200:
            break

        date_data = json.loads(response.text)

        data[generate_month()] = date_data

        if counter == 14:
            time.sleep(1)
            counter = 0

        print(generate_month())
        current_month, current_year = go_back_month(current_month, current_year)

        counter += 1

        if current_year == 2016:
            go = False



file = open('/Users/edcarron/DataSets/Police/cally_crime_data.json', "w")

crime_data = json.dump(data, file)

file.close()








response = requests.get(url='https://data.police.uk/api/crimes-at-location?date=2017-02&location_id=884227')

response







df = pd.read_csv('/Users/edcarron/DataSets/Police/cally_LSOA.csv')


callyDF = df[df['WD18NM'] == 'Caledonian']

callyDF.to_csv('/Users/edcarron/DataSets/Police/cally_LSOA.csv')


df

def cleanCouncil(row):
    row['Amount'] = row['Amount'].replace(',', '')
    return row

df = df.apply(lambda x: cleanCouncil(x), axis=1)

df['Amount'] = df['Amount'].astype(float)

totalSpend = df['Amount'].sum()

people = df['Name'].unique()

total_pay = {}

max = 0

for person in people:
    total_pay[person] = df[df['Name'] == person]['Amount'].sum()








biggest_spend = df[df["Amount"] == df['Amount'].max()]

colstonDf = df[df['Description 3'].str.contains('Colston')]

df








df['Type'].fillna('',inplace=True)
df['Designation Sources'].fillna('None',inplace=True)
df['Region'].fillna('',inplace=True)


def clean(row):

    try:
        if 'Terror' in row['Name']:
            row['Name'] = row['Name'][:-6]
            row['Category'] = ['Terror']
    except:
        pass

    if 'Media Wing' in row['Region']:
        row['Region'] = row['Region'][:-10]
        row['Type'] = 'Media Wing'

    if row['Type'] != '' and row['Type'] != 'Media Wing':
        row['Affiliated With'] = row['Type']
        row['Type'] = ''

    return row






df = df.apply(lambda x: clean(x), axis=1)


df['Affiliated With'].fillna('',inplace=True)


df.to_csv('/Users/edcarron/DataSets/FacebookStuff/bannedList/organisations/terror_org_clean.csv')




df['Scores/Hygiene'] = df['Scores/Hygiene'].astype(int)
df['RatingValue'] = df['RatingValue'].astype(int)


take_df = df[df['BusinessType'] == 'Takeaway/sandwich shop' ]






low_rated_df = df[df['RatingValue'] == '0']

low_rated_df

worst_hyg = df[df["Scores/Hygiene"] == df['Scores/Hygiene'].max()]

print(df['BusinessType'].unique())


df