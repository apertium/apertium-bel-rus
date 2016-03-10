# Example of usage tag-analyzer
from BelarusianTagsAnalyzer import Analyzer

tag = 'NCIXNN1DP'

analyzer = Analyzer()

# It prints:
# ['Назоўнік', 'агульны', 'неадушаўлёны', '???????', 'нескарот', 'ніякі', '1 скланенне', 'давальны', 'множны']
print(analyzer.describe('NCIXNN1DP'))
