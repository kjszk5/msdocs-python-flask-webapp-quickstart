from flask import session
import pandas as pd
import random
def script_get(request_args):

    print("Script GET")
    print(request_args)
    print(request_args["page"])
    page = int(request_args["page"])
    if page == 0:
        df = pd.read_csv("script.csv")
        script_list = df.to_numpy().tolist()
        random.shuffle(script_list)
        print(script_list[0][0])
        en_script = script_list[0][0]
        jp_script = script_list[0][1]
        session["script_list"] = script_list
        session["page"] = page
    else:
        script_list = session["script_list"] 
        print("Script_GET")
        print(script_list)
        
        en_script = script_list[page][0]
        jp_script = script_list[page][1]
        session["page"] = page


    return en_script,jp_script,page

#script_get(request_args)
