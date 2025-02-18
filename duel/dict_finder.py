import csv

def change_to_dict():
    """Change the csv format into list of dictionary format"""
    with open('duel/game_data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
        return data
    
def dict_finder(name):
    """Find the matching name dictionary then output that dictionary"""
    data = change_to_dict()
    finder = lambda x : x["Name"] == name
    filtered = next(filter(finder, data))
    return filtered
            