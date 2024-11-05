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

def sortSchool(list):
    school = {}
    sum_gpa = 0
    for i in list:
        if i["School"] in school:
            continue
        else:
            sch_list = [z for z in list if z["School"] == i["School"]]
            gend_list, cgpa = sortGender(sch_list)
            sum_gpa += cgpa
            school[i["School"]] = gend_list
    return school, sum_gpa

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

def getGenderCount(list):
    male = 0
    female = 0
    for v in list.values():
        #check gender ratio
        for gend, v in v.items():
            if gend == "Male":
                male += len(v)
            else:
                female += len(v)
    return((male, female))

#Calculates the number of Male and Females for each group (Basic)
def getGendNum(groupsize=5,ratio):
    each_gend = 5//2
    high, low = max(ratio), min(ratio)
       
#when the difference is equal to the group size
    if high - low == group_size: 
        if high == ratio[0]:
            num_m = group_size
            num_f = 0
        else:
            num_m = 0
            num_f = group_size

#Difference less than or equal to 5
    elif high - low < 5:
        if ratio[0] > ratio[1]:
            num_m = each_gend + 1
            num_f = each_gend
        else:
            num_m = each_gend
            num_f = each_gend + 1
    
    return num_m,num_f

def getSchlCount(list):
    schls_count = {}
    for schl, val in list.items():
        gends_count = {}
        
        for gend, v in val.items():
            # print(schl, ":", gend, len(v[0]))
            gends_count[gend] = len(v)
             
        schls_count[schl] = gends_count
    # print(schls_count)
    return(schls_count)

def getSchlGend(list, gend):
    max_gend = []
    for sch, value in list.items():
        try:
            max_gend.append([sch, value[gend]])
        except:
            continue

    sorted_dict = sorted(max_gend, key=lambda x:x[1])

    return sorted_dict

def getStudentbyGpa(list, avg_gpa, group_gpa):
    student = 0
    for i in list:
        ref_gpa = avg_gpa
        if group_gpa == avg_gpa:
            student = list.pop(list.index(i))
            break
        elif group_gpa > avg_gpa:
            if group_gpa - avg_gpa > 0.2:
                ref_gpa -= 0.2
            if i["CGPA"] <= ref_gpa:
                student = list.pop(list.index(i))
                break
        else:
            if avg_gpa - group_gpa > 0.2:
                ref_gpa += 0.2
            if i["CGPA"] >= ref_gpa:
                student = list.pop(list.index(i))
                break

    if student == 0:
        group_gpa = avg_gpa
        student, list = getStudentbyGpa(list, avg_gpa, group_gpa)
        
    return student, list
def getGroups(list, num_m, num_f, avg_gpa):
    group_size = 5
    group = []
    
    group_gpa = 0.0

    while len(group) < group_size:
        student = 0
        i = 0

        if len(group) < num_m:
            gend = "Male"
            num = num_m
            opp_num = 0
        else:
            gend = "Female"
            num = num_f
            opp_num = num_m

        sch_count = getSchlCount(list)
        sorted_dict = getSchlGend(sch_count, gend)
        # print(sorted_dict)
        if sorted_dict == []:
            break

        while student == 0:
            if len(group) - opp_num < (num//2):
                schl = sorted_dict[i][0]
                num_of_students = sorted_dict[i][1]
            else:
                schl = sorted_dict[-i-1][0]
                num_of_students = sorted_dict[-i-1][1]

            if num_of_students == 1:
                student = list[schl][gend].pop()
                # print(student)
                del list[schl][gend]
            else:
                student, list[schl][gend] = getStudentbyGpa(list[schl][gend], avg_gpa, group_gpa)
            try:
                if list[schl][gend] == []:
                    del list[schl][gend]
            except:
                continue

            i += 1
        # print(schl)
        # print(student["CGPA"])
        group.append(student)
        group_gpa = round((((len(group)-1)*group_gpa)+student["CGPA"])/len(group), 2)
        # print(group_gpa, len(group))

    return group, list
def main(list, group_size = 5):
    all_groups = {}
    for tut, value in list.items():
        #check school distribution
        # print(tut, getGenderCount(value))
        ratio = getGenderCount(value[0])
        class_size = ratio[0] + ratio[1]
        num_of_grps = class_size // group_size
        num_of_extra = class_size % group_size
        
        tut_grps = []
        #counts number of groups, carries through extras and normal groups
        for i in range(num_of_grps):
            ratio = getGenderCount(value[0])

            if i < num_of_extra:
                extra = group_size + 1
                num_m, num_f = getGendNum(extra, ratio)
            else:
                num_m, num_f = getGendNum(group_size, ratio)

            if i == num_of_grps-1:
                group = []
                for schl, val in value[0].items():
                    for gend, v in val.items():
                        for stu in v:
                            group.append(stu)
            else:
                group, value[0] = getGroups(value[0], num_m, num_f, value[1])
                
            tut_grps.append([i+1, group])
        all_groups[tut] = tut_grps
    return all_groups

all_groups = main(sorted_list)

with open("result.csv", "w") as file:
    file.write(','.join(labels)+",Team Assigned"+"\n")
    for tut, value in all_groups.items():
        for i in value:
            group_num = i[0]
            for student in i[1]:
                file.write(f"""{student["Tutorial Group"]},{student["Student ID"]},{student["School"]},{student["Name"]},{student["Gender"]},{student["CGPA"]},{group_num}\n""")
