from src.util.parser_rules import *
from src.util.tokenizer_utils import word_tokenize
from src.util.headers_dict import bucket2title, title2bucket, headers_dict_init

dict1 = {}
dict1["Resume_Parser"] = {"ResumeFileName" : '' , "FullName" : '' , "Email" : '' , "Phone" : '' , "Links" : '' , "Address" : '' , "Education_full" : '' , "Education" : [] , "SkillSet" : '' , "Experience" : '' ,"Projects" : [], "Hobbies" : '' , "Objective" : '' , "Extracurricular_Activities" : '' , "Personal Details" : ''} 

Education_dict = {"Name" : '' , "Degree" : ''}


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


        print(dict1)

        #print(" ---mobile : ", extract_mobile(self.personal_lines))
        #print(" ---email : ", extract_email(self.personal_lines))
        #print(" ---address : ", extract_address(self.personal_lines))

        #print(extract_insti(self.education_lines))


    def summary(self):
        print("Skiping Summary")
        return ""
