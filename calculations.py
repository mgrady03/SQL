import os
import pandas as pd
import datetime
import numpy as np

class Calculations:
    def __init__(self, files):
        self.trips = self.produce_trips_table(files)
        self.daily_counts = self.calculate_daily_counts(self.get_trips())
        self.monthly_counts = self.calculate_monthly_counts(self.get_trips())
    
    def get_trips(self):
        return self.trips

    def get_daily_counts(self):
        return self.daily_counts

    def get_monthly_counts(self):
        return self.monthly_counts

    def produce_trips_table(self, files):
        # DataFrame must have at least the 'Bikeid', 'Starttime', 'Trip id', 'From station id', 'To station id' columns
        '''#1 try
        dfs = []
        for file in files:
            df = pd.read_csv(file, parse_dates=['Starttime'])
            dfs.append(df)

        trips_df = pd.concat(dfs)
        trips_df = trips_df[['Bikeid', 'Starttime', 'From station id', 'To station id']]
        
        return trips_df
        '''
        #2 try
        dataframes = []
        for file in files:
            df = pd.read_csv(file)
            # Convert 'Starttime' column to datetime format
            df['Starttime'] = pd.to_datetime(df['Starttime'], format='%m/%d/%Y %H:%M')
            dataframes.append(df)
        trips_table = pd.concat(dataframes, ignore_index=True)
        return trips_table

    
    def calculate_daily_counts(self, trips):
        # DataFrame must have "day", "station_id", "fromCNT", "toCNT" and "rebalCNT" columns
        '''#1 try
        daily_counts_df = trips.copy()
        
        daily_counts_df['day'] = daily_counts_df['Starttime'].dt.strftime('%m/%d/%Y')
        daily_counts_df = daily_counts_df.groupby(['day', 'From station id']).size().reset_index(name='fromCNT')
        to_counts = trips.groupby(['day', 'To station id']).size().reset_index(name='toCNT')
        
        daily_counts_df = pd.merge(daily_counts_df, to_counts, how='left', left_on=['day', 'From station id'], right_on=['day', 'To station id'])
        daily_counts_df.fillna(0, inplace=True)
        daily_counts_df['rebalCNT'] = abs(daily_counts_df['fromCNT'] - daily_counts_df['toCNT'])
        
        return daily_counts_df[['day', 'From station id', 'fromCNT', 'toCNT', 'rebalCNT']]
        
        #2 try
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['day'] = trips['Starttime'].dt.strftime('%m/%d/%Y')
        daily_counts = trips.groupby(['day', 'From station id']).size().reset_index(name='fromCNT')
        daily_counts['station_id'] = daily_counts['From station id']
        #daily_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        daily_counts['toCNT'] = trips.groupby(['day', 'To station id']).size().reset_index(name='toCNT')['toCNT']
        daily_counts['rebalCNT'] = np.abs(daily_counts['fromCNT'] - daily_counts['toCNT'])

        #daily_counts['station_id'] = daily_counts['station_id'].astype(int)
        return daily_counts
        
        #3 try 
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['day'] = trips['Starttime'].dt.strftime('%m/%d/%Y')
        daily_counts = trips.groupby(['day', 'From station id']).size().reset_index(name='fromCNT')
        daily_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        daily_counts['toCNT'] = trips.groupby(['day', 'To station id']).size().reset_index(name='toCNT')['toCNT'].fillna(0).astype(int)
        daily_counts['rebalCNT'] = np.abs(daily_counts['fromCNT'] - daily_counts['toCNT']).astype(int)
        return daily_counts
        
        #4 try 
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['day'] = trips['Starttime'].dt.strftime('%m/%d/%Y')
        daily_counts = trips.groupby(['day', 'From station id']).size().reset_index(name='fromCNT')
        daily_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        daily_counts['toCNT'] = trips.groupby(['day', 'To station id']).size().reset_index(name='toCNT')['toCNT'].fillna(0)
        daily_counts['rebalCNT'] = np.abs(daily_counts['fromCNT'] - daily_counts['toCNT']).fillna(0)
       
        daily_counts['toCNT'] = daily_counts['toCNT'].astype(int)
        daily_counts['rebalCNT'] = daily_counts['rebalCNT'].astype(int)
        return daily_counts
        '''
        #5 try im gonna kms
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['day'] = trips['Starttime'].dt.strftime('%m/%d/%Y')
        daily_counts = trips.groupby(['day', 'From station id']).size().reset_index(name='fromCNT')
        daily_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        daily_counts['toCNT'] = trips.groupby(['day', 'To station id']).size().reset_index(name='toCNT')['toCNT'].fillna(0)
        daily_counts['rebalCNT'] = np.abs(daily_counts['fromCNT'] - daily_counts['toCNT']).fillna(0)


        daily_counts['station_id'] = daily_counts['station_id'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        daily_counts['toCNT'] = daily_counts['toCNT'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        daily_counts['rebalCNT'] = daily_counts['rebalCNT'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        daily_counts['day'] = daily_counts['day'].astype(str)
        #print(daily_counts.dtypes)
        #print(daily_counts.isnull().sum())
        return daily_counts
        '''
        #ok 6 f this 
        temporary = self.trips.copy()
        temporary['day'] = pd.to_datetime(temporary['Starttime']).dt.strftime('%m/%d/%Y')
        temporary.sort_values(by = ['Bikeid', 'Starttime'], inplace=True)
        temporary['prev_station_id'] = temporary.groupby('Bikeid')['To station id'].shift()
        temporary['rebal'] = (temporary['From station id'] != temporary['prev_station_id']) & (temporary['From station id'].notna())
        temporary['first_appearance'] = temporary.groupby('Bikeid')['Starttime'].transform('min')
        temporary.loc[temporary['Starttime'] == temporary['first appearance'],'rebal'] = False

        rebalCNT = temporary.groupby ( ['day', 'From station id']) ['rebal'].sum().reset_index()
        rebalCNT.rename(columns = {'From station id':'station_id','rebal': 'rebalCNT'}, inplace = True)
        rebalCNT['rebalCNT'] = rebalCNT['rebalCNT'].astype(int)

        fromCNT = temporary.groupby(['day', 'From station id']).size().reset_index(name='fromCNT')
        toCNT = temporary.groupby(['day', 'To station id']).size().reset_index(name = 'toCNT')

        fromCNT.rename(columns = {'From station id': 'station_id'}, inplace=True)
        toCNT.rename(columns={'To station id': 'station_id'}, inplace = True)
                                                
        daily_counts = pd.merge(pd.merge(fromCNT, toCNT, how='outer', on=['day', 'station_id']), rebalCNT, how='outer', on=['day', 'station_id'])
        dailv_counts = dailv_counts.sort_values(by= ['day', 'station id']). reset_index(drop=True)

        daily_counts. fillna(0, inplace=True)
        daily_counts['day'] = daily_counts['day'].astype(str)
        daily_counts['station id'] = daily_counts ['station id'].astype(int)
        dailv_counts['fromCNT'] = dailv_counts[' fromCNT'].astype(int)
        dailv_counts['toCNT'] = dailv_counts['toCNT'].astype(int)
        dailv_counts['rebalcNT'] = dailv_counts['rebalCNT'].astype(int)

        return dailv_counts[['day','station_id', 'fromCNT', 'toCNT', 'rebalCNT']]
        '''
    def calculate_monthly_counts(self, trips):
        # DataFrame must have "month", "station_id", "fromCNT", "toCNT" and "rebalCNT" columns
        '''#1 try
        monthly_counts_df = trips.copy()

        monthly_counts_df['month'] = monthly_counts_df['Starttime'].dt.strftime('%m/%Y')
        monthly_counts_df = monthly_counts_df.groupby(['month', 'From station id']).size().reset_index(name='fromCNT')
        

        to_counts = trips.groupby(['month', 'To station id']).size().reset_index(name='toCNT')
        monthly_counts_df = pd.merge(monthly_counts_df, to_counts, how='left', left_on=['month', 'From station id'], right_on=['month', 'To station id'])
        monthly_counts_df.fillna(0, inplace=True)
        monthly_counts_df['rebalCNT'] = abs(monthly_counts_df['fromCNT'] - monthly_counts_df['toCNT'])
        
        return monthly_counts_df[['month', 'From station id', 'fromCNT', 'toCNT', 'rebalCNT']]    
        
        #2 try
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['month'] = trips['Starttime'].dt.strftime('%m/%Y')
        
        monthly_counts = trips.groupby(['month', 'From station id']).size().reset_index(name='fromCNT')
        #monthly_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        monthly_counts['station_id'] = monthly_counts['From station id']
        monthly_counts['toCNT'] = trips.groupby(['month', 'To station id']).size().reset_index(name='toCNT')['toCNT']
        monthly_counts['rebalCNT'] = np.abs(monthly_counts['fromCNT'] - monthly_counts['toCNT'])

        #monthly_counts['station_id'] = monthly_counts['station_id'].astype(int)
        return monthly_counts
        
        #3 try 
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['month'] = trips['Starttime'].dt.strftime('%m/%Y')
        monthly_counts = trips.groupby(['month', 'From station id']).size().reset_index(name='fromCNT')
        monthly_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        monthly_counts['toCNT'] = trips.groupby(['month', 'To station id']).size().reset_index(name='toCNT')['toCNT'].fillna(0).astype(int)
        monthly_counts['rebalCNT'] = np.abs(monthly_counts['fromCNT'] - monthly_counts['toCNT']).astype(int)
        return monthly_counts
        
        #4 try 
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['month'] = trips['Starttime'].dt.strftime('%m/%Y')
        monthly_counts = trips.groupby(['month', 'From station id']).size().reset_index(name='fromCNT')
        monthly_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        monthly_counts['toCNT'] = trips.groupby(['month', 'To station id']).size().reset_index(name='toCNT')['toCNT'].fillna(0)
        monthly_counts['rebalCNT'] = np.abs(monthly_counts['fromCNT'] - monthly_counts['toCNT']).fillna(0)
        
        monthly_counts['toCNT'] = monthly_counts['toCNT'].astype(int)
        monthly_counts['rebalCNT'] = monthly_counts['rebalCNT'].astype(int)
        return monthly_counts
        '''
        #5 try if this doesn't work ima be so mad 
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['month'] = trips['Starttime'].dt.strftime('%m/%Y')
        monthly_counts = trips.groupby(['month', 'From station id']).size().reset_index(name='fromCNT')
        monthly_counts.rename(columns={'From station id': 'station_id'}, inplace=True)
        monthly_counts['toCNT'] = trips.groupby(['month', 'To station id']).size().reset_index(name='toCNT')['toCNT'].fillna(0)
        monthly_counts['rebalCNT'] = np.abs(monthly_counts['fromCNT'] - monthly_counts['toCNT']).fillna(0)

        monthly_counts['station_id'] = monthly_counts['station_id'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        monthly_counts['toCNT'] = monthly_counts['toCNT'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        monthly_counts['rebalCNT'] = monthly_counts['rebalCNT'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        monthly_counts['month'] = monthly_counts['month'].astype(str)
        #print(monthly_counts.dtypes)
        #print(monthly_counts.isnull().sum())
        return monthly_counts
        '''
        #6 ugh
        daily_counts = self.get_daily_counts().copy()
        daily_counts['month'] = pd.to_datetime(daily_counts['day']).dt.strftime('m'/'%Y')
        monthly_counts = daily_counts.groupby(['month', 'station_id']).agg({'toCNT': 'sum', 'fromCNT':'sum', 'rebalCNT': 'sum'}).reset_index()
        return monthly_counts[['month', 'station_id', 'fromCNT', 'toCNT', 'rebalCNT']]
        '''
        
if __name__ == "__main__":
    calculations = Calculations(['HealthyRideRentals2021-Q1.csv', 'HealthyRideRentals2021-Q2.csv', 'HealthyRideRentals2021-Q3.csv'])
    print("-------------- Trips Table ---------------")
    print(calculations.get_trips().head(10))
    print()
    print("-------------- Daily Counts ---------------")
    print(calculations.get_daily_counts().head(10))
    print()
    print("------------- Monthly Counts---------------")
    print(calculations.get_monthly_counts().head(10))
    print()