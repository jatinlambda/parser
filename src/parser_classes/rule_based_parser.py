from src.util.parser_rules import *
from src.util.other_util import preprocess_text
import json, os


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

    def parse(self, texts, print_line=False):
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


        insti_list = []
        for line in self.education_lines:
            insti = extract_insti(line["text"])
            for i in insti:
                insti_list.append(i)  # insti_list extracted
        self.parsedDict["Resume"]["Education"] = insti_list
        text = [x["text"] for x in self.texts]
        text = ' '.join(text)

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
        
    def summary(self):
        print("Skiping Summary")
        return ""

    def save_json(self):
        with open(os.path.basename(self.file_path)+".json", "w") as write_file:
            json.dump(self.parsedDict, write_file, indent=4)



