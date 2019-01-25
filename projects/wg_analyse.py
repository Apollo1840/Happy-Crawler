# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 21:54:26 2018

@author: zouco

"""
# note: 也可以用中文，没必要用英语

# import numpy as np
import pandas as pd
import re
# import random

import matplotlib.pyplot as plt
# import time


class WgPreprocess():
    
    def __init__(self, df):
        self.df = df
    
    def run(self):
        self.clean()
        self.get_addr_details()
        self.get_date_details()
        self.get_situ_details()
        self.get_want_details()
        
        self.df.room_size = self.df.room_size.astype('float')
        self.df.price = self.df.price.astype('float')
        self.df.reset_index()
        
        self.df.start_date = pd.to_datetime(self.df.start_date)
        self.df.end_date = pd.to_datetime(self.df.end_date)
        self.df['duration_month'] = (self.df.end_date - self.df.start_date).dt.days/30
        self.df['rent_type'] = pd.cut(self.df['duration_month'], bins=3, labels=['short','middle','long'])
        
        
        return self.df
    
    def save_data(self):
        self.df.to_csv('material/The_wg_information_in_munich_modified.csv', encoding='utf-8')
            
    def clean(self):
        df2 = self.df.dropna()
        df2 = df2.loc[df2.caution != -2, :]
        df2 = df2.loc[df2.caution != -1, :]
        df2 = df2.loc[df2.address != 'Error in page', :]
        df2 = df2.loc[df2.address != 'Not format', :]
        
        self.df = df2.drop_duplicates()
        
    
    def get_addr_details(self):
        self.df['street']   = self.df.address.apply(WgPreprocess.transform_addr, return_id=0)
        self.df['zipcode']  = self.df.address.apply(WgPreprocess.transform_addr, return_id=1)
        self.df['city']     = self.df.address.apply(WgPreprocess.transform_addr, return_id=2)
        self.df['area']     = self.df.address.apply(WgPreprocess.transform_addr, return_id=3)

        del self.df['address']
    
    
    @staticmethod
    def transform_addr(addressContent, return_id=0):
        street, zipcode, city, area = None, None, None, None
        
        # find PLZ
        blocks = [content.strip() for content in addressContent.split()]
        for content in blocks:
            if re.match('[0-9]{5}', content):
                zipcode = content
                break
        
        # find others
        addr_content = [row.strip() for row in addressContent.split('\n')]
        addr_content = list(filter(None, addr_content)) # normally it contains 2 rows
        if len(addr_content) >= 2:
            street = addr_content[0]
            
            second_part = addr_content[1].split(' ')
            if len(second_part)>=3:
                city = second_part[1]
                area = second_part[2]
            else:
                city = second_part[0]
        
        result = [street, zipcode, city, area]  
        return result[return_id]
    
    def get_date_details(self):
        self.df['start_date']   = self.df.date.apply(WgPreprocess.transform_date, return_id=0)
        self.df['end_date']     = self.df.date.apply(WgPreprocess.transform_date, return_id=1)
        
        del self.df['date']
    
    @staticmethod
    def transform_date(dateContent, return_id=0):
        start_date, end_date = None, None
        
        pieces = WgPreprocess.information_to_pieces(dateContent, second_level=':')
    
        if pieces[0] == 'frei ab':
            start_date = pieces[1]
        if len(pieces) == 4 and pieces[2] == 'frei bis':
            end_date = pieces[3]
            
        result = [start_date, end_date]
        return result[return_id]
    
    @staticmethod
    def information_to_pieces(text, first_level='\n', second_level=' '):
        pieces = []
        for content in text.split(first_level):
            words = content.split(second_level)
            for word in words:
                word = word.strip() 
                if word:
                    pieces.append(word)
        return pieces
    
    @staticmethod    
    def transform_situation(situation, return_id=0):
        title_split = situation.split()
        totalRenterString = title_split[0] # _er
        renterGenderString = title_split[2] #(_w,_m)
    
        num_total_renter = totalRenterString[0:renterGenderString.find("er")-1]
        num_female_renter = renterGenderString[renterGenderString.find("(")+1:renterGenderString.find("w")]
        num_male_renter = renterGenderString[renterGenderString.find(",")+1:renterGenderString.find("m")]
           
        result = [num_total_renter, num_female_renter, num_male_renter]
        return result[return_id]
    
    def get_situ_details(self):
        self.df['num_renter']     = self.df.situation.apply(WgPreprocess.transform_situation, return_id=0)
        self.df['num_renter_w']   = self.df.situation.apply(WgPreprocess.transform_situation, return_id=1)
        self.df['num_renter_m']   = self.df.situation.apply(WgPreprocess.transform_situation, return_id=2)

        del self.df['situation']
           
    @staticmethod
    def transform_wanted_list(wanted_list, return_id=0):
        num_wanted_male = 0
        num_wanted_female = 0
        num_no_gender_limit = 0
        
        wanted_list = wanted_list.split('|')

        for wanted in wanted_list[1:-1]:
            if 'oder' in wanted:
                num_no_gender_limit += 1
            elif 'Mitbewohnerin' in wanted:
                num_wanted_female += 1
            elif 'Mitbewohner' in wanted:
                num_wanted_male += 1
            else:
                print("Error in get_situation_details: keyword not found")
        
        result = [num_wanted_male, num_wanted_female, num_no_gender_limit]
        return result[return_id]
    
    def get_want_details(self):
        self.df['num_want_m']       = self.df.wanted_list.apply(WgPreprocess.transform_wanted_list, return_id=0)
        self.df['num_want_w']       = self.df.wanted_list.apply(WgPreprocess.transform_wanted_list, return_id=1)
        self.df['num_want_(m/w)']   = self.df.wanted_list.apply(WgPreprocess.transform_wanted_list, return_id=2)

        del self.df['wanted_list']
        
    def get_addr_details_2(self):
        def transform_addr(addressContent):
            addressContent = addressContent.split()
            
            # Check if the address information is complete
            # Maybe refator it to a check-function
            if len(addressContent) < 5:
                if len(addressContent[1]) < 5:
                    street = addressContent[0] + addressContent[1]
                    zipCode = addressContent[2]
                    city = addressContent[3]
                else:
                    street = addressContent[0]
                    zipCode = addressContent[1]
                    city = addressContent[2]
                    area = addressContent[3]
            else:
                street = addressContent[0] + addressContent[1]
                zipCode = addressContent[2]
                city = addressContent[3]
                area = addressContent[4]
            
            if re.match('[0-9]{5}', zipCode):
                pass
            else:
                zipCode = None
            
            return street + '|' + zipCode + '|' + city + '|' + area
        
        self.df['addressContent'] = self.df.address.apply(transform_addr)
        df_addr = pd.DataFrame([ac.split('|') for ac in self.df.addressContent], 
                                columns = ['street','zipcode','zipcode','area'])
        
        self.df = pd.concat([self.df, df_addr], axis = 0)
        
        del self.df.addressContent
        del self.df.address
    
    

class WgAnalysis():
    df = None
    
    def __init__(self, df):
        self.df = df
        plt.style.use('ggplot')
    
    def size_price(self, path = None):
        plt.plot(self.df.room_size, self.df.price, 'o')
        
        plt.xlabel('Room size (m²)')
        plt.ylabel('Price (euro)')
        title = 'Relationship between room size and price'
        plt.title(title)
        if path:
            plt.savefig(path)
        else:
            plt.savefig('material/{}.jpg'.format(title))
        
        plt.show()





if __name__ == '__main__':
    
    pd.set_option('max_colwidth',200)
    pd.set_option('max_columns',None) 
    
    file_name = "final_result(1-5).csv"
    wp = WgPreprocess(pd.read_csv(file_name))
    df = wp.run()
    df.to_csv("preprocessed_"+file_name)
    
    
    
    
    
    
    