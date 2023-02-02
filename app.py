from src.graph import Graph
from src.apiHandler import APIHandler
from src.utils import makeCSV


# Fetch Currency list and its rates from external API
result = APIHandler.fetchCurrencyRates()

currencyNames = {} # Holds currency name for currency name, later used in csv
currencies = [] # Holds all unique currency codes
for currency in result:    
    if currency['fromCurrencyCode'] not in currencies:
        currencies.append(currency['fromCurrencyCode'])
        currencyNames[currency['fromCurrencyCode']] = currency['fromCurrencyName']
    if currency['toCurrencyCode'] not in currencies:
        currencies.append(currency['toCurrencyCode'])
        currencyNames[currency['toCurrencyCode']] = currency['toCurrencyName']

# Create a graph structure
graph = Graph()

# Add all the nodes in the graph
for currencyCode in currencies:
    graph.addNode(currencyCode)

# Add all the edges between the nodes
for currency in result:
    graph.add_edge(currency['fromCurrencyCode'], currency['toCurrencyCode'], currency['exchangeRate'])
    # As this is currency conversion from back and forth, hence added reverse edge as well
    graph.add_edge(currency['toCurrencyCode'], currency['fromCurrencyCode'], 1/currency['exchangeRate']) 

start = "CAD" # Start or source currency, can be managed from here
startAmount = 100 # Starting amount with source currency

# To find the negative cycle in Bellman ford algorithm, negating all the values
graph.negate_logarithm_converter()

# Validate, if the source currency exists or not in the graph
if start not in currencies:
    print('Start currency not exists in the list')
    exit()
# Execute Bellman Ford algorithm to find profitable opportunity
profitablePath = graph.bellmanFord(start)
print(f"Profitable cycle: {'|'.join(profitablePath)}")

# Find non reachable currencies from source currency, so that we can ignore them hence forth as the trades are not possible
nonReachableNodes = graph.findNonReachableNodes(start)
print('Non reachable nodes', nonReachableNodes)

allCurrenciesSSP = {} # Get all possible single source shortest path from source currency to other currencies
for currency in currencies:
    if currency not in nonReachableNodes:
        # Find shortest path using BFS
        spath = graph.bfs(start, currency)
        allCurrenciesSSP[currency] = spath

finalData = [] # Holds final data for preparing csv
print(f"Started with {startAmount} {start}")

for node in allCurrenciesSSP:
    # Get final amount and trade sequence after trades
    path, amount = graph.getAmount(start, node, allCurrenciesSSP, profitablePath)
    finalData.append([node, currencyNames[node], round(amount*startAmount, 2), " | ".join(path)])
    
# Prepare CSV file and store output
makeCSV(start, startAmount, finalData, profitablePath, nonReachableNodes)

print("Finished Execution")
