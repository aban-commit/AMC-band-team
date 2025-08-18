# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 04:24:50 2025

@author: abane
"""

import streamlit as st
from PIL import Image
from pytesseract import pytesseract
from datetime import date
import pandas as pd


image_path = st.file_uploader("Upload the band screenshot")


# Defining paths to tesseract.exe 
# and the image we would be using 
path_to_tesseract = "/tesseract.exe"

current_day = date.today().day

## LIST 1
forward1 = ['naveen', 'sourish', 'sujoy sen', 'rajib', 'prithish',
'arindam hazra', 'avi g.', 'sujit', 'sabby g.', 'pankaj choudhury']

midfield1 = ['sourav', 'amit banerjee', 'suman biswas', 'sourav jana', 'pinaki mukherjee',
'anand goswami', 'dhiman', 'neel das', 'pranab', 'sumanta']

defence1 = ['ram dutta', 'sujeet tiwari', 'sudeep ganguly', 'shaheen', 'mukherjee joydeep',
'premjit pan', 'ayan', 'amritesh chatterjee', 'kallol roy', 'ismail sardar', 'samrat chattapadhyay',
'sourav das', 'subhrodip', 'kunal', 'soumya', 'pramit g', 'rupam roy', 'mahadev roy', 
'abhishek kahali']

goalie1 = ['swadhin ghosh', 'puspendu sarkar', 'subrata', 'amar']

player_list1 = forward1 + midfield1 + defence1 + goalie1

## LIST 2
forward2 = ['naveen', 'sourish', 'sujoy sen', 'rajib', 'prithish', 'arindam hazra', 'avi g.',
'sujit', 'sabby g.', 'pankaj choudhury']

midfield2 = ['sourav', 'suman biswas', 'amit banerjee', 'sourav jana', 'pinaki mukherjee',
'anand goswami', 'neel das', 'pranab', 'sumanta']

defence2 = ['dhiman', 'ram dutta', 'sujeet tiwari', 'sudeep ganguly', 'shaheen', 'mukherjee joydeep',
'premjit pan', 'amritesh chatterjee', 'ayan', 'kallol roy', 'ismail sardar', 'samrat chattapadhyay',
'subhrodip', 'kunal', 'soumya', 'pramit g', 'rupam roy', 'abhishek kahali', 'mahadev roy']

goalie2 = ['swadhin ghosh', 'puspendu sarkar', 'subrata', 'amar']

player_list2 = midfield2 + defence2 + goalie2 + forward2

## LIST 3
forward3 = ['naveen', 'sourish', 'prithish', 'sujoy sen', 'rajib', 'arindam hazra', 'avi g.',
'sujit', 'sabby g.', 'pankaj choudhury',]

midfield3 = ['amit banerjee', 'sourav', 'suman biswas', 'sourav jana', 'dhiman', 'pinaki mukherjee',
'neel das', 'pranab', 'ram dutta', 'sujeet tiwari', 'anand goswami', 'sudeep ganguly', 'shaheen',
'sumanta']

defence3 = ['mukherjee joydeep', 'premjit pan', 'ayan', 'dhiman', 'amritesh chatterjee',
'kallol roy', 'samrat chattapadhyay', 'ismail sardar', 'kunal', 'soumya', 'pramit g',
'rupam roy', 'mahadev roy', 'abhishek kahali']

goalie3 = ['swadhin ghosh', 'puspendu sarkar', 'subrata', 'amar']

player_list3 = defence3 + goalie3 + forward3 + midfield3

name_tokens = ' '.join(player_list1)
name_tokens = name_tokens.split(' ')
name_tokens_comma = [token + ',' for token in name_tokens]
#print("Tokens: ", name_tokens_comma)

# Function to get the join list and make teams
def make_team(join_list):
    print(join_list)
    
    join_list_lower = [x.lower() for x in join_list]
    diff_list = list(set(join_list_lower) - set(player_list))
    print(diff_list)
    
    team_list = [x for x in player_list if x in join_list_lower]
    print(team_list)
    
    if current_day % 2:
        team_blue = team_list[::2]
        team_yellow = team_list[1::2]
    else:
        team_blue = team_list[1::2]
        team_yellow = team_list[::2]
    
    print("Team Blue ",team_blue)
    print("Team Yellow ",team_yellow)
    return(team_blue, team_yellow)

# Function to write out excel file with the teams
def write_teams_file(team_B, team_Y):
    if len(team_B) > len(team_Y):
        team_Y.append(' ')
    elif len(team_Y) > len(team_B):
        team_B.append(' ')
        
    team_dict={'Team Blue' : team_B, 'Team Yellow' : team_Y}
    team_df = pd.DataFrame(team_dict)
    
    # Create a styled data frame
    team_df_styled = team_df.style
    team_df_styled = team_df_styled.set_properties(subset='Team Blue', **{'background-color': 'LightBlue'})
    team_df_styled = team_df_styled.set_properties(subset='Team Yellow', **{'background-color': 'yellow'})

    return(team_df_styled)


if image_path is not None:
    # Opening the image & storing it in an image object 
    img = Image.open(image_path)

    # Providing the tesseract executable 
    # location to pytesseract library 
    pytesseract.tesseract_cmd = path_to_tesseract

    # Passing the image object to image_to_string() function 
    # This function will extract the text from the image 
    text = pytesseract.image_to_string(img)

    # Displaying the extracted text 
    # print(text[:-1])

    full_list = text.split()
    print(full_list)


    try:
        s_ind = full_list.index("Join")
    except ValueError:
        try:
            s_ind = full_list.index("doin")
        except ValueError:
            s_ind = full_list.index("soin")
    
    e_ind = full_list.index("Decline")

    index1 = [(s_ind+i) for i in range(6) if full_list[s_ind + i].lower() in name_tokens]
    index2 = [(s_ind+i) for i in range(6) if full_list[s_ind + i].lower() in name_tokens_comma]
    try:
        beg_ind = min(index1[0], index2[0])
    except IndexError:
        try:
            beg_ind = index1[0]
        except IndexError:
            beg_ind = index2[0]
        
    print("begin index ",beg_ind)

    index3 = [(e_ind-i) for i in range(6) if full_list[e_ind - i].lower() in name_tokens]
    index4 = [(e_ind-i) for i in range(6) if full_list[e_ind - i].lower() in name_tokens_comma]
    try:
        end_ind = max(index3[0], index4[0])
    except IndexError:
        try:
            end_ind = index3[0]
        except IndexError:
            end_ind = index4[0]

    print("end index ",end_ind)
    #print(index3, index4)

    new_list = full_list[beg_ind:end_ind + 1]
    #print(new_list)

    new_string = ' '.join(new_list)
    #print(new_string)

    joins = new_string.split(', ')

    if current_day % 4 == 0:
        player_list = player_list1
    elif current_day % 2 == 0:
        player_list = player_list2
    else:
        player_list = player_list3

    team_B, team_Y = make_team(joins)

    final_df = write_teams_file(team_B, team_Y)
    
    df1 = st.dataframe(final_df, height=1500, hide_index=True)
    #df1 = st.data_editor(final_df, height=1500, hide_index=True,num_rows="dynamic",column_config={"Team Blue": st.column_config.Column(disabled=True)})
    
             
            
        

    
    
