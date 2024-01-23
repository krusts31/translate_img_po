from deep_translator import GoogleTranslator
import polib
import os

target_file = str(os.environ["TARGET_FILE"])
target_language = str(os.environ["TARGET_LANGUAGE"])
source_language= str(os.environ["SOURCE_LANGUAGE"])

def translate(text: str, target_language: str) -> str:
    try:
        text = GoogleTranslator(source='en', target=target_language).translate(text)
        return text
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""

po = polib.pofile("po-files/" + target_file)

for entry in po:
    if entry.msgstr == "" and entry.msgid != "":
        entry.msgstr = translate(entry.msgid, target_language)
    if entry.msgid_plural != "" or entry.msgstr_plural == "":
        entry.msgstr_plural = {}

        translated_singular = translate(entry.msgid, target_language)
        translated_plural = translate(entry.msgid_plural, target_language)

        entry.msgstr_plural[0] = translated_singular
        entry.msgstr_plural[1] = translated_plural
    print("Total translated: ", po.percent_translated(), "%", flush=True)

po.save("result/" + target_file)
po.save_as_mofile("result/" + target_file + '.mo')
