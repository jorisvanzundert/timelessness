from spellchecker import SpellChecker
import nltk
import utils

def find_untxted_PDFs():
    for dir in [ utils.POPULAR_FULLTEXT, utils.BEST_SELLING_FULLTEXT ]:
        pdfs = set( utils.get_file_names_by_extension( dir, "pdf", utils.DROP_EXTENSION ) )
        txts = set( utils.get_file_names_by_extension( dir, "txt", utils.DROP_EXTENSION ) )
        print( dir, len(pdfs) )
        for pdf_without_txt in (pdfs-txts):
            print( pdf_without_txt )

def list_misspellings( file_path ):
    spell = SpellChecker()
    a_text = open( file_path, "r" ).read()
    text_tokens = nltk.word_tokenize( a_text )
    vocabulary = sorted( set( text_tokens ) )
    misspelled = list( spell.unknown( vocabulary ) )
    concordance = nltk.text.ConcordanceIndex( text_tokens )
    misspelled.remove("’")
    misspelled.remove("‘")
    misspelled.remove("”")
    misspelled.remove("“")
    misspelled.remove("``")
    misspelled.remove("—")
    print( len( misspelled ) )
    for token in misspelled:
        kwics = concordance.find_concordance( token, width=40 )
        for kwic in kwics:
            print( kwic.query, ":", kwic.line )

# MAIN

find_untxted_PDFs()

# Steps taken to turn initial data into parseable
#
# 1) From alternative English sources (because files were German/Spanish), pdf/ocr:
#    * POP_1910_The Notebooks of Malte Laurids Brigge
#    * POP_1913_Petersburg
#    * POP_1914_Niebla
# 2) Removes POP_POP_1917_Cuentos de amor, de locura y de muerte as it is in Spanish
#    and no alternative source found.
# 3) pdftotext
#    * POP_1919_In the Shadow of Young Girls in Flower (In Search of Lost Time, #2)
#    * POP_1914_The Dead.pdf
# 4) mv POP_1921_The\ Good\ Soldier\ Svejk.txt POP_1921_The\ Good\ Soldier\ Svejk.pdf
# 5) OCR'd Sveijk
# 6) Use list_misspellings to improve the OCR
# 7) rm *.pdf
# 8) remove space in front of filename: " BS_1917_The Light in the Clearing"
# 9) convert to UTF-8 (from CP1252):
#       utils.correct_wrong_encodings( POPULAR_FULLTEXT )
# --
