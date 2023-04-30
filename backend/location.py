REGIONS = [["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont", "New Jersey", "New York", "Pennsylvania"], # 0 items
                   ["Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin", "Iowa", "Kansas", "Minesota", "Missouri",
                       "Nebraska", "North Dakota", "South Dakota"], # 2675 items
                   ["Delaware", "Florida", "Georgia", "Maryland", "North Carolina",
                       "South Carolina", "Virginia", "District of Columbia", "West Virginia"], # 0 items
                   ["Alabama", "Kentucky", "Mississippi", "Tennessee", "Arkansas", "Louisiana", "Oklahoma", "Texas"], # 1627 items
                   ["Arizona", "Colorado", "Idaho", "Montana",
                       "Nevada", "New Mexico", "Utah", "Wyoming", "Alaska", "California", "Hawaii", "Oregon", "Washington"], # 374 items
                   ["American Samoa", "Guam", "Northern Mariana Islands", "Puerto Rico", "United States Minor Outlying Islands", "U.S. Virgin Islands"]] # 0 items

STATES = [state for region in REGIONS for state in region]

def get_all_states(): 
    return STATES

def get_neighboring_states(state): 
    for region in REGIONS: 
        if state in region: 
            return [st for st in region if st != state]
    return [] 