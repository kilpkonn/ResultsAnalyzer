"""Examples."""
from results_analyzer import Analyzer

if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.load_results("./example_data.txt")
    for n in analyzer.get_competitiors():
        print(n)
    print('-' * 100)
    for n in analyzer.get_results():
        print(n)
