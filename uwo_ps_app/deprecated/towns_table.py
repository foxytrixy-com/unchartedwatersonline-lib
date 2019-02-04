"""A Utility module to get current town from nearby towns.
"""

TOWNS_TABLE = {}
TOWNS_TABLE[('Cairo', 'Jaffa', 'Beirut', 'Benghazi')]\
= 'Alexandria'
TOWNS_TABLE[('Tunis', 'Ceuta', 'Cagliari')]\
= 'Algiers'
TOWNS_TABLE[('Antwerp', 'Helder', 'Groningen', 'Bremen', 'Rotterdam')]\
= 'Amsterdam'
TOWNS_TABLE[('Venice', 'Zadar', 'Pisa', 'Cattaro')]\
= 'Ancona'
TOWNS_TABLE[('Amsterdam', 'Helder', 'Groningen', 'Rotterdam')]\
= 'Antwerp'
TOWNS_TABLE[('Salonika', 'Candia', 'Istanbul')]\
= 'Athens'
TOWNS_TABLE[('Valencia', 'Palma', 'Montpellier')]\
= 'Barcelona'
TOWNS_TABLE[('Famagusta', 'Jaffa', 'Alexandria', 'Cairo')]\
= 'Beirut'
TOWNS_TABLE[('Alexandria', 'Tripoli')]\
= 'Benghazi'
TOWNS_TABLE[('Oslo', 'Bremen', 'Hamburg')]\
= 'Bergen'
TOWNS_TABLE[('Porto', 'Gijon')]\
= 'Bilbao'
TOWNS_TABLE[('Nantes', 'Calais', 'Le Havre')]\
= 'Bordeaux'
TOWNS_TABLE[('Groningen', 'Hamburg')]\
= 'Bremen'
TOWNS_TABLE[('Sassari', 'Naples', 'Tunis')]\
= 'Cagliari'
TOWNS_TABLE[('Bordeaux', 'Nantes', 'Dover', 'Le Havre')]\
= 'Calais'
TOWNS_TABLE[('Genoa', 'Sassari', 'Marseille')]\
= 'Calvi'
TOWNS_TABLE[('Athens', 'Salonika', 'Famagusta')]\
= 'Candia'
TOWNS_TABLE[('Faro', 'Madeira', 'Ceuta')]\
= 'Casablanca'
TOWNS_TABLE[('Ragusa', 'Zadar', 'Ancona', 'Trieste', 'Venice')]\
= 'Cattaro'
TOWNS_TABLE[('Faro', 'Lisbon', 'Seville', 'Algiers')]\
= 'Ceuta'
TOWNS_TABLE[('Lubeck', 'Oslo')]\
= 'Copenhagen'
TOWNS_TABLE[('Riga', 'Visby')]\
= 'Danzig'
TOWNS_TABLE[('London', 'Plymouth', 'Calais', 'Portsmouth', 'Le Havre')]\
= 'Dover'
TOWNS_TABLE[('Plymouth', 'London', 'Edinburgh', 'Manchester', 'Portsmouth')]\
= 'Dublin'
TOWNS_TABLE[('London', 'Dover', 'Dublin', 'Plymouth')]\
= 'Edinburgh'
TOWNS_TABLE[('Beirut', 'Jaffa', 'Candia', 'Alexandria')]\
= 'Famagusta'
TOWNS_TABLE[('Lisbon', 'Porto', 'Gijon', 'Seville', 'Viana do Castelo')]\
= 'Faro'
TOWNS_TABLE[('Pisa', 'Calvi', 'Marseille', 'Naples')]\
= 'Genoa'
TOWNS_TABLE[('Porto', 'Lisbon', 'Faro', 'Seville', 'Bilbao')]\
= 'Gijon'
TOWNS_TABLE[('Amsterdam', 'Bremen', 'Helder', 'Rotterdam')]\
= 'Groningen'
TOWNS_TABLE[('Bremen', 'Groningen', 'Lubeck')]\
= 'Hamburg'
TOWNS_TABLE[('Antwerp', 'Amsterdam', 'Groningen', 'Rotterdam')]\
= 'Helder'
TOWNS_TABLE[('Odessa', 'Trebizond', 'Sevastopol', 'Kaffa')]\
= 'Istanbul'
TOWNS_TABLE[('Beirut', 'Famagusta', 'Cairo', 'Alexandria')]\
= 'Jaffa'
TOWNS_TABLE[('Sevastopol', 'Trebizond')]\
= 'Kaffa'
TOWNS_TABLE[('Stockholm', 'Riga', 'Visby', 'St. Petersburg')]\
= 'Kokkola'
TOWNS_TABLE[('Madeira', 'Casablanca', 'Arguin')]\
= 'Las Palmas'
TOWNS_TABLE[('Calais', 'Nantes', 'Bordeaux', 'Portsmouth')]\
= 'Le Havre'
TOWNS_TABLE[('Faro', 'Porto', 'Ceuta', 'Madeira', 'Viana do Castelo')]\
= 'Lisbon'
TOWNS_TABLE[('Dover', 'Plymouth', 'Edinburgh', 'Dublin', 'Portsmouth', 'Manchester')]\
= 'London'
TOWNS_TABLE[('Hamburg', 'Copenhagen', 'Danzig')]\
= 'Lubeck'
TOWNS_TABLE[('Las Palmas', 'Casablanca', 'The Azores')]\
= 'Madeira'
TOWNS_TABLE[('Seville', 'Valencia', 'Palma')]\
= 'Malaga'
TOWNS_TABLE[('Dublin', 'Plymouth', 'Portsmouth', 'Dover', 'London')]\
= 'Manchester'
TOWNS_TABLE[('Montpellier', 'Genoa', 'Calvi', 'Pisa')]\
= 'Marseilles'
TOWNS_TABLE[('Marseille', 'Barcelona')]\
= 'Montpellier'
TOWNS_TABLE[('Bordeaux', 'Calais', 'Le Havre')]\
= 'Nantes'
TOWNS_TABLE[('Pisa', 'Syracuse', 'Cagliari', 'Calvi')]\
= 'Naples'
TOWNS_TABLE[('Sevastopol', 'Barcelona')]\
= 'Odessa'
TOWNS_TABLE[('Copenhagen', 'Bergen', 'Stockholm')]\
= 'Oslo'
TOWNS_TABLE[('Valencia', 'Malaga', 'Barcelona')]\
= 'Palma'
TOWNS_TABLE[('Genoa', 'Calvi', 'Naples')]\
= 'Pisa'
TOWNS_TABLE[('London', 'Dublin', 'Edinburgh', 'Dover', 'Portsmouth')]\
= 'Plymouth'
TOWNS_TABLE[('Lisbon', 'Faro', 'Gijon', 'The Azores', 'Viana do Castelo')]\
= 'Porto'
TOWNS_TABLE[('Dover', 'Plymouth', 'London', 'Dublin', 'Manchester')]\
= 'Portsmouth'
TOWNS_TABLE[('Zadar', 'Ancona', 'Trieste', 'Venice', 'Candia')]\
= 'Ragusa'
TOWNS_TABLE[('Kokkola', 'Stockholm', 'Visby', 'St. Petersburg')]\
= 'Riga'
TOWNS_TABLE[('Helder', 'Antwerp', 'Amsterdam', 'Groningen')]\
= 'Rotterdam'
TOWNS_TABLE[('Athens', 'Candia', 'Istanbul')]\
= 'Salonika'
TOWNS_TABLE[('Cagliari', 'Calvi', 'Marseille')]\
= 'Sassari'
TOWNS_TABLE[('Kaffa', 'Odessa')]\
= 'Sevastopol'
TOWNS_TABLE[('Malaga', 'Faro', 'Valencia', 'Palma')]\
= 'Seville'
TOWNS_TABLE[('Stockholm', 'Riga', 'Kokkola', 'Visby')]\
= 'St. Petersburg'
TOWNS_TABLE[('Kokkola', 'Visby', 'Danzig', 'Riga')]\
= 'Stockholm'
TOWNS_TABLE[('Naples', 'Cagliari', 'Sassari', 'Tunis')]\
= 'Syracuse'
TOWNS_TABLE[('Porto', 'Lisbon')]\
= 'The Azores'
TOWNS_TABLE[('Kaffa', 'Sevastopol')]\
= 'Trebizond'
TOWNS_TABLE[('Venice', 'Zadar', 'Ragusa', 'Candia')]\
= 'Trieste'
TOWNS_TABLE[('Tunis', 'Benghazi', 'Algiers')]\
= 'Tripoli'
TOWNS_TABLE[('Algiers', 'Tripoli', 'Cagliari', 'Syracuse')]\
= 'Tunis'
TOWNS_TABLE[('Palma', 'Barcelona', 'Seville', 'Malaga')]\
= 'Valencia'
TOWNS_TABLE[('Trieste', 'Ancona', 'Zadar', 'Ragusa', 'Cattaro')]\
= 'Venice'
TOWNS_TABLE[('Porto', 'Lisbon', 'Faro', 'Gijon')]\
= 'Viana do Castelo'
TOWNS_TABLE[('Danzig', 'Stockholm', 'Riga')]\
= 'Visby'
TOWNS_TABLE[('Ragusa', 'Trieste', 'Cattaro')]\
= 'Zadar'

def get_current_town(nearby_towns):
    """Get town from nearby towns

    Arguments:
        nearby_towns (list): list of towns

    Return:
        town name (str)
        None if failed to search
    """
    for towns in TOWNS_TABLE.keys():
        for li in __make_listlist(towns):
            if li == nearby_towns:
                return TOWNS_TABLE.get(towns)

    return None

def __make_listlist(towns):
    """Split list of towns list.

    The nearby towns of a town can be over 5.
    But up to 5 towns can be displayed at once.
    """
    towns_list = list(towns)
    if len(towns) <= 5:
        return [towns_list]
    else:
        lists = []
        for i in range(len(towns)-5+1):
            lists += [towns_list[i:i+5]]
        return lists
