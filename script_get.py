from flask import session
import pandas as pd
import random
def script_get():

    print("Script GET")
#    print(request_args)
#    print(request_args["question_no"])
    question_no = 0
    question_num = int(session["question_num"])
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
    session["script_list"] = script_list[:question_num]
    session["question_no"] = question_no
    print("EnScript,JPScript")
    print(en_script,jp_script)
    print("Script GET END")

    return en_script,jp_script,question_no

#script_get(request_args)
