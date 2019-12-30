from src.util.nlp_tools import nlp_process_text_foo

bucket2title = {}

# possible titles of headers or possible buckets
titles = ['Experience','Skills','Projects','Qualifications','Education','Hobbies','Extra curricular','Personal Details','Objective']

for title in titles:
    bucket2title[title] = []

bucket2title['Personal Details'].append('Personal Details')
bucket2title['Personal Details'].append('Personal Information')
bucket2title['Personal Details'].append('Personal Info')
bucket2title['Personal Details'].append('Personal Interests')
bucket2title['Personal Details'].append('Personal Profile')
bucket2title['Personal Details'].append('Personal particulars')


bucket2title['Experience'].append('Experience')
bucket2title['Experience'].append('work experience')
# bucket2title['Experience'].append('working experience')
bucket2title['Experience'].append('expertise')
bucket2title['Experience'].append('professional experience')
bucket2title['Experience'].append('internships')
bucket2title['Experience'].append('courses')
bucket2title['Experience'].append('employment details')
bucket2title['Experience'].append('employment history')

# bucket2title['Skills'].append('Skills')
bucket2title['Skills'].append('skills')
bucket2title['Skills'].append('specialties')
bucket2title['Skills'].append('key skills')
bucket2title['Skills'].append('additional skills')
bucket2title['Skills'].append('Technical Skills')
bucket2title['Skills'].append('Management Skills')

bucket2title['Projects'].append('Projects')
bucket2title['Projects'].append('key projects')
bucket2title['Projects'].append('projects completed')
bucket2title['Projects'].append('projects undertaken')
bucket2title['Projects'].append('academic projects')
bucket2title['Projects'].append('Major Projects')
bucket2title['Projects'].append('Other Projects')
bucket2title['Projects'].append('technical activites')


bucket2title['Qualifications'].append('qualifications')
bucket2title['Qualifications'].append('core qualifications')
bucket2title['Qualifications'].append('technical qualifications')
bucket2title['Qualifications'].append('academic qualifications')
bucket2title['Qualifications'].append('educational qualifications')
bucket2title['Qualifications'].append('achievements')
bucket2title['Qualifications'].append('awards and honours')
bucket2title['Qualifications'].append('awards')
bucket2title['Qualifications'].append('certifications')
bucket2title['Qualifications'].append('certificates')
bucket2title['Qualifications'].append('academic credentials')
bucket2title['Qualifications'].append('accomplishment')

bucket2title['Education'].append('education')
bucket2title['Education'].append('educational details')
bucket2title['Education'].append('academics')

bucket2title['Hobbies'].append('hobbies')
bucket2title['Hobbies'].append('interests')

bucket2title['Extra curricular'].append('extra-curriculars')
bucket2title['Extra curricular'].append('extra-curricular activities')
bucket2title['Extra curricular'].append('co-curricular activities')
bucket2title['Extra curricular'].append('extra curriculars')
bucket2title['Extra curricular'].append('extra curricular activities')
bucket2title['Extra curricular'].append('co curricular activities')

bucket2title['Objective'].append('responsibilities')
bucket2title['Objective'].append('objective')
bucket2title['Objective'].append('career objective')
bucket2title['Objective'].append('aim')
bucket2title['Objective'].append('main objectives')
bucket2title['Objective'].append('roles')

for bucket in bucket2title:
    for i in range(len(bucket2title[bucket])):
        tokens, doc=nlp_process_text_foo(bucket2title[bucket][i])
        bucket2title[bucket][i]={'title':bucket2title[bucket][i], 'doc':doc, 'tokens':tokens, 'bucket':bucket}

title2bucket = {}

# def headers_dict_init():
for k,v in bucket2title.items():
    for m in v:
        title2bucket[m['title']] = m

