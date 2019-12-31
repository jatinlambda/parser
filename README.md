Resume parser in Python : Parses pdf and docx resumes and classifies lines of the resume into various fields.

To run : $ python3 parser/src/demo/rule_based_parser.py 

Python Environment Required to run:
absl-py==0.8.1
apturl==0.5.2
asgiref==3.2.3
asn1crypto==0.24.0
astor==0.8.0
attrs==19.3.0
backcall==0.1.0
blis==0.4.1
Brlapi==0.6.6
cachetools==3.1.1
catalogue==0.0.8
certifi==2019.11.28
chardet==3.0.4
Click==7.0
command-not-found==0.3
configobj==5.0.6
configparser==4.0.2
cryptography==2.1.4
cupshelpers==1.0
cycler==0.10.0
cymem==2.0.3
decorator==4.4.1
defer==1.0.6
distro==1.4.0
distro-info===0.18ubuntu0.18.04.1
Django==3.0.1
django-crispy-forms==1.8.1
docx==0.2.4
docx2txt==0.8
en-core-web-md==2.2.5
en-core-web-sm==2.2.5
etelemetry==0.1.2
filelock==3.0.12
fitz==0.0.1.dev2
funcsigs==1.0.2
future==0.18.2
gast==0.3.2
google-auth==1.7.1
google-auth-oauthlib==0.4.1
google-pasta==0.1.8
grpcio==1.25.0
h5py==2.10.0
httplib2==0.14.0
idna==2.8
importlib-metadata==1.3.0
isodate==0.6.0
joblib==0.14.0
jsonschema==3.2.0
Keras==2.3.1
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
keyring==10.6.0
keyrings.alt==3.0
kiwisolver==1.1.0
language-selector==0.1
launchpadlib==1.10.6
lazr.restfulclient==0.13.5
lazr.uri==1.0.3
louis==3.5.0
lxml==4.4.2
macaroonbakery==1.1.3
Mako==1.0.7
Markdown==3.1.1
MarkupSafe==1.0
matplotlib==3.1.2
mcpi==1.1.0
minecart==0.3.0
more-itertools==8.0.2
murmurhash==1.0.2
netifaces==0.10.4
networkx==2.4
neurdflib==5.0.1
nibabel==2.5.1
nipype==1.3.1
nltk==3.4.5
numpy==1.18.0
oauth==1.0.1
oauthlib==3.1.0
olefile==0.45.1
packaging==19.2
pandas==0.25.3
ParallelDots==3.2.13
pdfminer==20191125
pdfminer.six==20191110
pdfminer3k==1.3.1
pexpect==4.2.1
Pillow==6.2.1
plac==1.1.3
pluggy==0.13.1
ply==3.11
preshed==3.0.2
protobuf==3.11.1
prov==1.5.3
py==1.8.0
pyasn1==0.4.8
pyasn1-modules==0.2.7
pycairo==1.16.2
pycrypto==2.6.1
pycryptodome==3.9.4
pycups==1.9.73
pydot==1.4.1
pydotplus==2.0.2
Pygments==2.5.2
pygobject==3.26.1
pymacaroons==0.13.0
PyNaCl==1.1.2
pyparsing==2.4.5
PyPDF2==1.26.0
pyresparser==1.0.6
pyRFC3339==1.0
pyrsistent==0.15.6
pytest==5.3.2
python-apt==1.6.4
python-dateutil==2.8.1
python-debian==0.1.32
python-docx==0.8.10
pytz==2019.3
pyxdg==0.25
pyxnat==1.2.1.0.post3
PyYAML==5.2
rdflib==4.2.2
reportlab==3.4.0
requests==2.22.0
requests-oauthlib==1.3.0
requests-unixsocket==0.1.5
rsa==4.0
scikit-learn==0.22
scipy==1.3.3
SecretStorage==2.3.1
simplejson==3.17.0
six==1.13.0
sklearn==0.0
sortedcontainers==2.1.0
spacy==2.2.3
sqlparse==0.3.0
srsly==0.2.0
system-service==0.3
systemd-python==234
tabula-py==1.4.3
tb-nightly==1.14.0a20190301
tensorboard==2.0.2
tensorflow==2.0.0a0
tensorflow-estimator==2.0.1
termcolor==1.1.0
tf-estimator-nightly==1.14.0.dev2019030115
thinc==7.3.1
tqdm==4.41.0
traits==5.2.0
ubuntu-drivers-common==0.0.0
ufw==0.36
unattended-upgrades==0.1
urllib3==1.25.7
usb-creator==0.3.3
wadllib==1.3.2
wasabi==0.4.2
wcwidth==0.1.7
Werkzeug==0.16.0
wrapt==1.11.2
xkit==0.0.0
xlrd==1.2.0
zipp==0.6.0
zope.interface==4.3.2





parser/src/util/AllCompanies.txt :  Contains names of all companies in india ( Manually add) (while adding try putting small length keywords of the company as bigger words often give poor similarity)
parser/src/util/indianNames.txt : Contains all indian names 
parser/src/util/allColleges : Contains all keywords related to college names (which must be there in a college name)
parser/src/util/skills.csv : Contains many skill keywords
parser/src/util/allDegrees : contains all education degrees offered in india (not being used anywhere in the code though)

parser/dataset contains resumes. Currently using content of parser/dataset/samplecv for parsing and writing into a json file which can be found in demo folder after running the script given above.

parser/src/util/parser_rules.py is the main file which has all extraction functions and which use helper functions which are present in other files in the same folder.

parser/src/demo/rule_based_parser.py is the file to be run which creates a resume object by calling resume class in parser/src/parser_classes/rule_based_parser.py and calls parse member function of the resume class which further calls all extract functions from parser_rules.py. 










