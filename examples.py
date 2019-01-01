"""Examples."""
from results_analyzer import Analyzer

if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.load_results("./example_data2.csv")
    for n in analyzer.get_competitors():
        print(f"{n}, worst race: {n.get_worst_race()}, best race: {n.best_race}, avg: {n.avg_place()}")
    print('-' * 100)
    for n in analyzer.get_results(discount=1):
        print(f"{n}, std dev: {n.std_dev}")
