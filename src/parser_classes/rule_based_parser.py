from src.util.parser_rules import *
from src.util.other_util import preprocess_text
import json, os
# from src.util.headers_dict import bucket2title, title2bucket

class ResumeParser(object):

    def __init__(self, file_path):
        self.name = None
        self.unknown = True
        self.file_path = os.path.basename(file_path)
        self.texts = []
        self.raw = None
        self.layouts = None
        self.parsedDict = {}
        self.parsedDict["Resume"] = {"ResumeFileName": '',
                                            "FullName": '',
                                            "Email": '',
                                            "Phone": '',
                                            "Links": '',
                                            "Address": '',
                                            "Personal Details": '',
                                            "Education Raw": '',
                                            "Education": [],
                                            "Skills Raw": '',
                                            "Skills": [],
                                            "Experience Raw": '',
                                            "Experience": [],
                                            "Projects Raw":'',
                                            "Projects": [],
                                            "Hobbies": [],
                                            "Hobbies Raw": '',
                                            "Objective": '',
                                            "Extracurricular Activities": '',
                                            "All Text":'',
                                            "Raw Parsed":[]}

    def parse(self, texts, print_line=True):
        for line, layout in zip(texts['text'], texts['layout']):
            self.texts.append(preprocess_text(line, layout))

        extract_headers(self.texts)
        extract_buckets(self.texts)

        if print_line:
            for line in self.texts:
                if line['isHeader']:
                    print(line['bucket'], '**', '\t', line['text'])
                else:
                    print(line['bucket'], '\t', line['text'])

        self.parsedDict["Resume"]["ResumeFileName"] = self.file_path

        self.education_lines = []
        self.personal_lines = []
        self.experience_lines = []
        self.skills_lines = []
        self.other_lines = []
        self.project_lines = []
        self.qualification_lines = []
        self.hobbies_lines = []
        self.extra_curricular_lines = []
        self.objective_lines = []

        for entry in self.texts:
            if entry['bucket'] == 'Personal Details':
                self.personal_lines.append(entry)
            elif entry['bucket'] == 'Experience':
                self.experience_lines.append(entry)
            elif entry['bucket'] == 'Skills':
                self.skills_lines.append(entry)
            elif entry['bucket'] == 'Projects':
                self.project_lines.append(entry)
            elif entry['bucket'] == 'Qualifications':
                self.qualification_lines.append(entry)
            elif entry['bucket'] == 'Education':
                self.education_lines.append(entry)
            elif entry['bucket'] == 'Hobbies':
                self.hobbies_lines.append(entry)
            elif entry['bucket'] == 'Extra curricular':
                self.extra_curricular_lines.append(entry)
            elif entry['bucket'] == 'Objective':
                self.objective_lines.append(entry)

        name = extract_name([], self.personal_lines)
        print(" ---name : ", name)
        self.parsedDict["Resume"]["FullName"] = name

        email = extract_email([], self.personal_lines)
        print(" ---email : ", email)
        self.parsedDict["Resume"]["Email"] = email

        phone = extract_mobile([], self.personal_lines)
        print(" ---mobile : ", phone)
        self.parsedDict["Resume"]["Phone"] = phone

        line = [x["text"] for x in self.education_lines]
        self.parsedDict["Resume"]["Education Raw"] = '\n'.join(line)

        line = [x["text"] for x in self.skills_lines]
        self.parsedDict["Resume"]["Skills Raw"] = '\n'.join(line)

        line = [x["text"] for x in self.experience_lines]
        self.parsedDict["Resume"]["Experience Raw"] = '\n'.join(line)

        line = [x["text"] for x in self.hobbies_lines]
        self.parsedDict["Resume"]["Hobbies Raw"] = '\n'.join(line)

        line = [x["text"] for x in self.objective_lines]
        self.parsedDict["Resume"]["Objective"] = '\n'.join(line)

        line = [x["text"] for x in self.project_lines]
        self.parsedDict["Resume"]["Projects Raw"] = '\n'.join(line)

        line = [x["text"] for x in self.personal_lines]
        self.parsedDict["Resume"]["Personal Details"] = '\n'.join(line)

        line = [x["text"] for x in self.extra_curricular_lines]
        self.parsedDict["Resume"]["Extracurricular Activities"] = '\n'.join(line)



        # degree = extract_degree(self.education_lines)     degrees extracted as a list. Currently not added in the dictionary

        insti_list = []
        for line in self.education_lines:
            # print(line)
            insti = extract_insti(line["text"])
            for i in insti:
                insti_list.append(i)  # insti_list extracted
                # print(degree)
        self.parsedDict["Resume"]["Education"] = insti_list
        text = [x["text"] for x in self.texts]
        text = ' '.join(text)

        # print(text)

        edu = extract_education([sent.string.strip() for sent in nlp(text).sents])
        self.parsedDict["Resume"]["Education"]=edu

        skills = extract_skills(nlp(
            self.parsedDict["Resume"]["Skills Raw"] +
            self.parsedDict["Resume"]["Experience Raw"] +
            '\n'.join(self.parsedDict["Resume"]["Projects"])))
        self.parsedDict["Resume"]["Skills"]=skills

        experience = extract_experience(text)
        self.parsedDict["Resume"]["Experience"]=experience

        self.parsedDict["Resume"]['All Text']='\n'.join([line['text'] for line in self.texts])
        self.parsedDict["Resume"]['Raw Parsed']=[dict([(key, val) for key, val in line.items() if key!='doc' and key!='tokens']) for line in self.texts]
        #
        #
        # # Skills extraction from skills and projects, then merging into one list and removing duplicates
        # # final_skill_list = extract_skills('\n'.join(self.skills_lines))
        # # final_skill_list2 = extract_skills('\n'.join(self.project_lines))
        # #  print(final_skill_list)
        # # print(final_skill_list2)
        # # res_list = final_skill_list + final_skill_list2
        # # flat_list = [item for sublist in res_list for item in sublist]
        # # print(flat_list)
        # # flat_list = list(dict.fromkeys(res_list))
        # # dict1["Resume"]["Skills"] = flat_list
        print(edu)
        print(skills)
        print(experience)
        print(insti_list)
        #
        # #date_list extracted but not added to dictionary
        # date_list = extract_date('\n'.join(self.education_lines))
        # #print(date_list)

        # print(extract_insti('\n'.join(education_lines)))
        # print(dict1)
        # for k,v in dict1["Resume"].items():
        #   print(k,":")
        #  print(v)

    def summary(self):
        print("Skiping Summary")
        return ""

    def save_json(self):
        print(os.path.basename(self.file_path))
        with open(os.path.basename(self.file_path)+".json", "w") as write_file:
            json.dump(self.parsedDict, write_file, indent=4)




# print(" ---mobile : ", extract_mobile(self.personal_lines))
# print(" ---email : ", extract_email(self.personal_lines))
# print(" ---address : ", extract_address(self.personal_lines))

# print(extract_insti(self.education_lines))



