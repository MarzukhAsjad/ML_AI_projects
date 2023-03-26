# version 1.0
import spacy
nlp = spacy.load('en_core_web_sm') # Load the English language model


def IsAbbreviation(token: str):
    count_caps = 0
    for char in token:
        if char.isupper():
            count_caps += 1
    
    if count_caps > 1:
        if count_caps == len(token):
            return True
        else:
            return False
    return True # not true per case but to evade the error

# void function prints error if there is any grammatical error in sentence, else prints "No errors"
def IsPoorSentence(sentence: str):
    errors = 0
    text = nlp(sentence) # tokenize the strings using Spacy

    # Capital letter error    
    if (not sentence[0].istitle()):
        print("Sentence does not start with a capitial letter.")
        errors += 1
        
    # End sentence error
    if (sentence[-1] not in ['!', '?', '.']):
        print("Sentence does not end with a terminal punctuation mark (?/!/.)")
        errors += 1
    # Iterate over each token in the sentence
    for token in text:
        # Check for grammatical errors in the subject-verb agreement
        # personal & possessive pronouns, singular and plurarl nouns
        if token.dep_ == 'nsubj' and token.tag_ not in ['PRP', 'PRP$', 'NN', 'NNS'] and not IsAbbreviation(token.text): 
            print("Incorrect subject:", token.text)
            errors += 1
        
        # root is verb with tag being either present singular or plural present 
        if token.dep_ == 'ROOT' and token.tag_ in ['VBZ', 'VBP'] and not IsAbbreviation(token.text):
            # for complex sentence, find all subjects of the sentence
            subjects = [t for t in token.head.children if t.dep_ == 'nsubj']
            # if complex sentence
            if subjects:
                verb_is_plural = token.tag_ == 'VBZ'
                for subject in subjects:
                    # redo the process
                    subject_is_plural = subject.tag_ == 'NNS' or subject.tag_ == 'NNPS'
                    # conflict with subject verb number agreement 
                    if subject_is_plural != verb_is_plural:
                        print("conflict with subject \"" + subject.text + "\" and verb agreement \"" + token.text + "\"")
                        errors += 1
                        break
        
        # auxillary verb error
        if token.dep_ == 'aux' and token.tag_ != 'MD':
            print("Error in auxillary verb:", token.text)
            errors += 1
    
        # indirect object error
        if token.dep_ == 'dobj' and token.tag_ != 'NN' and token.tag_ != 'NNS':
            print("Error in indirect object:", token.text)
            errors += 1 
    
    if errors == 0:
        print("No errors found!")


# main function
def main():
    sentence = input()
    IsPoorSentence(sentence)

main()