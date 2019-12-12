bucket2title = {}

titles = ['Experience','Skills','Projects','Qualifications','Education','Hobbies','Extra curricular','Personal Details']

for title in titles:
    bucket2title[title] = []

bucket2title['Personal Details'].append('Personal Details')
bucket2title['Personal Details'].append('Personal Information')
bucket2title['Personal Details'].append('Personal Info')
bucket2title['Personal Details'].append('Personal Interests')
bucket2title['Personal Details'].append('Personal Profile')
bucket2title['Personal Details'].append('Personal particulars')

bucket2title['Experience'].append('Experience')
bucket2title['Experience'].append('experience')
bucket2title['Experience'].append('work experience')
bucket2title['Experience'].append('working experience')
bucket2title['Experience'].append('expertise')
bucket2title['Experience'].append('professional experience')
bucket2title['Experience'].append('internships')

bucket2title['Skills'].append('Skills')
bucket2title['Skills'].append('skills')
bucket2title['Skills'].append('specialties')
bucket2title['Skills'].append('key skills')
bucket2title['Skills'].append('additional skills')
bucket2title['Skills'].append('Technical Skills')
bucket2title['Skills'].append('Management Skills')

bucket2title['Projects'].append('Projects')
bucket2title['Projects'].append('key projects')
bucket2title['Projects'].append('projects')
bucket2title['Projects'].append('projects done')
bucket2title['Projects'].append('projects completed')
bucket2title['Projects'].append('projects undertaken')
bucket2title['Projects'].append('academic projects')
bucket2title['Projects'].append('Major Projects')
bucket2title['Projects'].append('Other Projects')


bucket2title['Qualifications'].append('Qualifications')
bucket2title['Qualifications'].append('qualifications')
bucket2title['Qualifications'].append('core qualifications')
bucket2title['Qualifications'].append('technical qualifications')
bucket2title['Qualifications'].append('academic qualifications')
bucket2title['Qualifications'].append('educational qualifications')
bucket2title['Qualifications'].append('achievements')
bucket2title['Qualifications'].append('awards and honours')
bucket2title['Qualifications'].append('awards')
bucket2title['Qualifications'].append('certifications')

bucket2title['Education'].append('education')
bucket2title['Education'].append('educational details')
bucket2title['Education'].append('academics')

bucket2title['Hobbies'].append('hobbies')

bucket2title['Extra curricular'].append('extra_curriculars')
bucket2title['Extra curricular'].append('extra_curricular activities')


title2bucket = {}

def headers_dict_init():
    for k,v in bucket2title.items():
        for m in v:
            title2bucket[m] = k