import pandas as pd 
import datetime as dt
import os

def excel_date(date1):
    temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def readWellNames (file_path):
    data = pd.read_csv(file_path)
    return( data['Well'])

def readWellData (file_path,sheet_name='Manual WLs'):
    df = pd.read_excel (file_path, sheet_name)
    return (df[['Well ID','Water Level (masl)','Date-Time']])

def getWellData(wellName,wellData):
    df = wellData[wellData['Well ID'] == wellName]
    if len(df)== 0:
        print ('\n\n@@@@@@@@ \n' + wellName + ' does not exist! \n@@@@@@@@@@')
        return df

    df = df.dropna()

    if len(df)== 0:
        print ('\n\n@@@@@@@@ \n' + wellName + ' exists but does not have valid record! \n@@@@@@@@@@')
        return df

    return df

def writeData(singleWellName, singleWellData):
    with open('MLWC_Manual_WL_readings.txt', 'a') as f:
        f.write('Variables= "Time (d)""Head (m ASL)"	\n')
        f.write('zone t="' + singleWellName + '"' + '\n')
        singleWellData.to_csv(f, columns = ['Date-Time','Water Level (masl)'], header = False, index=False, sep='\t', float_format="%.2f")
        f.close()

def calcMedian(singleWellName, singleWellData, startDay = '2005-10-01', endDay='2018-01-01'):
    with open('median_manual_WL_'+startDay+"_"+endDay+'.txt','a') as f:
        if len(singleWellData)==0:
            f.write(singleWellName + '\t' + "NaN" +"\n")
        else:
            singleWellData['Date-Time'] = pd.to_datetime(singleWellData["Date-Time"])
            singleWellData = singleWellData.set_index('Date-Time')
            target = singleWellData[startDay:endDay]
            median = target.median(axis=0)
            f.write(singleWellName + '\t' + str(median)[22:-15]+"\n")
        f.close()

#Output directory
os.chdir("D:\MLWC\well_2019\Tecplot_input_2019")
wellFilePath = 'D:\MLWC\well_2019\well_list_2019_final - manual.csv'
wellDataFilePath = r'D:\MLWC\well_2019\FH - Manual Water Level Measurements v4.0.xlsx'

wellNames = readWellNames(wellFilePath)
wellData = readWellData (wellDataFilePath)

for well in wellNames:
    data = getWellData(well,wellData)
    #remove recordless well names to output file
    #if len(data) == 0: continue
    calcMedian(well,data)
    #data['Date-Time'] = data['Date-Time'].apply(excel_date)
    #writeData(well,data)



#single well test
#well ='FH11-MW-002'
#data = getWellData(well,wellData)

# # if len(data) == 0: continue

# data['Date-Time'] = data['Date-Time'].apply(excel_date)
# writeData(well,data)