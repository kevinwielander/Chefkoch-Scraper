import spacy
import re
nlp = spacy.load('de_core_news_md')

file_path = "../analysis/ingredients.txt"
output_file = "../analysis/ingredients_lemma_set.txt"
ingredients_lemmatized = []

try:
    # Open the file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the file line by line
        for line in file:
            # Process each line as needed
            cleaned_ingredient = re.sub(r'\s*\(.*\)|\s.*', '', line)
            cleaned_string = cleaned_ingredient.replace(',', '')
            ingredient_lemma = nlp(cleaned_string).text
            if ingredient_lemma not in ingredients_lemmatized:
                ingredients_lemmatized.append(ingredient_lemma)

    with open(output_file, 'w', encoding='utf-8') as file:
        for ingredient in ingredients_lemmatized:
             file.write(f"{ingredient}\n")  # Using a list for JSON serialization

except FileNotFoundError:
    print(f"File not found: {file_path}")

except Exception as e:
    print(f"Error reading file: {e}")

# mails=['Hallo. Ich spielte am frühen Morgen und ging dann zu einem Freund. Auf Wiedersehen', 'Guten Tag Ich mochte Bälle und will etwas kaufen. Tschüss']
#
# mails_lemma = []
#
# for mail in mails:
#      doc = nlp(mail)
#      result = ' '.join([x.lemma_ for x in doc])
#      mails_lemma.append(result)
#
#
# print(mails_lemma)