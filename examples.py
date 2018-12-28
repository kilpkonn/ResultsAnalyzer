"""Examples."""
from results_analyzer import Analyzer

if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.load_results("./example_data.csv")
    for n in analyzer.get_competitors():
        print(n)
    print('-' * 100)
    for n in analyzer.get_results(races=-2, discount=1):
        print(n)
