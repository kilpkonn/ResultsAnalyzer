"""Examples."""
from results_analyzer import Analyzer
from season import Regatta, Season
from numpy import array
import numpy as np
from scipy.stats import spearmanr
from scipy.stats import kendalltau


def line(i, name, club, races, total, nett, seperator, silver=None, gold=None, change=None, key: str = "sama",
         original: bool=False):
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
        for b in original:
            if analyzed[i].name == b.name:
                orig = original.index(b)
        change = orig - i
        if key == "new":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}".format(
                    "Pos", "Name", "Club", races_syntax, "Total", "Nett", "Silver", "Gold"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>7s}".format(
                    "Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(
                i + 1, line.name, line.club, races, total, nett, silver, gold))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>7d}".format(
                i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, change))
            f.write("\n")
        if key == "old":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}".format(
                    "Pos", "Name", "Club", races_syntax, "Total", "Nett"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}\t{8:>7s}".format(
                    "Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Silver", "Gold", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}".format(
                i + 1, line.name, line.club, races, total, nett))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}\t{8:>7d}".format(
                i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, silver_new, gold_new,
                change))
            f.write("\n")
        if key == "same":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}".format(
                    "Pos", "Name", "Club", races_syntax, "Total", "Nett", "Silver", "Gold"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}\t{8:>7s}".format(
                    "Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Silver", "Gold", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(
                i + 1, line.name, line.club, races, total, nett, silver, gold))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}\t{8:>7d}".format(
                i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, silver_new, gold_new,
                change))
            f.write("\n")
    f.write("-"*303)
    f.write("\n")


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


def create_array_season(list1, list2):
    x = []
    y = []
    for i, line in enumerate(list1):
        x.append(i+1)
        for j, line2 in enumerate(list2):
            if line[0] == line2[0]:
                y.append(j+1)
        if i == 19:
            break
    return(x,y)


def add_row(files, row):
    cup = ""
    offset = 0
    for j in range(len(files)):
        if j + offset < len(row[1][:len(row[1]) - 2]):
            if j + 1 == row[1][j + offset].number and row[1][j + offset].extra != 0:
                cup = cup + "\t" + format(row[1][j + offset].points, " >3") + "\t" + format(row[1][j + offset].extra,
                                                                                            " >1")
            elif j + 1 == row[1][j + offset].number and row[1][j + offset].extra == 0:
                cup = cup + "\t" + format(row[1][j + offset].points, " >3") + "\t" + format("", " >1")
            elif j + 1 < row[1][j + offset].number:
                cup = cup + "\t" + format("", " >3") + "\t" + format("", " >1")
                offset = offset - 1
        else:
            cup = cup + "\t" + format("", " >3") + "\t" + format("", " >1")
    return cup


def write_year(f, original, converted, files):
    for i, row in enumerate(original):
        for k in original:
            if converted[i][0] == k[0]:
                change = original.index(k) - i
        if i == 0:
            cupname = ""
            for j in range(len(files)):
                cupname = cupname + "\t" + format(str(j+1), ">3") + "\t" + format("", " >1")
            f.write("{0:>3s}\t{1:<25s}\t{2:>30s}\t{3:>6s}".format("Pos", "Name", cupname, "Total"))
            f.write("\t" + "|" + "\t")
            f.write("{0:>3s}\t{1:<25s}\t{2:>30s}\t{3:>6s}\t{4:>7s}".format("Pos", "Name", cupname, "Total", "Change"))
            f.write("\n")
        cup = add_row(files, row)
        cup1 = add_row(files, converted[i])
        f.write("{0:>3d}\t{1:<25s}\t{2:>30s}\t{3:>6}".format(i+1, row[0], cup, row[1][len(row[1])-2]))
        f.write("\t"+"|"+"\t")
        f.write("{0:>3d}\t{1:<25s}\t{2:>30s}\t{3:>6}\t{4:>7}".format(i+1, converted[i][0], cup1,
                                                                     converted[i][1][len(row[1])-2], change))
        f.write("\n")
    f.write("-" * 303)
    f.write("\n")


if __name__ == "__main__":
    analyzer = Analyzer()
    year = "2014_"
    files = ["./example_data.csv", "./example_data_2.csv"]
    for k, file in enumerate(files):
        regatta = Regatta(file)
        analyzer.load_results(file)
        if analyzer.is_finals():
            x1, y1 = create_array(regatta.get_results_normal_finals(), regatta.get_results_normal())
            x2, y2 = create_array(regatta.get_results_normal_finals(), regatta.get_results_2())
            x3, y3 = create_array(regatta.get_results_normal_finals(), regatta.get_results_3())
            x = x1 + x2 + x3
            y = y1 + y2 + y3
            x = array(x)
            y = array(y)
            print(np.corrcoef(x, y))
            print(spearmanr(x, y))
            print(kendalltau(x, y))
            correlation = round(spearmanr(x, y)[0], 2)

            x1, y1 = create_array(regatta.get_results_normal_finals(), regatta.get_results_4())
            x = array(x1)
            y = array(y1)
            correlation1 = round(spearmanr(x, y)[0], 2)

            filew = year+str(k+1)+".txt"
            f = open(filew, "w")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_normal(), key="new")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_2(), key="new")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_3(), key="new")
            f.write("correlation = ")
            f.write(str(correlation))
            f.write("\n")
            f.write("\n")
            f.write("-" * 303)
            f.write("\n")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_4())
            f.write("correlation = ")
            f.write(str(correlation1))
            f.close()
        else:
            x1, y1 = create_array(regatta.get_results_normal(), regatta.get_results_newfinals_1())
            x2, y2 = create_array(regatta.get_results_normal(), regatta.get_results_newfinals_2())
            x3, y3 = create_array(regatta.get_results_normal(), regatta.get_results_newfinals_3())
            x = x1 + x2 + x3
            y = y1 + y2 + y3
            x = array(x)
            y = array(y)
            correlation = round(spearmanr(x, y)[0], 2)

            x4, y4 = create_array(regatta.get_results_normal(), regatta.get_results_oldfinals_1())
            x5, y5 = create_array(regatta.get_results_normal(), regatta.get_results_oldfinals_2())
            x6, y6 = create_array(regatta.get_results_normal(), regatta.get_results_oldfinals_3())
            x = x4 + x5 + x6
            y = y4 + y5 + y6
            x = array(x)
            y = array(y)
            correlation1 = round(spearmanr(x, y)[0], 2)

            filew = year + str(k + 1) + ".txt"
            f = open(filew, "w")
            write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_1(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_2(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_3(), key="old")
            f.write("correlation = ")
            f.write(str(correlation))
            f.write("\n")
            f.write("\n")
            f.write("-" * 303)
            f.write("\n")
            write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_1(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_2(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_3(), key="old")
            f.write("correlation = ")
            f.write(str(correlation1))
            f.close()

    season = Season(files)
    if int(year.replace("_", "")) > 2014:

        x1, y1 = create_array_season(season.get_results_finals(), season.get_results())
        x2, y2 = create_array_season(season.get_results_finals(), season.get_results_old1())
        x3, y3 = create_array_season(season.get_results_finals(), season.get_results_old2())
        x = x1 + x2 + x3
        y = y1 + y2 + y3
        x = array(x)
        y = array(y)
        correlation = round(spearmanr(x, y)[0], 2)

        x4, y4 = create_array_season(season.get_results_finals(), season.get_results_old3())
        x = array(x4)
        y = array(y4)
        correlation1 = round(spearmanr(x, y)[0], 2)

        filew = year + "conclusion" + ".txt"
        f = open(filew, "w")
        write_year(f, season.get_results_finals(), season.get_results(), files)
        write_year(f, season.get_results_finals(), season.get_results_old1(), files)
        write_year(f, season.get_results_finals(), season.get_results_old2(), files)
        f.write("correlation = ")
        f.write(str(correlation))
        f.write("\n")
        f.write("\n")
        f.write("-" * 303)
        f.write("\n")
        write_year(f, season.get_results_finals(), season.get_results_old3(), files)
        f.write("correlation = ")
        f.write(str(correlation1))
        f.close()
    else:
        x1, y1 = create_array_season(season.get_results(), season.get_results_new1())
        x2, y2 = create_array_season(season.get_results(), season.get_results_new2())
        x3, y3 = create_array_season(season.get_results(), season.get_results_new3())
        x = x1 + x2 + x3
        y = y1 + y2 + y3
        x = array(x)
        y = array(y)
        correlation = round(spearmanr(x, y)[0], 2)

        x1, y1 = create_array_season(season.get_results(), season.get_results_new4())
        x2, y2 = create_array_season(season.get_results(), season.get_results_new5())
        x3, y3 = create_array_season(season.get_results(), season.get_results_new6())
        x = x1 + x2 + x3
        y = y1 + y2 + y3
        x = array(x)
        y = array(y)
        correlation1 = round(spearmanr(x, y)[0], 2)

        filew = year + "conclusion" + ".txt"
        f = open(filew, "w")
        write_year(f, season.get_results(), season.get_results_new1(), files)
        write_year(f, season.get_results(), season.get_results_new2(), files)
        write_year(f, season.get_results(), season.get_results_new3(), files)
        f.write("correlation = ")
        f.write(str(correlation))
        f.write("\n")
        f.write("\n")
        f.write("-" * 303)
        f.write("\n")
        write_year(f, season.get_results(), season.get_results_new4(), files)
        write_year(f, season.get_results(), season.get_results_new5(), files)
        write_year(f, season.get_results(), season.get_results_new6(), files)
        f.write("correlation = ")
        f.write(str(correlation1))
        f.close()

