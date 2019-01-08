"""Examples."""
from results_analyzer import Analyzer
from results_analyzer import Place
from year import Regatta
from numpy import array
import numpy as np
from scipy.stats import spearmanr
from scipy.stats import kendalltau

def line(i, name, club, races, total, nett, seperator, silver=None, gold=None, change=None, key: str = "sama", original: bool=False):
    always = "{0:3d}"+seperator+"{1:<25s}"+seperator+"{2:<10s}"+seperator+"{3:>}"+seperator+"{4:6}"+seperator+"{5:5}"
    fin = "{6:>8s}"+seperator+"{7:>4s}"
    chan = "{8:>7d}"
    b = seperator+"|"+seperator
    if original and key == "uus":
        a = always+fin+b
        write = a.format(i, name, club, races, total, nett, silver, gold)
    elif key == "uus" and not original:
        a = always+chan+"\n"
        write = a.format(i, name, club, races, total, nett, change)
    elif original and key == "vana":
        a = always+b
        write = a.format(i, name, club, races, total, nett)
    elif key == "vana" and not original:
        a = always+fin+chan+"\n"
        write = a.format(i, name, club, races, total, nett, silver, gold, change)
    elif key == "sama" and original:
        a = always+fin+b
        write = a.format(i, name, club, races, total, nett, silver, gold)
    elif key == "sama" and not original:
        a = always+fin+chan+"\n"
        write = a.format(i, name, club, races, total, nett, silver, gold, change)
    return write


def write_file(f, original, analyzed, key: str = "same"):
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
        name = line.name
        club = line.club
        for b in original:
            if analyzed[i].name == b.name:
                orig = original.index(b)
        change = orig - i
        if key == "new":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}".format("Pos", "Name", "Club", races_syntax, "Total", "Nett", "Silver", "Gold"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>7s}".format("Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Change"))
                f.write("\n")
            #f.write(line(i + 1, name, club, races, total, nett, "\t", silver, gold, key="uus", original=True))
            #f.write(line(i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, change, "\t", silver, gold, key="uus"))
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(i + 1, line.name, line.club, races, total, nett, silver, gold))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>7d}".format(i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, change))
            f.write("\n")
        if key == "old":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}".format("Pos", "Name", "Club", races_syntax, "Total", "Nett"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}\t{8:>7s}".format("Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Silver", "Gold", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}".format(i + 1, line.name, line.club, races, total, nett))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}\t{8:>7d}".format(i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, silver_new, gold_new, change))
            f.write("\n")
        if key == "same":
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


def year_results(result, list_1, discount: int = 0, races: int = None):
    res = analyzer.get_results(discount=discount, races=races)
    for i, j in enumerate(list_1):
        got = False
        top = False
        for k in res[:3]:
            if j.name == k.name:
                point = [50 - i, 3 - res.index(k)]
                top = True
        if top == False:
            point = [50 - i]
        for k in result:
            if j.name in k[0]:
                k.append(point)
                got = True
        if not got:
            result.append([j.name, point])


def sorted_year(list_1):
    for i in list_1:
        total = 0
        for j in i[1:]:
            total = total + sum(j)
        i.append(total)
    list_sort = sorted(list_1, key=lambda x: x[len(x) - 1], reverse=True)

    for i, j in enumerate(list_sort):
        if i == len(list_sort)-1:
            break
        if j[len(j) - 1] == list_sort[i + 1][len(list_sort[i + 1]) - 1]:
            equal = True
            first = []
            second = []
            for a in range(len(j[1:len(j) - 1])):
                first.append(j[a + 1][0])
                second.append(list_sort[i + 1][a + 1][0])
            first_1 = sorted(first, reverse=True)
            second_2 = sorted(second, reverse=True)
            for a in range(len(first_1)):
                if first_1[a] != second_2[a]:
                    if first_1[a] < second_2[a]:
                        list_sort[i], list_sort[i + 1] = list_sort[i + 1], list_sort[i]
                    equal = False
            if equal == True:
                if first[len(first) - 1] < second[len(second) - 1]:
                    list_sort[i], list_sort[i + 1] = list_sort[i + 1], list_sort[i]
    return list_sort


if __name__ == "__main__":
    analyzer = Analyzer()
    files = ["./example_data.csv", "./example_data_2.csv"]
    print(Regatta("./example_data.csv").get_results_finals())
    year_original = []
    year_1 = []
    year_2 = []
    year_3 = []
    for k, file in enumerate(files):
        analyzer.load_results(file)
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
                print(line(i+1, n.name, n.club, races, total, nett, "\t", silver, gold, key="uus", original=True))
                # print("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(i+1, n.name, n.club, races, total, nett, silver, gold))
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
            print(np.corrcoef(x, y))
            print(spearmanr(x, y))
            print(kendalltau(x, y))
            correlation = round(spearmanr(x, y)[0], 2)

            year_results(year_original, results_original, discount=1)
            year_results(year_1, results_newtoold_1, discount=1)
            year_results(year_2, results_newtoold_2, discount=1)
            year_results(year_3, results_newtoold_3, discount=1)

            filew = "2016_"+str(k+1)+".csv"
            f = open(filew, "w")
            write_file(f, Regatta(file).get_results_normal_finals(), Regatta(file).get_results_normal(), key="new")
            f.write("\n")
            write_file(f, results_original, results_newtoold_2, key="new")
            f.write("\n")
            write_file(f, results_original, results_newtoold_3, key="new")
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

            new_5_data = analyzer.get_competitors()
            new_analyzer_5 = Analyzer()
            new_analyzer_5.import_data(new_5_data)
            new_5 = new_analyzer_5.get_results(discount=1, races=-1)
            for i in new_5[:10]:
                i.silver = i.races[len(i.races) - 1]
                i.gold = i.races[len(i.races) - 1]
            new_analyzer_5.import_data(new_5)
            results = new_analyzer_5.get_results_final(discount=1, races=-1)
            for n, i in enumerate(results[:4]):
                i.silver = None
                i.gold = Place(n + 1, str(n + 1))
            for n, i in enumerate(results[3:10]):
                if n == 0:
                    i.silver = Place(n + 1, str(n + 1))
                else:
                    i.gold = None
                    i.silver = Place(n + 1, str(n + 1))
            results_oldtonew_3 = results

            x1, y1 = create_array(results_original_old, results_oldtonew_1)
            x2, y2 = create_array(results_original_old, results_oldtonew_2)
            x3, y3 = create_array(results_original_old, results_oldtonew_3)
            x = x1 + x2 + x3
            y = y1 + y2 + y3
            x = array(x)
            y = array(y)
            correlation = round(spearmanr(x, y)[0], 2)

            year_results(year_original, results_original_old, discount=1)
            year_results(year_1, results_oldtonew_1, discount=1)
            year_results(year_2, results_oldtonew_2, discount=1, races= -2)
            year_results(year_3, results_oldtonew_3, discount=1, races= -1)

            filew = "2016_" + str(k + 1) + ".csv"
            f = open(filew, "w")
            write_file(f, results_original_old, results_oldtonew_1, key="old")
            f.write("\n")
            write_file(f, results_original_old, results_oldtonew_2, key="old")
            f.write("\n")
            write_file(f, results_original_old, results_oldtonew_3, key="old")
            f.write("\n")
            f.write("correlation = ")
            f.write(str(correlation))
            f.close()

    year_original = sorted_year(year_original)
    year_1 = sorted_year(year_1)
    year_2 = sorted_year(year_2)
    year_3 = sorted_year(year_3)

    for i in year_1:
        linew = ''
        for j in i[1:len(i)-1]:
            if len(j) == 2:
                linew = linew + "\t" + str(j[0]) +"\t"+ str(j[1])
            else:
                linew = linew +"\t"+ str(j[0]) +"\t" + ""
        linew.strip()
        print("{0:<25s}\t{1:>}\t{2:3d}".format(i[0], linew, i[len(i)-1]))



