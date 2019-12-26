from src.util.parser_rules import *
# from src.util.tokenizer_utils import word_tokenize
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
        self.raw = texts['text']
        self.layout = texts['layout']
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

        dict1["Resume_Parser"]["Personal Details"] = '\n'.join(self.personal_lines)

        dict1["Resume_Parser"]["Extracurricular_Activities"] = '\n'.join(self.extra_curricular_lines) 

        # degree = extract_degree(self.education_lines)     #degrees extracted as a list. Currently not added in the dictionary

        # insti_list = []
        # for line in self.education_lines:
        #     print(line)
        #     insti = extract_insti(line)
        #     for i in insti:
        #         insti_list.append(i)                      #insti_list extracted
        #print(degree)
        #print(self.education_lines)
        #print(self.skills_lines)
        # dict1["Resume_Parser"]["Education"] = insti_list
        text = ' '.join(('\n'.join(self.raw)).split())
        print(text)

        # edu = extract_education([sent.string.strip() for sent in nlp(text).sents])
        # skills = extract_skills(nlp('\n'.join(self.skills_lines + self.project_lines + self.experience_lines)),nlp('\n'.join(self.skills_lines)).noun_chunks)
        # experience = extract_experience(text)
        #Skills extraction from skills and projects, then merging into one list and removing duplicates
        #final_skill_list = extract_skills('\n'.join(self.skills_lines))
        #final_skill_list2 = extract_skills('\n'.join(self.project_lines))
      #  print(final_skill_list)
       # print(final_skill_list2)
        #res_list = final_skill_list + final_skill_list2
        #flat_list = [item for sublist in res_list for item in sublist]
        #print(flat_list)
        #flat_list = list(dict.fromkeys(res_list))
        #dict1["Resume_Parser"]["Skills"] = flat_list 
        # print(edu)
        # print(skills)
        # print(experience)
        # print(insti_list)
        #
        # #date_list extracted but not added to dictionary
        # date_list = extract_date('\n'.join(self.education_lines))
        # #print(date_list)

        #print(extract_insti('\n'.join(education_lines)))
        #print(dict1)
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


    
