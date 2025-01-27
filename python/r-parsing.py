#!/usr/bin/env python
# coding: utf-8

# In[1]:


# read the R output to parse
import sys
r_output_file = "C:/Users/augus/Downloads/USOPC-time-series-forecasting.html"
file_obj = open(r_output_file, 'r')
raw = file_obj.read()
print(raw)


# In[2]:


# insure beautiful soup 4 and regular expression libraries are installed and then import them
get_ipython().system('pip3 install bs4')
get_ipython().system('pip3 install re')
from bs4 import BeautifulSoup
import re
# prepare a beautiful soup object to parse our html file
soup = BeautifulSoup(raw, 'html.parser')

clean_forecasts = []
# all code blocks with the word Point Forecast correspond to input data
raw_forecasts = soup.find_all(string=re.compile("Point Forecast"))
for forecast in raw_forecasts:
    # find the decimals
    clean_forecasts.append(re.findall(r"[-+]?(?:\d*\.+\d+)", forecast))

clean_forecasts


# In[3]:


raw_name_app = soup.find_all("pre", {"class": "r"})
raw_name_app

raw_string_name_app = []
for entry in raw_name_app:
    raw_string_name_app.append(str(entry))

raw_string_name_app


# In[4]:


clean_name = []
clean_app = []
# for entry in raw_name_app:
#     clean_name.append()
#     clean_app.append()

# zipped = zip(clean_name, clean_app)
for entry in raw_string_name_app:
    something = re.findall('[^\|]\s*Apparatus == "(.+?)"\)*\|*', entry)
    if something:
        clean_app.append(something)
    else:
        clean_app.append(None)
    
clean_app

for entry in raw_string_name_app:
    something = re.findall('LastName == "(.+?)"', entry)
    if something:
        clean_name.append(something)
    else:
        clean_name.append(None)
    
clean_name


# In[5]:


for index in range(len(clean_app)):
    clean_app[index] = clean_app[index][0]

clean_app

for index in range(len(clean_name)):
    clean_name[index] = clean_name[index][0]

clean_name


# In[6]:


for entry in clean_forecasts:
    for index in range(len(entry)):
        entry[index] = float(entry[index])

clean_forecasts
    


# In[7]:


forecasts = list(zip(clean_name, clean_app, clean_forecasts))
forecasts


# In[8]:


oh_no = 0
oh_yes = 0
print(len(forecasts))
for name, app, values in forecasts:
    if len(values) != 11:
        oh_no += 1
        print(name, app) # braunton VT, lincoln UB
    else:
        oh_yes += 1

print(oh_no, oh_yes)


# In[9]:


# We want to change the structure of forecasts so it can be called like
# forecasts[LastName][Apparatus][Interval] and return a value

forecasts
# no more magic numbers, these are tags
intervals = ['Avg', 'Lo 95', 'Hi 95', 'Lo 75', 'Hi 75', 'Lo 55', 'Hi 55', 'Lo 35', 'Hi 35', 'Lo 15', 'Hi 15']
fourcasts = {} # dummy temp variable

for forecast in forecasts:
    # if last name not a key in our dict, add a blank nested dict value
    if forecast[0] not in fourcasts:
        fourcasts[forecast[0]] = {}
    
    # if apparatus not a key in fourcasts[LastName] dict, add dict with interval to forecast values zipped pairs
    if forecast[1] not in fourcasts[forecast[0]]:
        zipped = dict(zip(intervals, forecast[2]))
        fourcasts[forecast[0]][forecast[1]] = zipped

# searchable like this now
#fourcasts['MALONE']['FX']['Avg']

forecasts = fourcasts # assign the old to the new and improved
forecasts


# In[10]:


# testing on forecasts
forecasts['MALONE']['PH']['Avg'] # yay
print(forecasts['BRAUNTON']) # make sure rng can handle only having an avg
print(forecasts['LINCOLN'])


# In[11]:


for name, apparatus in forecasts.items():
    if (len(apparatus.keys()) != 6) & (len(apparatus.keys()) != 4):
        print(name) # ALFONSO DIAB NEWFELD NUNEZ PETROSYAN


# In[12]:


print(forecasts['ALFONSO'].keys())
print(forecasts['DIAB'].keys())
print(forecasts['NEWFELD'].keys())
print(forecasts['NUNEZ'].keys())
print(forecasts['PETROSYAN'].keys())
print(forecasts['SUN'].keys()) # all of these incompletes are male gymnasts


# In[13]:


m_apps = set(['FX', 'VT', 'SR', 'PH', 'HB', 'PB'])
for name, apparatuses in forecasts.items():
    if name in ['ALFONSO', 'DIAB', 'NEWFELD', 'NUNEZ', 'PETROSYAN', 'SUN']:
        add_apps = m_apps - set(apparatuses.keys())
        for new_app in add_apps:
            apparatuses[new_app] = {}
            apparatuses[new_app]['Avg'] = 0.0


# In[14]:


print(forecasts['ALFONSO'].keys())
print(forecasts['DIAB'].keys())
print(forecasts['NEWFELD'].keys())
print(forecasts['NUNEZ'].keys())
print(forecasts['PETROSYAN'].keys())
print(forecasts['SUN'].keys()) # all of these incompletes are male gymnasts


# In[15]:


thirtieths = [0.0]
x = 0.0
while x <= 20.0:
    x += 1/30
    thirtieths.append(x)


# In[16]:


thirtieths


# In[17]:


from bisect import bisect_left

def round_thirtieths(myNumber):
    """
    Assumes thirtieths is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(thirtieths, myNumber)
    if pos == 0:
        return thirtieths[0]
    if pos == len(thirtieths):
        return thirtieths[-1]
    before = thirtieths[pos - 1]
    after = thirtieths[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


# In[18]:


test = round_thirtieths(0.11)
test


# In[19]:


forecasts


# # We now would like to get historical records of past games
# # 2012 and 2016
# ## x Mens and Womens
# ### Team Qualifying Sums
# ### Team Final Sums
# ### AA qualifying sums
# ### AA final sums
# ### Event qualifyings by 4 or 6 apparatuses
# ### Event finals by 4 or 6 apparatuses
# 
# # Mens + Women's
# # = 2*(12+4) + 2*(8+4)
# # = 32 + 24
# # = 56 tables

# In[20]:


genders = ['M', 'W']
years = ['2012', '2016']
phases = ['qual', 'final']
groupings = ['team', 'aa', 'event']

m_apps = ['VT', 'SR', 'PH', 'PB', 'HB', 'FX']
w_apps = ['BB', 'VT', 'FX', 'UB']


# In[21]:


historical_data = {}
for year in years:
    historical_data[year] = {}
    for gender in genders:
        if gender == 'M':
            apps = m_apps
        else:
            apps = w_apps
        historical_data[year][gender] = {}
        for phase in phases:
            historical_data[year][gender][phase] = {}
            for grouping in groupings:
                if grouping == 'event':
                    historical_data[year][gender][phase][grouping] = {}
                    for app in apps:
                        historical_data[year][gender][phase][grouping][app] = []
                else:
                    historical_data[year][gender][phase][grouping] = []


# In[22]:


historical_data


# In[23]:


historical_data


# In[24]:


# Men's 2012 London Games results see the source at https://gymnasticsresults.com/results/2012/olympics/documents/ga_results_book.pdf
# Note: Threshold to Qual is taken as the 8th highest non-US score
historical_data['2012']['M']['qual']['team'] = 265.587 # team total threshold to qual
historical_data['2012']['M']['final']['team'] = [275.997, 271.952, 271.711] # medaled team scores in order of podium plus 4th
historical_data['2012']['M']['qual']['aa'] = 83.931 # thresh to qual
historical_data['2012']['M']['final']['aa'] = [92.690, 91.031, 90.698, 90.432] # medaled aa in order of podium plus 4th
historical_data['2012']['M']['qual']['event']['VT'] = 16.200 # thresh to qual for event final
historical_data['2012']['M']['qual']['event']['SR'] = 15.308 # ' '
historical_data['2012']['M']['qual']['event']['PH'] = 14.900
historical_data['2012']['M']['qual']['event']['PB'] = 15.366
historical_data['2012']['M']['qual']['event']['HB'] = 15.100
historical_data['2012']['M']['qual']['event']['FX'] = 15.433

historical_data['2012']['M']['final']['event']['VT'] = [16.533, 16.399, 16.316] # medaled event scores plus 4th
historical_data['2012']['M']['final']['event']['SR'] = [15.900, 15.800, 15.733] # ' '
historical_data['2012']['M']['final']['event']['PH'] = [16.066, 16.066, 15.600]
historical_data['2012']['M']['final']['event']['PB'] = [15.966, 15.800, 15.566]
historical_data['2012']['M']['final']['event']['HB'] = [16.533, 16.400, 16.366]
historical_data['2012']['M']['final']['event']['FX'] = [15.933, 15.800, 15.366]


# In[25]:


# Men's 2016 Rio Games results see the source at https://library.olympics.com/Default/doc/SYRACUSE/165312/results-book-rio-2016-organising-committee-for-the-olympic-and-paralympic-games-in-rio-in-2016?_lg=en-GB
historical_data['2016']['M']['qual']['team'] = 260.262 # 
historical_data['2016']['M']['final']['team'] = [274.094, 271.453, 271.122]
historical_data['2016']['M']['qual']['aa'] = 84.565
historical_data['2016']['M']['final']['aa'] = [92.365, 92.266, 90.641]
historical_data['2016']['M']['qual']['event']['VT'] = 15.149
historical_data['2016']['M']['qual']['event']['SR'] = 15.333
historical_data['2016']['M']['qual']['event']['PH'] = 15.300
historical_data['2016']['M']['qual']['event']['PB'] = 15.466
historical_data['2016']['M']['qual']['event']['HB'] = 15.116
historical_data['2016']['M']['qual']['event']['FX'] = 15.200

historical_data['2016']['M']['final']['event']['VT'] = [15.691, 15.516, 15.449]
historical_data['2016']['M']['final']['event']['SR'] = [16.000, 15.766, 15.700]
historical_data['2016']['M']['final']['event']['PH'] = [15.966, 15.833, 15.600]
historical_data['2016']['M']['final']['event']['PB'] = [16.041, 15.783, 15.766]
historical_data['2016']['M']['final']['event']['HB'] = [15.766, 15.466, 15.400]
historical_data['2016']['M']['final']['event']['FX'] = [15.633, 15.533, 15.433]


# In[26]:


# Women's 2012 results
# Note: Different Apparatuses from Men, all else is the same
historical_data['2012']['W']['qual']['team'] = 167.331
historical_data['2012']['W']['final']['team'] = [178.530, 176.414, 174.430]
historical_data['2012']['W']['qual']['aa'] = 53.698
historical_data['2012']['W']['final']['aa'] = [61.973, 59.566, 58.833]
historical_data['2012']['W']['qual']['event']['BB'] = 14.433
historical_data['2012']['W']['qual']['event']['VT'] = 13.924
historical_data['2012']['W']['qual']['event']['FX'] = 14.333
historical_data['2012']['W']['qual']['event']['UB'] = 14.866

historical_data['2012']['W']['final']['event']['BB'] = [15.600, 15.500, 15.066]
historical_data['2012']['W']['final']['event']['VT'] = [15.191, 15.050, 15.016]
historical_data['2012']['W']['final']['event']['FX'] = [15.200, 14.900, 14.900]
historical_data['2012']['W']['final']['event']['UB'] = [16.133, 15.933, 15.916]


# In[48]:


# Women's 2016 results
historical_data['2016']['W']['qual']['team'] = 171.761
historical_data['2016']['W']['final']['team'] = [176.688, 176.003, 174.371]
historical_data['2016']['W']['qual']['aa'] = 54.866
historical_data['2016']['W']['final']['aa'] = [58.665, 58.549, 58.298]
historical_data['2016']['W']['qual']['event']['BB'] = 14.500
historical_data['2016']['W']['qual']['event']['VT'] = 14.783
historical_data['2016']['W']['qual']['event']['FX'] = 14.300
historical_data['2016']['W']['qual']['event']['UB'] = 15.233

historical_data['2016']['W']['final']['event']['BB'] = [15.466, 14.600, 14.533]
historical_data['2016']['W']['final']['event']['VT'] = [15.253, 15.216, 15.066]
historical_data['2016']['W']['final']['event']['FX'] = [14.933, 14.766, 14.666]
historical_data['2016']['W']['final']['event']['UB'] = [15.900, 15.566, 15.533]


# In[49]:


historical_data


# In[50]:


import math
def reorder_array(array):
    # INPUT: [Lo 95, Hi 95, Lo 75, Hi 75, Lo 55, Hi 55, Lo 35, Hi 35, Lo 15, Hi 15]
    # OUPUT: [Lo 95, Lo 75, Lo 55, Lo 35, Lo 15, Hi 15, Hi 35, Hi 55, Hi 75, Hi 95]
    return [array[0], array[2], array[4], array[6], array[8], array[9], array[7], array[5], array[3], array[1]]
    


# In[51]:


def find_lowest_neighbor_index(number, array):
   i = 0
   while i < len(array):
        if number < array[i]:
            return i - 1
        i = i + 1


# In[52]:


from numpy import random
from numpy import diff
def rng(upper_lower_bounds_dict):
    # generate a random number (g a rn) on uniform distribution
    number = random.uniform(0.025, 0.975)
    # these are samples where the pdf is known and given
    intervals = [0.025, 0.125, 0.225, 0.325, 0.425, 0.575, 0.675, 0.775, 0.875, 0.975]
    # convert the dict input of Hi 95, Lo 95 etc. from the R code into a usable array
    # array: discrete score as a function of the uniform sample
    # some forecasts only have one value
    if len(upper_lower_bounds_dict.values()) == 1:
        return list(upper_lower_bounds_dict.values())[0]
    upper_lower_bounds_array = reorder_array(list(upper_lower_bounds_dict.values())[1:])
    # get index of the closest interval to the left of the sample
    index = find_lowest_neighbor_index(number, intervals)
    # find the slopes between points in the forecast
    slopes = diff(upper_lower_bounds_array)
    # del{x} for some fun linear interpolation
    run = number - intervals[index]
    # if it were possible to get continuous scores in artistic gymnastics.....
    raw_score = upper_lower_bounds_array[index] + run*slopes[index]
    # round to the nearest thirtieth of a point!
    output = round_thirtieths(raw_score)
    return output
    # 1 find the closest lower neighbor for number from the intervals of []
    # 2 find the slopes of each piecewise point line
    # 3 compute the value of the function at the number
    # 4 round to the nearest thirtieth
    # upper_lower_bounds looks like Avg, Lo 95, Hi 95, Lo 75, Hi 75, Low 55, Hi 55, Low 35, Hi 35, Low 15, Hi 15


# In[53]:


assert reorder_array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == ([1, 3, 5, 7, 9, 10, 8, 6, 4, 2])


# In[54]:


print(rng(forecasts['MALONE']['FX']))


# In[55]:


w_apps = set(['FX', 'VT', 'UB', 'BB'])
m_apps = set(['FX', 'VT', 'SR', 'PH', 'HB', 'PB'])

gymnasts = {'M': {}, 'W': {}, 'G': {}}

for athelete, apps in forecasts.items():
    gender = 'G'
    if set(apps.keys()) <= w_apps:
        gender = 'W'
    elif set(apps.keys()) <= m_apps:
        gender = 'M'
    else:
        print(athelete, apps, w_apps, m_apps)
        break
    gymnasts[gender][athelete] = apps
    
gymnasts['G']


# In[56]:


for athelete, apps in forecasts.items():
    print(athelete, apps)


# In[57]:


gymnasts['W']


# In[58]:


print(len(gymnasts['W'].keys()))


# =29

# In[59]:


print(len(gymnasts['M'].keys()))


# =40

# In[60]:


print(math.comb(len(gymnasts['W'].keys()), 5))


# =118755

# In[61]:


print(math.comb(len(gymnasts['M'].keys()), 5))


# =658008

# In[62]:


M_ID_to_gymnasts = [key for key, val in gymnasts['M'].items()]
M_IDs = [i for i in range(len(M_ID_to_gymnasts))]
W_ID_to_gymnasts = [key for key, val in gymnasts['W'].items()]
W_IDs = [i for i in range(len(W_ID_to_gymnasts))]


# In[63]:


from itertools import combinations
M_teams = list(combinations(M_IDs, 5))
W_teams = list(combinations(W_IDs, 5))


# In[64]:


W_teams


# In[ ]:





# In[65]:


def get_competitors(app, id_to_gymnasts, athelete_ids):
    #check how many valid forecasts we have for this app on this team
    averages = [forecasts[id_to_gymnasts[id]][app]['Avg'] for id in athelete_ids]
    id_averages = list(zip(athelete_ids, averages))
    # return: tuple of remaining IDs
    return [id for id, val in id_averages if val > min(averages)]


# In[66]:


def update_scorecard(scorecard, score, app, id):
    scorecard[app][id] = score
    return scorecard
def get_team_qual(year, gender, scorecard):
    points = 0.0
    scoresheet = [set(apparatus.values()) for apparatus in scorecard.values()]
    for team_score in scoresheet:
        team_score.pop()
        points += sum(team_score)
    return points >= historical_data[year][gender]['qual']['team']
def get_aa_qual(year, gender, scorecard):
    pass
def get_event_qual(year, gender, scorecard):
    pass
def sim_team(did_team_qual, scorecard, year, gender, athelete_ids):
    return 0
def sim_aas(aas, scorecard, year, gender, athelete_ids):
    return 0
def sim_events(events, scorecard, year, gender, athelete_ids):
    return 0


# In[67]:


def sim_competition(year, gender, team_id, athelete_ids):
    if gender == 'M':
        apps = m_apps
        id_to_gymnasts = M_ID_to_gymnasts
    elif gender == 'W':
        apps = w_apps
        id_to_gymnasts = W_ID_to_gymnasts
    else:
        raise Exception('Invalid gender')
    
    scorecard = {app: {} for app in apps}
    # qualification
    for app in apps:
        # find competing atheletes by lowest average
        competitors = get_competitors(app, id_to_gymnasts, athelete_ids)
        for id in competitors: 
            score = rng(forecasts[id_to_gymnasts[id]][app])
            #update individual scorecard
            scorecard = update_scorecard(scorecard, score, app, id)
        #update team scorecard, dropping lowest score
    
    did_team_qual = get_team_qual(year, gender, scorecard) # bool
    aas = get_aa_qual(year, gender, scorecard)  # tuple of ids of atheletes who qualed
    events = get_event_qual(year, gender, scorecard) # dict of tuples of ids of atheletes who qualed for each event

    medals = 0
    medals += sim_team(did_team_qual, scorecard, year, gender, athelete_ids)
    medals += sim_aas(aas, scorecard, year, gender, athelete_ids)
    medals += sim_events(events, scorecard, year, gender, athelete_ids)
        

    return did_team_qual


# In[68]:


for id, val in enumerate(W_teams):
    if id <= len(W_teams)/100:
        print(sim_competition('2016', 'W', id, val))
    else:
        break


# In[ ]:


M_ID_to_gymnasts


# In[ ]:




