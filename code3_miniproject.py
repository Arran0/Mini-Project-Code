labels = ["Tutorial Group","Student ID","School","Name","Gender","CGPA"]

with open('./records.csv', mode ='r') as file:    
    full_list = [] 
    next(file) 
    for lines in file:
        line = {} 
        lines = lines.rstrip() 
        lines = lines.split(",") 
        for i in range(len(lines)):
            if labels[i] == "CGPA":
                line[labels[i]] = float(lines[i])
            else:
                line[labels[i]] = lines[i]
        full_list.append(line)

def sortTut(list):
    tutgrp = {}
    for i in list:
        sum_gpa = 0
        if i["Tutorial Group"] in tutgrp:
            continue
        else:
            tut_list = [z for z in list if z["Tutorial Group"] == i["Tutorial Group"]]
            schl_list, cgpa = sortSchool(tut_list)
            sum_gpa += cgpa
            tutgrp[i["Tutorial Group"]] = [schl_list, round(sum_gpa/len(tut_list),2)]
    return tutgrp
sorted_list = sortTut(full_list)

def sortGender(list): 
    gender = {}
    sum_gpa = 0
    for i in list:
        sum_gpa += i["CGPA"]
        if i["Gender"] in gender:
            continue
        else:
            gender[i["Gender"]] = [z for z in list if z["Gender"] == i["Gender"]]
    return gender, sum_gpa
