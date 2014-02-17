
# In[285]:

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re as re
import np as n


# In[286]:

# mutual fund ticker symbol
portfolio = {"Company": "Nationwide", 
             "Funds": {"US Equity":'GRMAX',
                       "International Equity":'GIIAX', 
                       "Bonds": 'GBIAX'}}


# In[287]:

# new df to store the data
df = pd.DataFrame(columns={'Company', 'Symbol', '3 Fund Type', 'Fund Name', 'Y! Category', 'Expense Ratio'})


# In[288]:

for fund_type, ticker in portfolio["Funds"].items():
    
    options_url = 'http://finance.yahoo.com/q?s=' + ticker
    options_page = urlopen(options_url)
    
    soup = BeautifulSoup(options_page)
    
    for title in soup.findAll("div", {"class": "title"}):
        fund_name = title.text
        
    for cell in soup.findAll("th", {"scope": "row"}):
        if 'Category' in cell.text: 
            category = cell.nextSibling.text
            
    for cell in soup.findAll("th", {"scope": "row"}):
        if 'Annual' in cell.text:
           expense = float(re.sub(r'\%', ' ', cell.nextSibling.text))
            
    df = df.append({'Company': portfolio["Company"],
                    'Symbol': ticker,
                    '3 Fund Type':fund_type, 
                    'Fund Name': fund_name, 
                    'Y! Category': category, 
                    'Expense Ratio': expense},
                   ignore_index = True)


# In[289]:

df


# Out[289]:

#       Expense Ratio                                  Fund Name     Company Symbol  \
#     0         $0.70  Nationwide International Index A (GIIAX)   Nationwide  GIIAX   
#     1         $0.57        Nationwide S&P 500 Index A (GRMAX)   Nationwide  GRMAX   
#     2         $0.66           Nationwide Bond Index A (GBIAX)   Nationwide  GBIAX   
#     
#                 3 Fund Type             Y! Category  
#     0  International Equity     Foreign Large Blend  
#     1             US Equity             Large Blend  
#     2                 Bonds  Intermediate-Term Bond  
#     
#     [3 rows x 6 columns]

# In[290]:

df.index = df["3 Fund Type"]


# In[291]:

# assumes a 60% stock, 40% bonds with 30% equity in international
total_expense = (df.ix["US Equity"]["Expense Ratio"] * .42 + 
                 df.ix["International Equity"]["Expense Ratio"] * .18 + 
                 df.ix["Bonds"]["Expense Ratio"] * .40)


# In[292]:

total_expense


# Out[292]:

#     0.6294

# In[306]:

# set variables
start_amount = 100000
start_date = '1/1/2014'
start_age = 30
retirement_age = 62
expected_return = .05
annual_contributions = 20000
years = retirement_age - start_age


# In[307]:

rng = pd.date_range(start_date, periods=years, freq='A')


# In[308]:

n = np.arange(start_age, start_age + years, 1)


# In[309]:

df = {"year": rng, "age":n, "start":NaN, "contributions": annual_contributions}


# In[310]:

df = pd.DataFrame(df)


# In[311]:

for i in range(0, len(rng)):
    if i == 0:
        df["start"][i] = start_amount
    else:
        df["start"][i] = df["net balance"][i-1]
    
    df["growth"] = (df["contributions"] + df["start"]) * (expected_return)
    df["balance"] = df["start"] + df["contributions"] + df["growth"]
    df["expenses"] = df["balance"] * (total_expense/100)
    df["net balance"] = df["balance"] - df["expenses"]


# In[312]:

df.tail()


# Out[312]:

#         age  contributions         start                year     growth  \
#     27   57          20000 $1,347,988.57 2041-12-31 00:00:00 $68,399.43   
#     28   58          20000 $1,427,347.37 2042-12-31 00:00:00 $72,367.37   
#     29   59          20000 $1,510,149.65 2043-12-31 00:00:00 $76,507.48   
#     30   60          20000 $1,596,544.84 2044-12-31 00:00:00 $80,827.24   
#     31   61          20000 $1,686,688.82 2045-12-31 00:00:00 $85,334.44   
#     
#              balance   expenses   net balance  
#     27 $1,436,388.00  $9,040.63 $1,427,347.37  
#     28 $1,519,714.74  $9,565.08 $1,510,149.65  
#     29 $1,606,657.14 $10,112.30 $1,596,544.84  
#     30 $1,697,372.08 $10,683.26 $1,686,688.82  
#     31 $1,792,023.26 $11,278.99 $1,780,744.26  
#     
#     [5 rows x 8 columns]

# In[313]:

df["growth"].sum()


# Out[313]:

#     1199254.5335789856

# In[314]:

df["expenses"].sum()


# Out[314]:

#     158510.26872126883

# In[315]:

balances = pd.melt(df[['age','expenses']], id_vars=['age'])


# In[304]:

ggplot(balances, aes('age', 'value', colour = 'variable')) + geom_point() + stat_smooth()


# Out[304]:

# image file:

#     <ggplot: (282174497)>
