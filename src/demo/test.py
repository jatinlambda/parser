import spacy
import pickle
from spacy import displacy

with open ('outfile', 'rb') as fp:
    itemlist = pickle.load(fp)
    # print(itemlist)
    for word in itemlist:
        print(word)
    line=" ".join(itemlist)
    # print(line)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(line)


    def remove_stopwords_fast(text):
        doc = nlp(text.lower())
        result = [token.text for token in doc if token.text not in nlp.Defaults.stop_words]
        return " ".join(result)

    # print(remove_stopwords_fast(line))

    def process_text(text):
        doc = nlp(text.lower())
        result = []
        for token in doc:
            if token.text in nlp.Defaults.stop_words:
                continue
            if token.is_punct:
                continue
            if token.lemma_ == '-PRON-':
                continue
            result.append(token.lemma_)
        return " ".join(result)


    def calculate_similarity(text1, text2):
        base = nlp(process_text(text1))
        compare = nlp(process_text(text2))
        return base.similarity(compare)



    # doc=nlp(remove_stopwords_fast(line))

    # doc = nlp(process_text(line))

    # print(doc)


    # for sent in doc.sents:
    #     print(sent.text)

    print(calculate_similarity("experience", "work experience"))
    print(calculate_similarity("key project", "main project"))
    print(calculate_similarity("projects", "project"))


    # def get_verbs


    # print(calculate_similarity("work experience", "done project on machine learning"))
    # print(calculate_similarity("experience", "Represented company to key clientele and prospective customers in a positive manner, playing an instrumental role in facilitating business development"))
    # print(calculate_similarity("education", "Represented company to key clientele and prospective customers in a positive manner, playing an instrumental role in facilitating business development"))
    # print(calculate_similarity("skill", "Represented company to key clientele and prospective customers in a positive manner, playing an instrumental role in facilitating business development"))
    #
    # print(calculate_similarity("experience", "Passed Intermediate from UP Board in year 2009."))
    # print(calculate_similarity("education", "Passed Intermediate from UP Board in year 2009."))
    # print(calculate_similarity("skill", "Passed Intermediate from UP Board in year 2009."))

    # print("-------------")
    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)
    #     print()

    # displacy.serve(doc, style="ent")
    # displacy.serve(doc, style="dep")

    # for item in itemlist:
    #     doc = nlp(item)
    #     print("------------------")
    #     for ent in doc.ents:
    #         print(ent.text, ent.label_)
    #         print()
