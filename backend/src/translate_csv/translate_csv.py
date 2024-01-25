from deep_translator import GoogleTranslator
import csv
import os

target_language: str = str(os.environ["TARGET_LANGUAGE"])
source_language: str = str(os.environ["SOURCE_LANGUAGE"])

# we cloud make this in to a general function and use dependecy injection inorder to
# set up a general translator and move it to the lib
def translate(text: str) -> str:
    try:
        text = GoogleTranslator(source=source_language, target=target_language).translate(text)
        return text
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""

#ID,Price,name_lv,name_ru, name_en, aukcion price, category_id,code,aukcion,new,Atspējota,picture,is_new,is_top,new_until,information_lv,information_en,information_ru,tech_lv,tech_en,tech_ru,prod_count,use_prodcounts,url_lv,url_en,url_ru,description_lv,description_en,description_ru,disabled,keywords_lv,keywords_en,keywords_ru,small_text_lv,small_text_en,small_text_ru,brand_id,times_searched,times_purchased,meta_description_lv,meta_description_en,meta_description_ru,pvn

#we want Price name_lv category_id, picture, information_lv, description_lv, keywords_lv, small_text_lv, meta_description_lv,

# we want to translate the strings
# we want to create a sub csv form a whole csv

# we could make this in to a function that would open all the files in a dir


for filename in os.listdir('/app/src/'):
    if filename.endswith('.csv'):
        with open('dest/' + target_language + '.csv', 'w', newline='') as csvfile:
            fieldnames: [str] = [
                'name_' + target_language,
                'information_' + target_language,
                'tech_' + target_language,
                'description_' + target_language,
                'keywords_' + target_language,
                'small_text_' + target_language,
                'meta_description_' + target_language,
                'category_id',
                'picture',
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            filepath = os.path.join('/app/src/', filename)
            with open(filepath, newline='') as csvfile:
                row_count = sum(1 for row in csvfile)
                csvfile.seek(0)
                reader = csv.DictReader(csvfile)
                for index, row in enumerate(reader):
                    print("progress:", index / row_count * 100, "%")

                    new_row = {}
                    try:
                        new_row['name_' + target_language] =  row['name_lv'],
                    except Exception as e:
                        new_row['name_' + target_language] =  "name_missing",
                    try:
                        new_row['picture'] = row['picture']
                    except Exception as e:
                        new_row['picture'] = ""
                    try:
                        new_row['category_id'] = row['category_id']
                    except Exception as e:
                        new_row['category_id'] = 0

                    for field in ['information_lv', 'tech_lv', 'description_lv', 'keywords_lv', 'small_text_lv', 'meta_description_lv']:
                        if field in row:
                            translated_text = translate(row[field])  # translate the text
                            new_field_name = field.replace('_lv', '_' + target_language)
                            new_row[new_field_name] = translated_text
                        else:
                            print(f"Warning: Field {field} not found in row.")
                    writer.writerow(new_row)
