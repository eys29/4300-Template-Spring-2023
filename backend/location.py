REGIONS = [["Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin", "Iowa", "Kansas", "Minesota",   "Missouri", "Nebraska", "North Dakota", "South Dakota"], # 2675 items
            ["Alabama", "Kentucky", "Mississippi", "Tennessee", "Arkansas", "Louisiana", "Oklahoma", "Texas"], # 1627 items
            ["Arizona", "Colorado", "Idaho", "Montana",
                "Nevada", "New Mexico", "Utah", "Wyoming", "Alaska", "California", "Hawaii", "Oregon", "Washington"]] # 374 items

STATES = [state for region in REGIONS for state in region]

def get_all_states(): 
    return STATES

def get_neighboring_states(state): 
    for region in REGIONS: 
        if state in region: 
            return [st for st in region if st != state]
    return [] 