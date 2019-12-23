import spacy
import pickle
import spacy
from spacy import displacy



with open ('outfile', 'rb') as fp:
    # itemlist = pickle.load(fp)
    # # print(itemlist)
    # for word in itemlist:
    #     print(word)
    # line=" ".join(itemlist)
    # print(line)

    nlp = spacy.load('en_core_web_md')
    # doc = nlp(line)
    # displacy.serve(doc, style="ent")

    #
    # def remove_stopwords_fast(text):
    #     doc = nlp(text.lower())
    #     result = [token.text for token in doc if token.text not in nlp.Defaults.stop_words]
    #     return " ".join(result)
    #
    # # print(remove_stopwords_fast(line))
    #
    # def process_text(text):
    #     doc = nlp(text.lower())
    #     result = []
    #     for token in doc:
    #         if token.text in nlp.Defaults.stop_words:
    #             continue
    #         if token.is_punct:
    #             continue
    #         if token.lemma_ == '-PRON-':
    #             continue
    #         result.append(token.lemma_)
    #     return " ".join(result)


    def process_main_text2(text):
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
        return result


    def process_main_text1(text):
        doc = nlp(text.lower())
        result = []
        for token in doc:
            if token.is_punct:
                continue
            if token.lemma_ == '-PRON-':
                continue
            result.append(token.lemma_)
        return result

    def process_main_text0(text):
        doc = nlp(text.lower())
        result = []
        for token in doc:
            if token.is_punct:
                continue
            result.append(token.lemma_)
        return result


    def calculate_similarity_with_processing(title, line):
        # print(title, line)
        process_main_tex_foo = process_main_text0
        title = nlp(' '.join(process_main_tex_foo(title)))
        line = nlp(' '.join(process_main_tex_foo(line)))
        for token in line:
            token_id = nlp.vocab.strings[token.text]
            if token_id not in nlp.vocab:
                return 0
        return title.similarity(line)







    # doc=nlp(remove_stopwords_fast(line))

    # doc = nlp(process_text(line))

    # print(doc)


    # for sent in doc.sents:
    #     print(sent.text)
    

    # print(calculate_similarity_with_processing("Technical University", "Rajasthan Technical University,Kota, Rajasthan"))
    # print(calculate_similarity_with_processing("university", "3 years Diploma in Computer Science (Agg. 70.8)"))
    # print(calculate_similarity_with_processing("university", "Bachelor of Technology, Computer Science and Technology"))

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
