# Id_Nobel_Prize_Paper_Titles_Generation
## Solution for ODS Hackathon (October 2020) Id Nobel Prize Paper Titles Generation

During the Hackathon, organized by [ODS](https://ods.ai/) in October 2020 the solution to the following problem was designed:
to implement the [Ig Nobel Prize](https://www.improbable.com/) topics generator.

### How to use the script:
The script can be used in two modes:
1. The model fit according to the corpus from the dataset (`fit`)
2. The model run - topics generation (`run`).

#### `Fit`:
* The script file (_ig_nobel.py_) should be placed in the desired folder from the _tools_ folder, the scientific papers titles file in _.csv_ format (_paper_titles.csv_) [Google Drive](https://drive.google.com/drive/folders/1Icl9RaCK_5z3m8Ku3O9Imt2QYffH2a89?usp=sharing);
* in the commamd prompt the directory is changed to the one leading to the script and data (`cd your/directory`);
* during the first launch the model should be trained by calling the function `fit` and passing the argument - the dataset file name (`paper_titles.csv`);
All in all, `python ig_nobel.py fit paper_titles.csv`
#### `Run`:
* starting from the second launches the `run` function should be called, and the argument passed - the desired first word for a scientific paper in English (e.g. _interstellar_). The generation process takes 15 seconds on average (`python ig_nobel.py run interstellar`);

* as the model is trained according to the STEM (Science, Technology, Engineering, Mathematics) scientific papers, it is wise to insert a word from this fields. In case of random word insertion, the outputted title logic can be surprising :)


#### Take it brief:
`python ig_nobel.py fit paper_titles.csv` - to fit the model;
`python ig_nobel.py run space` - to run the title generation with the first word of _space_.

The script is written in Python 3.7; the data is in English. All the relevant frameworks version can be found in _requirements.txt_.

The data used for generation is the dataset of scientific papers titles ([STEM](https://www.kaggle.com/Cornell-University/arxiv)). The original dataset was cleaned first to present the data in tidy form: only titles are remained, the abbreviations were removed. As the result, 1.771.038 titles are used.

The generator is based on the trigram (3-gram) model ([source, in Russian](https://habr.com/ru/post/88514/)). The model presented in the article was re-built in the following parts:
* the first word free choice was added to the logic;
* in case of the desired first word missig in the corpus, the closest word in the meaning of the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) is used;
* the randomization part was improved (every word, starting from the second, is chosen randomly from the presented in the model pairs (word, probability) with respect to the previous word);
* CLI (Command Line Interface) was added.

### Operation principle:
The script consists of three logical parts:
1. Data preparation for the model build. Firstly, from the initial corpus (papers titles) the text generator is formed (the `gen_lines` function). Then, the token generator is formed (the `gen_tokens` function); the generator yields the sequence of words and punctiation marks. The trigram generator (the `gen_trigrams` function) yields the array of three consecutive tokens. The $ symbol is used for sentence borders designation. In general, the trigrams generator operates as follows: it returns three consecutive words, shifting by one token at each iteration. 
2. Model composing (training) (the `train` function). In the function the word probability with respect to the previous two words is calculated; every word and its probability is placed in the dictionary - the model itself. From the software point of view, the model (`model`) is a list, in which for each words pair the list of pairs (word, probability) is contained. 
3. Titles generation (the `gen_title` function). The first word is inserted via CLI. In case of the inserted word is missing in the model, using the method `process.extract` from the `fuzzywuzzy` library, based on the Levenshtein distance, the random word is selected out of five most closest words. Every following word is selected randomly from the model based on the previous word (the `unirand` function). The title length is limited by 100 symbols. 


### Development prospects:
* improved randomization (customly designed for each purpose - more random titles, or just strict scientific titles);
* data variety (the model is trained and works only with STEM papers);
* improved performance (using more sophisticated algorithms).

The example of using the main functionality can be found in the Jupyter notebook `Ig_Nobel_Prize.ipynb`.

* Author - Aleksandr Mirlenko
* Mentor - [Anastasia Malysheva](https://github.com/AnastasiaMalysheva)
