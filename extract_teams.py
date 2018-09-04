import os

from fbmoo.settings import MAIN_LEAGUE_PATH


def extract_team(csv):
    first_row_skipped = False
    with open(csv, "r", encoding='windows-1252') as season_data:
        try:
            for count, row in enumerate(season_data):
                if not first_row_skipped:
                    first_row_skipped = True
                    continue
                # print(row)
                data = row.split(",")
                if len(data) < 4:   # invalid data
                    continue
                hometeam = data[2]
                awayteam = data[3]
                teams.add(hometeam)
                teams.add(awayteam)
        except Exception as e:
            print("Error csv file:", csv)
            print(e)


teams = set()

dirs = os.listdir(MAIN_LEAGUE_PATH)
for dir in dirs:
    league_path = MAIN_LEAGUE_PATH + dir
    # print('League path:', league_path)

    season_dirs = os.listdir(league_path)

    for season_dir in season_dirs:
        season_path = league_path + '/' + season_dir
        # print('Season path:', season_path)

        csvs = os.listdir(season_path)
        # print('CSV(s):', csvs, "\n")

        # start processing CSV(s)
        for csv in csvs:
            csv_path = season_path + '/' + csv
            extract_team(csv_path)

print("Teams:", teams)