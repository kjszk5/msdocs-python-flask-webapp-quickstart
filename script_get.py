from flask import session
import pandas as pd
import random
def script_get(request_args):

    print("Script GET")
    print(request_args)
    print(request_args["question_no"])
    question_no = int(request_args["question_no"])
    if question_no == 0:
        df = pd.read_csv("script.csv")
        df['accuracy_score']=0
        df['fluency_score']=0
        df['completeness_score']=0
        df['pronunciation_score']=0

        script_list = df.to_numpy().tolist()
        random.shuffle(script_list)
        print(script_list[0][0])
        en_script = script_list[0][0]
        jp_script = script_list[0][1]
        session["script_list"] = script_list[:10]
        session["question_no"] = question_no
    else:
        script_list = session["script_list"] 
        print("Script_GET")
#        print(script_list)
        
        en_script = script_list[question_no][0]
        jp_script = script_list[question_no][1]
        session["question_no"] = question_no


    return en_script,jp_script,question_no

#script_get(request_args)
