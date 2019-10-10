# Timelessness, a.k.a. “Bestsellers vs. Evergreens”

This is the code that accompanies the DH2020 paper Van Zundert, J. et. al "Features of Timelessness: Intermediate Report on a Quest for Stylistic Features that Mark Literary Canonicity". It cleans up data, POS tags it through [Spacy](https://spacy.io/) using its [medium sized English model](https://spacy.io/models/en#en_core_web_md), creates [TfIdf](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) matrices, and does a [UMAP analysis](https://umap-learn.readthedocs.io/en/latest/) with plot to tease out differences between novels that were US [bestsellers during the early 20th century](https://en.wikipedia.org/wiki/Publishers_Weekly_lists_of_bestselling_novels_in_the_United_States) and novels that, according to information found on [Goodreads](https://www.goodreads.com/), are still read to this day.

As per usual in the case of highly bespoke text analytical software, this code is riddled with obsolete debug prints, surplus lines of inspection stuff, and has hard coded stuff in places where you'd really want it to be cleaner and more configurable. Apologies for that. To support your own tinkering I have clarified the function of each little script below.

Obviously this code expects data to work on. This data has not been reproduced here yet because of concerns of size and around potential intellectual property rights. The code in this repository expects your data to live in a directory next to its own. Expected layout:

```
└── project folder
    ├── data
    |   ├── Best Selling_Fulltext
    |   ├── Popular_Fulltext
    |   └── Texts-as-Data
    │       ├── Best Selling_Fulltext
    │       ├── Popular_Fulltext
    │       ├── POS
    │       └── TFIdf
    |           └── analysis_20191009_1253 (eg.)
    └── src
```

The idea in this project was to touch the original files as little as possible. So all cleaning was done script wise and should be repeatable. In a very small set of cases (two or three) I had to re-OCR stuff using [Tesseract](https://github.com/tesseract-ocr/tesseract), or upgraded OCR with [NLTK](https://www.nltk.org/). These particular steps have not been documented as code.

## Folder contents

#### data/Best Selling_Fulltext & data/Popular_Fulltext
Contain your original .txt files according to category.

#### data/Texts-as-Data/Best Selling_Fulltext & data/Texts-as-Data/Popular_Fulltext
Receive the cleaned and prepared texts for analysis.

#### data/Texts-as-Data/POS
Receives all pickles with POS tag information, one per text.

#### data/Texts-as-Data/TfIdf
Receives pickles containing TfIdfs and Vectorizers for analysis, pickles with umap analysis information, and plots.

#### scr
Where you put the files from this repository.

## Function of scripts, roughly in the order in which you would want to use them

#### utils.py
Some helpers to generate lists of file names conveniently and correct wrong txt file encodings. Also the place where some useful configuration of paths is centralized.

#### src_to_txt.py
Helpers to figure out and clean up bad text sources. E.g. un-OCR'ed pdfs, badly ocr'ed, in which NLTK was used to suggest respelling. Contains some notes on what was done in specific cases to the actual .txt and .pdf files I received.

#### shape_data.py
Worker horse that figures out what part of a .txt file is story text and what is para text. Lines of story text are marked with "[+]", paratext is marked "[-]". Writes marked files from `data/Best Selling_Fulltext` to `data/Texts-as-Data\Best Selling_Fulltext`, likewise for `Popular_Fulltext`.

#### overlap_popularbestselling.py
Helper to figure out if there are duplicate texts between the two sets (that, if present, will show as 'both' in the legend of plots). This is determined based on file name, but file names not always play nice, so  an edit distance is used to determine possible overlap too.

#### pos_data.py
POS tags .txt files in `data/Texts-as-Data/Best Selling_Fulltext` and `data/Texts-as-Data/Popular_Fulltext` and pushes the resulte as a POS pickle per .txt file into `data/Texts-as-Data/POS`.

#### pos_reporting.py
Helper to inspect how well the POS tagger is doing. Can print a 'token + POS tag' representation of a .txt file.

#### tfidf.py
Creates TfIdfs for POS pickles in `data/Texts-as-Data/POS` and writes the vectorizers and tfids to the `Texts-as-Data/TfIdf` folder. *Beware*: adjusting resulting file locations is by hardcoding.

#### umap_texts.py
Calculates umaps for two categories based on tfids pickles in `Text-as-Data/TfIdf` subfolders. *Beware*: adjusting file selection and resulting file locations is through hardcoding.

#### gradient_grid.py
Helper to produce gradient patches in plots

#### plotter.py
Creates charts from umap information.

#### text_length_global.py
Script to determine the overall length of the two sets.

#### sent_lengths_analysis.py
Calculates mean and stdev for sentence length of each novel in each category, can plot (overlay) histograms of the variance of these means.

--JZ_20191010_1705
