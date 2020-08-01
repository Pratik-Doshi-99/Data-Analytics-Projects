import nsepy
import pandas as pd
import numpy as np

#
# Read the README file in the directory for better udnerstanding.
#
#


# Inputs:
base_folder = ''  #mention base folder for saving data
logs_folder = ''  #mention folder where the log file will be stored
start = pd.datetime(2020,2,1)   #starting date set to 01-02-2020 to gauge COVID Impact
end = pd.datetime(2020,4,30)    #ending date set to 30-04-2020 to gauge COVID Impact
step_list = [4,5,6]             # the list of depths to be used. in this case, data for OTM options of depth 4, 5 and 6 will be evaluated
min_step = pd.read_csv('path of csv file')    #the csv file that has two columns ('Scrip','Step Size'). Scrip mentions name of scrips in the sample
                                              # and Step Size is the multiple in which the strike price of that scrip must be expressed.
min_step = min_step.set_index('Scrip').T.to_dict()
for i in min_step.keys():
    min_step[i] = min_step[i]['Step Size']
    
expiries = {1:pd.datetime(2020,1,30),2:pd.datetime(2020,2,27),3:pd.datetime(2020,3,26),
            4:pd.datetime(2020,4,30),5:pd.datetime(2020,5,28),6:pd.datetime(2020,6,25),
            7: pd.datetime(2020,7,30)}
            

#Core functions
def getNearestExpiry(date):
    base = expiries[date.month]
    if(date>base):
        return expiries[date.month+1]
    return base


def getOTM(scrip, price, option = 'CE'):
    step = min_step[scrip]
    
    if(option == 'CE'):
        return price + step-((price+step)%step)
    else:
        if(price%step ==0):
            return price - step
        return price - price%step

    
def getDeepOTM(scrip, OTM, option = 'CE', depth = 6):
    if option == 'CE':
        return OTM + depth * min_step[scrip]
    else:
        return OTM - depth*min_step[scrip]
    
def fillRow(date, row):
    if (row.empty):
        return pd.concat([row,pd.DataFrame(index = [date])], sort = False)
    return row
  
  
  
#Main Iteration
for scrip in min_step.keys():
    
    print('Current Scrip: {}'.format(scrip))
    logs = 'Date,Spot,Nearest Expiry,OTM Call Strike,OTM Call Price,OTM Put Strike,OTM Put Price'
    df = nsepy.get_history(scrip, start, end)
    print('A')
    df.reset_index(inplace = True)
    df['Date'] = pd.to_datetime(df['Date'])
    otms_call = pd.DataFrame()
    otms_put = pd.DataFrame()
    deepotms_call = []
    deepotms_put = []
    for s in step_list:
        deepotms_call.append(pd.DataFrame())
        deepotms_put.append(pd.DataFrame())
        logs += ',Call Depth{} Strike,Call Depth{} Price,Put Depth{} Strike,Put Depth{} Price'.format(s,s,s,s)
    logs += '\n'
    
    print('Extracting Data...')
    for i in range(len(df)):  #populates the data rows
        #immediate otm call option 
        date = df.loc[i,'Date']
        close = df.loc[i,'Close']
        logs += '{},{}'.format(date,close)
        if(i%4 == 0):
            print(date)
        
        OTM_call = getOTM(scrip,close,option = 'CE')
        temp_call = nsepy.get_history(scrip, date, date, option_type = 'CE',
                           expiry_date = getNearestExpiry(date),
                           strike_price = OTM_call)
        temp_call = fillRow(date, temp_call)
        otms_call = pd.concat([otms_call,temp_call])
        
        
    
        #immediate otm put option 
        OTM_put = getOTM(scrip,close,option = 'PE')
        temp_put = nsepy.get_history(scrip, date, date, option_type = 'PE',
                           expiry_date = getNearestExpiry(date),
                           strike_price = OTM_put)
        temp_put = fillRow(date, temp_put)
        otms_put = pd.concat([otms_put,temp_put])
        
        
        logs += ',{},{},{},{},{}'.format(temp_call.iloc[0,1], temp_call.iloc[0,3],temp_call.iloc[0,7],
                                        temp_put.iloc[0,3],temp_put.iloc[0,7])
        
        #Deep otm options
        for s,depth in enumerate(step_list):
            #calls
            deep_call = getDeepOTM(scrip, OTM_call, option = 'CE', depth = depth)
            temp2_call = nsepy.get_history(scrip, date, date, option_type = 'CE',
                               expiry_date = getNearestExpiry(date),
                               strike_price = deep_call)
            temp2_call = fillRow(date, temp2_call)
            deepotms_call[s] = pd.concat([deepotms_call[s],temp2_call])
            
            logs += ',{},{}'.format(temp2_call.iloc[0,3],temp2_call.iloc[0,7])
            
            #puts
            deep_put = getDeepOTM(scrip, OTM_put, option = 'PE', depth = depth)
            temp2_put = nsepy.get_history(scrip, date, date, option_type = 'PE',
                               expiry_date = getNearestExpiry(date),
                               strike_price = deep_put)
            temp2_put = fillRow(date, temp2_put)
            deepotms_put[s] = pd.concat([deepotms_put[s],temp2_put])
            
            logs += ',{},{}'.format(temp2_put.iloc[0,3],temp2_put.iloc[0,7])
        logs += '\n'
    
    #storing the generated data
    print('Saving Data Data...')
    with open(logs_folder + '\\{}.csv'.format(scrip),'w') as file:
        file.write(logs)
        
    otms_call.to_csv(base_folder + '\\{}_Call_OTM.csv'.format(scrip))
    otms_put.to_csv(base_folder + '\\{}_Put_OTM.csv'.format(scrip))
    
    for s,st in enumerate(step_list):
        deepotms_call[s].to_csv(base_folder + '\\{}_Call_D{}.csv'.format(scrip,st))
        deepotms_put[s].to_csv(base_folder + '\\{}_Put_D{}.csv'.format(scrip,st))
    
    print('\n\n')
