import csv
from typing import List

from Commit import Commit

import dateutil.parser as parser


def is_day_row(row: List[str]) -> bool:
    return row[0] != None and len(row[0]) > 0


def process_dados() -> List[str]:
    commits: List[List[str]] = []
    user_map: dict = {}
    user_index: int = 0
    project_map: dict = {}
    project_index: int = 0
    with open('dados.csv', newline='') as dados:
        reader = csv.reader(dados, delimiter=',', quotechar='\"')
        next(reader, None)
        i = 1
        date_string = ''
        while True:
            try:
                row = next(reader)
            except StopIteration:
                break
            except Exception as e:
                print("Linha " + str(i) + " >> READ_ERROR >> ", e)
                i += 1
                continue
            if is_day_row(row):
                try:
                    date_string = parser.parse(row[0])
                except Exception as e:
                    print("Linha " + str(i) + " >> DATE_PARSE_ERROR >> ", e)
                    continue
                    raise e
            if not is_day_row(row):
                new_commit: Commit
                try:
                    new_commit = Commit(row, 0, date_string)
                except Exception as e:
                    print("Linha " + str(i) + " >> CONVERT_ERROR >> ", e)
                    raise e
                if new_commit.usuario not in user_map.keys():
                    user_map[new_commit.usuario] = user_index
                    user_index += 1
                if new_commit.projeto not in project_map.keys():
                    project_map[new_commit.projeto] = project_index
                    project_index += 1
                new_commit.usuario = user_map[new_commit.usuario]
                new_commit.projeto = project_map[new_commit.projeto]
                commits.append(new_commit.to_csv())
            i += 1
        return commits


commits = process_dados()
with open('processed_dados.csv', 'w', newline='', encoding='utf-8') as processed_dados:
    writer = csv.writer(processed_dados)
    writer.writerow(Commit.get_csv_headers())
    writer.writerows(commits)
