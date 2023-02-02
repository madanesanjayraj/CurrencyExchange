import csv
"""
This file will hold utilities

"""
def makeCSV(start, startAmount, data, profitablePath, nonReachableNodes) -> None:
    """
    Create CSV file from provided information

    :param str start: Start currency or Source Currency
    :param float startAmount: The initial amount of source currency before starting conversions
    :param list data: List of Currency Code, Currency Name, Amount, Profitable Path
    :param list profitablePath: The list of currency nodes having profitable cycle
    :param list nonReachableNodes: The list of non reachable currency nodes from source
    :return: None
    """
    try:
        f = open('ProfitableTrades.csv', 'w', newline='')
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow([f"Max profitable cycle: {'|'.join(profitablePath)}"])
        writer.writerow([f"Non connected currencies: {'|'.join(nonReachableNodes)}"])
        writer.writerow([])
        writer.writerow([f"Started with {startAmount} {start}"])
        writer.writerow([])
        writer.writerow(['Currency Code', 'Currency Name', 'Amount', 'Path'])    
        for row in data:
            writer.writerow(row)
        # close the file
        f.close()
    except Exception as err:
        print(f"Failed to create CSV: {str(err)}")