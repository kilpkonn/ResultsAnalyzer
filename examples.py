"""Examples."""
from results_analyzer import Analyzer
from results_analyzer import Place
from numpy import array
import numpy as np
from scipy.stats import spearmanr
from scipy.stats import kendalltau

def write_file(f, original, analyzed, key: str = "sama"):
    for i, line in enumerate(original):
        if not line.silver:
            silver = ""
        if line.silver:
            silver = str(line.silver)
        if not line.gold:
            gold = ""
        if line.gold:
            gold = str(line.gold)
        total = int(line.get_points_after(races=len(line.races)))
        nett = int(line.get_points_after(races=len(line.races), discount=1))
        races = '\t'.join([format(str(x), '>3') for x in line.races])
        races_syntax = '\t'.join([format("R" + str(x + 1), '>3') for x in range(len(line.races))])
        if not analyzed[i].silver:
            silver_new = ""
        if analyzed[i].silver:
            silver_new = str(analyzed[i].silver)
        if not analyzed[i].gold:
            gold_new = ""
        if analyzed[i].gold:
            gold_new = str(analyzed[i].gold)
        total_new = int(analyzed[i].get_points_after(races=len(analyzed[i].races)))
        nett_new = int(analyzed[i].get_points_after(races=len(analyzed[i].races), discount=1))
        races_new = '\t'.join([format(str(x), '>3') for x in analyzed[i].races])
        races_syntax_new = '\t'.join([format("R" + str(x + 1), '>3') for x in range(len(analyzed[i].races))])
        for b in original:
            if analyzed[i].name == b.name:
                orig = original.index(b)
        change = orig - i
        if key == "uus":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}".format("Pos", "Name", "Club", races_syntax, "Total", "Nett", "Silver", "Gold"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>7s}".format("Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(i + 1, line.name, line.club, races, total, nett, silver, gold))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>7d}".format(i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, change))
            f.write("\n")
        if key == "vana":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}".format("Pos", "Name", "Club", races_syntax, "Total", "Nett"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}\t{8:>7s}".format("Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Silver", "Gold", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}".format(i + 1, line.name, line.club, races, total, nett))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}\t{8:>7d}".format(i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, silver_new, gold_new, change))
            f.write("\n")
        if key == "sama":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}".format("Pos", "Name", "Club", races_syntax, "Total", "Nett", "Silver", "Gold"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}\t{8:>7s}".format("Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Silver", "Gold", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(i + 1, line.name, line.club, races, total, nett, silver, gold))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}\t{8:>7d}".format(i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, silver_new, gold_new, change))
            f.write("\n")
    f.write("-"*303)
def create_array(list1, list2):
    x = []
    y = []
    for i, line in enumerate(list1):
        x.append(i+1)
        for j, line2 in enumerate(list2):
            if line.name == line2.name:
                y.append(j+1)
        if i == 9:
            break
    return(x,y)


if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.load_results("./example_data.csv")
    for n in analyzer.get_competitors():
        print(f"{n}, worst race: {n.get_worst_race()}, best race: {n.best_race}, avg: {n.avg_place()}")
    print('-' * 100)

    if analyzer.get_competitors()[0].gold:
        results_original = analyzer.get_results_final_gold(discount=1)
        for i, n in enumerate(results_original):
            if not n.silver:
                silver = ""
            if n.silver:
                silver = str(n.silver)
            if not n.gold:
                gold = ""
            if n.gold:
                gold = str(n.gold)
            total = int(n.get_points_after(races=len(n.races)))
            nett = int(n.get_points_after(races=len(n.races), discount=1))
            races = '\t'.join([format(str(x), '>3') for x in n.races])
            races_syntax = '\t'.join([format("R"+str(x+1), '>3') for x in range(len(n.races))])
            if i == 0:
                print("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}".format("Pos", "Name", "Club", races_syntax, "Total", "Nett", "Silver", "Gold"))
            print("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(i+1, n.name, n.club, races, total, nett, silver, gold))
        print('-' * 100)

        results_newtoold_1 = analyzer.get_results(discount=1)
        for n in analyzer.get_results(discount=1):
            print(n)
        print('-' * 100)
        new = analyzer.get_competitors()
        for i in new:
            if not i.silver and not i.gold:
                i.races.append(Place(round(i.avg_place()), str(round(i.avg_place()))))
            elif i.silver and i.gold:
                i.races.append(i.gold)
            elif i.gold and not i.silver:
                i.races.append(i.gold)
            elif i.silver and not i.gold:
                i.races.append(i.silver + 3)

        new_analyzer = Analyzer()
        new_analyzer.import_data(new)
        results_newtoold_2 = new_analyzer.get_results(discount=1)
        for n in new_analyzer.get_results(discount=1):
            print(n)
        print('-' * 100)

        new_2 = analyzer.get_competitors()
        for i in new_2:
            if not i.silver and not i.gold:
                i.races.append(i.races[len(i.races)-2])
                i.races.append(i.races[len(i.races) - 2])
            elif i.silver and i.gold:
                i.races.append(i.silver)
                i.races.append(i.gold)
            elif i.gold and not i.silver:
                i.races.append(i.races[len(i.races)-2])
                i.races.append(i.gold)
            elif i.silver and not i.gold:
                i.races.append(i.silver)
                i.races.append(i.races[len(i.races) - 2])

        new_analyzer_2 = Analyzer()
        new_analyzer_2.import_data(new_2)
        results_newtoold_3 = new_analyzer_2.get_results(discount=1)
        for n in new_analyzer_2.get_results(discount=1):
            print(n)
        print('-' * 100)
        results_newtonew = analyzer.get_results_final(discount=1)
        x1, y1 = create_array(results_original, results_newtoold_1)
        x2, y2 = create_array(results_original, results_newtoold_2)
        x3, y3 = create_array(results_original, results_newtoold_3)
        x = x1 + x2 + x3
        y = y1 + y2 + y3
        x = array(x)
        y = array(y)
        print(x,y)
        print(np.corrcoef(x, y))
        print(spearmanr(x, y))
        print(kendalltau(x, y))
        correlation = round(spearmanr(x, y)[0], 2)

        f = open("example_results.txt", "w")
        write_file(f, results_original, results_newtoold_1, key="uus")
        f.write("\n")
        write_file(f, results_original, results_newtoold_2, key="uus")
        f.write("\n")
        write_file(f, results_original, results_newtoold_3, key="uus")
        f.write("\n")
        write_file(f, results_original, results_newtonew)
        f.write("\n")
        f.write("correlation = ")
        f.write(str(correlation))
        f.close()
    else:
        results_original_old = analyzer.get_results(discount=1)

        new_3_data = analyzer.get_competitors()
        new_analyzer_3 = Analyzer()
        new_analyzer_3.import_data(new_3_data)
        new_3 = new_analyzer_3.get_results(discount=1)
        for i in new_3[:10]:
            i.silver = i.races[len(i.races)-2]
            i.gold = i.races[len(i.races)-1]
        new_analyzer_3.import_data(new_3)
        results = new_analyzer_3.get_results_final(discount=1)
        for n, i in enumerate(results[:4]):
            i.silver = None
            i.gold = Place(n+1, str(n+1))
        for n, i in enumerate(results[3:10]):
            if n == 0:
                i.silver = Place(n + 1, str(n + 1))
            else:
                i.gold = None
                i.silver = Place(n+1, str(n+1))
        results_oldtonew_1 = results
        for i in results:
            print(i)
        print('-' * 100)

        new_4_data = analyzer.get_competitors()
        new_analyzer_4 = Analyzer()
        new_analyzer_4.import_data(new_3_data)
        new_4 = new_analyzer_4.get_results(discount=1, races=-2)
        for i in new_4[:10]:
            i.silver = i.races[len(i.races) - 2]
            i.gold = i.races[len(i.races) - 1]
        new_analyzer_4.import_data(new_4)
        results = new_analyzer_4.get_results_final(discount=1, races=-2)
        for n, i in enumerate(results[:4]):
            i.silver = None
            i.gold = Place(n + 1, str(n + 1))
        for n, i in enumerate(results[3:10]):
            if n == 0:
                i.silver = Place(n + 1, str(n + 1))
            else:
                i.gold = None
                i.silver = Place(n + 1, str(n + 1))
        results_oldtonew_2 = results
        for i in results:
            print(i)

        f = open("example_results.txt", "w")
        write_file(f, results_original_old, results_oldtonew_1, key="vana")
        f.write("\n")
        write_file(f, results_original_old, results_oldtonew_2, key="vana")
        f.close()


