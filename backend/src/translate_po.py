from deep_translator import GoogleTranslator
import polib

def translate(text: str, target_language: str) -> str:
    try:
        text = GoogleTranslator(source='en', target=target_language).translate(text)
        return text
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""

target_file = "wp-plugins-woocommerce-stable-lv.po"

target_language = "lv"

#add src dest lang
async def translate_po_file(file: any) -> str:
    po = polib.pofile(file)

    for entry in po:
        if entry.msgstr == "" and entry.msgid != "":
            entry.msgstr = translate(entry.msgid, target_language)
        if entry.msgid_plural != "" and entry.msgstr_plural == "":
            entry.msgstr_plural = {}

            translated_singular = translate(entry.msgid, target_language)
            translated_plural = translate(entry.msgid_plural, target_language)

            entry.msgstr_plural[0] = translated_singular
            entry.msgstr_plural[1] = translated_plural
        print("Total translated: ", po.percent_translated(), "%", flush=True)

    po.save(target_file)
    po.save_as_mofile(target_file + '.mo')
    return target_file
