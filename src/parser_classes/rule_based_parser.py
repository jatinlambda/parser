from src.util.parser_rules import *
from src.util.other_util import preprocess_text
from src.util.headers_dict import bucket2title, title2bucket

parsedDict = {}
parsedDict["Resume_Parser"] = {"ResumeFileName": '', "FullName": '', "Email": '', "Phone": '', "Links": '', "Address": '',
                          "Education_full": '', "Education": [], "SkillSet": '', "Skills": [], "Experience": '',
                          "Projects": [], "Hobbies": '', "Objective": '', "Extracurricular_Activities": '',
                          "Personal Details": ''}


class ResumeParser(object):
    def __init__(self, file_path):
        self.name = None
        self.unknown = True
        self.file = file_path
        self.texts = []
        self.raw = None
        self.layouts = None

    def parse(self, texts, print_line=False):
        for line, layout in zip(texts['text'], texts['layout']):
            self.texts.append(preprocess_text(line, layout))
            # print(self.texts[-1]['text'])

        extract_headers(self.texts)
        extract_buckets(self.texts)

        parsedDict["Resume_Parser"]["ResumeFileName"] = self.file

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
        parsedDict["Resume_Parser"]["FullName"] = name;

        email = extract_email([], self.personal_lines)
        print(" ---email : ", email)
        parsedDict["Resume_Parser"]["Email"] = email

        phone = extract_mobile([], self.personal_lines)
        print(" ---mobile : ", phone)
        parsedDict["Resume_Parser"]["phone"] = phone

        line = [x["text"] for x in self.education_lines]
        parsedDict["Resume_Parser"]["Education_full"] = '\n'.join(line)

        line = [x["text"] for x in self.skills_lines]
        parsedDict["Resume_Parser"]["SkillSet"] = '\n'.join(line)

        line = [x["text"] for x in self.experience_lines]
        parsedDict["Resume_Parser"]["Experience"] = '\n'.join(line)

        line = [x["text"] for x in self.hobbies_lines]
        parsedDict["Resume_Parser"]["Hobbies"] = '\n'.join(line)

        line = [x["text"] for x in self.objective_lines]
        parsedDict["Resume_Parser"]["Objective"] = '\n'.join(line)

        line = [x["text"] for x in self.project_lines]
        parsedDict["Resume_Parser"]["Projects"] = line

        line = [x["text"] for x in self.personal_lines]
        parsedDict["Resume_Parser"]["Personal Details"] = '\n'.join(line)

        line = [x["text"] for x in self.extra_curricular_lines]
        parsedDict["Resume_Parser"]["Extracurricular_Activities"] = '\n'.join(line)

        # degree = extract_degree(self.education_lines)     #degrees extracted as a list. Currently not added in the dictionary

        insti_list = []
        for line in self.education_lines:
            # print(line)
            insti = extract_insti(line["text"])
            for i in insti:
                insti_list.append(i)  # insti_list extracted
                # print(degree)
        # print(self.education_lines)
        # print(self.skills_lines)
        parsedDict["Resume_Parser"]["Education"] = insti_list
        text = [x["text"] for x in self.texts]
        text = ' '.join(text)

        # print(text)

        edu = extract_education([sent.string.strip() for sent in nlp(text).sents])
        skills = extract_skills(nlp(
            parsedDict["Resume_Parser"]["SkillSet"] + parsedDict["Resume_Parser"]["Experience"] + '\n'.join(
                parsedDict["Resume_Parser"]["Projects"])), nlp(parsedDict["Resume_Parser"]["SkillSet"]).noun_chunks)
        experience = extract_experience(text)
        # Skills extraction from skills and projects, then merging into one list and removing duplicates
        # final_skill_list = extract_skills('\n'.join(self.skills_lines))
        # final_skill_list2 = extract_skills('\n'.join(self.project_lines))
        #  print(final_skill_list)
        # print(final_skill_list2)
        # res_list = final_skill_list + final_skill_list2
        # flat_list = [item for sublist in res_list for item in sublist]
        # print(flat_list)
        # flat_list = list(dict.fromkeys(res_list))
        # dict1["Resume_Parser"]["Skills"] = flat_list
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
        # for k,v in dict1["Resume_Parser"].items():
        #   print(k,":")
        #  print(v)

    def summary(self):
        print("Skiping Summary")
        return ""



# print(" ---mobile : ", extract_mobile(self.personal_lines))
# print(" ---email : ", extract_email(self.personal_lines))
# print(" ---address : ", extract_address(self.personal_lines))

# print(extract_insti(self.education_lines))



