from bs4 import BeautifulSoup
import pandas as pd
import os
from os import listdir
from os.path import isfile, join


def extract_element_data(num):
    """Extracts data from a specified HTML element"""

    # try / except to catch different encodings 
        try:
            file_object = open(f'./results/{i}.html', "r")
            parsed_content = BeautifulSoup(file_object, 'lxml')

        except:
            file_object = open(f'./results/{i}.html', "r", encoding="utf-8")
            parsed_content = BeautifulSoup(file_object, 'lxml')

        
    # Parsing html with beautifulsoup
    parsed_content = BeautifulSoup(file_object, 'lxml')

    # Feature dossard, nom, prénom
    cat = parsed_content.find("div", {"class": "cat"}).getText(strip=True)
    cat = cat.replace('Infos coureurDossard ', '')
    cat = cat.replace('Infos coureurPalmarèsDossard ', '')
    cat = cat.split('   Diagonale des fous - ')
    num_dossard = int(cat[0])
    pnom = parsed_content.find("span", {"class": "pnom"}).getText()
    nom = parsed_content.find("span", {"class": "nom"}).getText()

    # initializing a athlete list 
    athlete = [num_dossard, pnom, nom]
    
    
    # features 'genre', 'cat', 'club', 'nationalité', 'ville', 'pays','etat', 
                        'vit_moy'
    personal_info = parsed_content.find("div", {"class": "col2"})
    tds = personal_info('td')
    for i, td in enumerate(tds):
        if i in [1, 3, 5, 7, 9, 11]:
            athlete.append(td.getText(strip=True))

    # features different for women (global rankin and women ranking) and men    
    # features 'class_gen', 'class_F','class_cat', 'arrivée', 'tps_course',
    table_resume = parsed_content.find("table", {"class": "resume"})
    resume_rows = table_resume('tr')
    for i, row in enumerate(resume_rows):
        for j, td in enumerate(row('td')):
            athlete.append(td.getText(strip=True))
    if athlete[3]=='Femme':
        athlete[9] = athlete[9].replace('Etat', '')
        athlete[10] = int(athlete[10][-1])
        athlete[11] = int(athlete[11][-1])
        athlete[12] = int(athlete[12][-1])
        athlete[13] = athlete[13].replace('Dernier pointVe. ', '')[:5]
        if athlete[9] != "Arrêté":
            athlete[14] = athlete[14].replace('Temps de course', '')
            athlete[15] = athlete[15].replace('Vitesse', '')
            athlete[15] = athlete[15].replace(' km/h', '')
            athlete[15] = float(athlete[15].replace(',', '.'))
    else:
        athlete[9] = athlete[9].replace('Etat', '')
        athlete[10] = int(athlete[10][-1])
        athlete[11] = int(athlete[11][-1])
        athlete[12] = athlete[12].replace('Dernier pointVe. ', '')[:5]
        if athlete[9]!="Arrêté":
            athlete[13] = athlete[13].replace('Temps de course', '')
            athlete[14] = athlete[14].replace('Vitesse', '')
            athlete[14] = athlete[14].replace(' km/h', '')
            athlete[14] = float(athlete[14].replace(',', '.'))
            athlete.insert(11,'')

    # Perf num_dossard, Point_de_passage, Vitesse, Class., Jour/heure_de_passage, tps_course
    table_tpasse = parsed_content.find("table", {"class": "tpass"})
    rows = table_tpasse('tr')
    rows_content = []
    for i, row in enumerate(rows):
        list = []
        if i == 0:
            for th in row('th'):
                if th.getText() == '\n\t\t\t\t\t\t\tTemps de course\t\t\t\t\t\t\t':
                    list.append('Temps de course')
                else:
                    list.append(th.getText())
                # print(list )
            rows_content.append(list)
        else:
            list = [num_dossard]
            for j, td in enumerate(row('td')):
                if j == 0:
                    list.append(td.find('a').getText())
                else:
                    list.append(td.getText(strip=True))
            rows_content.append(list)

    perf = rows_content[1:]

    return athlete, perf


def parse_individuals():
    directory_path = os.getcwd()
    results_directory = join(directory_path, 'results')
    file_list = [f for f in listdir(results_directory) if isfile(join(results_directory, f))]
    target_directory = join(directory_path, 'parsed_results')
    datasets_directory = join(directory_path, 'datasets')

    athletes_columns = ['num_dossard', 'pname', 'name', 'genre', 'cat', 'club', 'nationalité', 'ville', 'pays','etat', 'class_gen', 'class_F','class_cat', 'arrivée', 'tps_course',
                        'vit_moy' ]

    performances_columns = ['num_dossard', 'Point_de_passage', 'Vitesse', 'Class.', 'Jour/heure_de_passage',
                            'tps_course']

    athletes = []
    performances = []
    errors=[]
    for i in range(len(file_list)):
        try:
            athlete, performance = extract_element_data(i)
            athletes.append(athlete)
            for lign in performance:
                performances.append(lign)
        except Exception as e:
            print("ERROR : " + str(e))
            print(i)
            errors.append(i)


    # Save Athletes dataset to CSV
    athletes_df = pd.DataFrame(athletes)
    athletes_df.columns = athletes_columns
    athletes_df.to_csv(join(datasets_directory, 'athletes.csv'), header=True, index=False)
    print(athletes_df.head())

    # Save Performancet dataset to CSV
    performances_df = pd.DataFrame(performances)
    performances_df.columns = performances_columns
    performances_df.to_csv(join(datasets_directory, 'performances.csv'), header=True, index=False)
    print(performances_df.head())

    # Print errors
    print(errors)
    return


if __name__ == "__main__":
    parse_individuals()