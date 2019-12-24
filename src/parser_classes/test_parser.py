from src.util.parser_rules import *
from src.util.tokenizer_utils import word_tokenize
from src.util.headers_dict import bucket2title, title2bucket, headers_dict_init

dict1 = {}
dict1["Resume_Parser"] = {"ResumeFileName" : '' , "FullName" : '' , "Email" : '' , "Phone" : '' , "Links" : '' , "Address" : '' , "Education_full" : '' , "Education" : [] , "SkillSet" : '' , "Skills" : [] , "Experience" : '' ,"Projects" : [], "Hobbies" : '' , "Objective" : '' , "Extracurricular_Activities" : '' , "Personal Details" : ''} 




class ResumeParser(object):

    def __init__(self,file_path):
        self.name = None
        self.unknown = True
        self.file = file_path

    def parse(self, texts, print_line=False):
        headers_dict_init()
        self.raw = texts
        headers = extract_headers(self.raw)
        buckets = extract_buckets(self.raw, headers)

        dict1["Resume_Parser"]["ResumeFileName"] = self.file

        self.education_lines=[]
        self.personal_lines=[]
        self.experience_lines=[]
        self.skills_lines=[]
        self.other_lines=[]
        self.project_lines=[]
        self.qualification_lines=[]
        self.hobbies_lines=[]
        self.extra_curricular_lines=[]
        self.objective_lines=[]

        for entry in buckets:
            if entry['label']=='Personal Details':
                self.personal_lines.append(entry['line'])
            elif entry['label']=='Experience':
                self.experience_lines.append(entry['line'])
            elif entry['label']=='Skills':
                self.skills_lines.append(entry['line'])
            elif entry['label']=='Projects':
                self.project_lines.append(entry['line'])
            elif entry['label']=='Qualifications':
                self.qualification_lines.append(entry['line'])
            elif entry['label']=='Education':
                self.education_lines.append(entry['line'])
            elif entry['label']=='Hobbies':
                self.hobbies_lines.append(entry['line'])
            elif entry['label']=='Extra curricular':
                self.extra_curricular_lines.append(entry['line'])
            elif entry['label']=='Objective':
                self.objective_lines.append(entry['line'])

        name = extract_name([],'\n'.join(self.personal_lines))        
        print(" ---name : ", name)
        dict1["Resume_Parser"]["FullName"] = name;

        email = extract_email([],'\n'.join(self.personal_lines))
        print(" ---email : ", email)
        dict1["Resume_Parser"]["Email"] = email

        phone = extract_mobile([],'\n'.join(self.personal_lines))
        print(" ---mobile : ", phone)
        dict1["Resume_Parser"]["phone"] = phone

        dict1["Resume_Parser"]["Education_full"] = '\n'.join(self.education_lines)


        dict1["Resume_Parser"]["SkillSet"] = '\n'.join(self.skills_lines)

        dict1["Resume_Parser"]["Experience"] = '\n'.join(self.experience_lines)

        dict1["Resume_Parser"]["Hobbies"] = '\n'.join(self.hobbies_lines)

        dict1["Resume_Parser"]["Objective"] = '\n'.join(self.objective_lines)

        dict1["Resume_Parser"]["Projects"] = self.project_lines

        degree = extract_degree(self.education_lines)
        #print(degree)
        #print(self.education_lines)
        #print(self.skills_lines)
        final_skill_list = extract_skills('\n'.join(self.skills_lines))
        final_skill_list2 = extract_skills('\n'.join(self.project_lines))
        res_list = [sum(i) for i in zip(final_skill_list, final_skill_list2)] 
        dict1["Resume_Parser"]["Skills"] = res_list 
        print(dict1)
        #for k,v in dict1["Resume_Parser"].items():
         #   print(k,":")
          #  print(v)


    def summary(self):
        print("Skiping Summary")
        return ""
            
"""
        insti_list = extract_insti(self.education_lines)
        print(insti_list)

        for insti in insti_list:
            Education_dict = {"Name" : '' , "Degree" : ''}
            Education_dict["Name"] = insti
            dict1["Resume_Parser"]["Education"].append(Education_dict)
"""


        #print(" ---mobile : ", extract_mobile(self.personal_lines))
        #print(" ---email : ", extract_email(self.personal_lines))
        #print(" ---address : ", extract_address(self.personal_lines))

        #print(extract_insti(self.education_lines))


    
