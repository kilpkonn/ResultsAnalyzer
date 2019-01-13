"""Examples."""
from results_analyzer import Analyzer
from season import Regatta, Season
from numpy import array
import numpy as np
from scipy.stats import spearmanr
from scipy.stats import pearsonr


def get_line(i, name, club, races, total, nett, separator: str, silver=None, gold=None, change=None, show_finals=False,
             display_stats=False):
    """Get line."""
    always = separator.join(["{0:3d}", "{1:<25s}", "{2:<10s}", "{3:>}"])
    total_net = separator.join(["{4:6}", "{5:5}"])
    finals = separator.join(["{6:>8s}", "{7:>4s}"])
    stats = separator + "{8:>7d}"
    line = always.format(i, name, club, separator.join([format(str(x), '>3') for x in races]))
    line += finals.format(silver, gold) if show_finals else ''
    line += total_net.format(total, nett)
    line += stats.format(change) if display_stats else ''
    return line


def get_line_syntax(races_count, separator, show_finals=False, display_stats=False):
    """Get syntax for line."""
    return get_line("Pos", "Name", "Club", separator.join([format("R" + str(x + 1), '>3') for x in range(races_count)]),
                    "Total", "Nett", separator, "Gold", "Silver", show_finals, display_stats)


def write_file(f, original, analyzed, key: str = "same"):
    changes = []
    correl = []
    chan = 0
    for i, sailor in enumerate(original):
        if not sailor.silver:
            silver = ""
        if sailor.silver:
            silver = str(sailor.silver)
        if not sailor.gold:
            gold = ""
        if sailor.gold:
            gold = str(sailor.gold)
        total = int(sailor.get_points_after(races=len(sailor.races)))
        nett = int(sailor.get_points_after(races=len(sailor.races), discount=1))
        races = '\t'.join([format(str(x), '>3') for x in sailor.races])
        races_syntax = '\t'.join([format("R" + str(x + 1), '>3') for x in range(len(sailor.races))])
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
        chan = chan + abs(change)
        if i == 2:
            changes.append(round(chan/(i+1), 2))
            x1, y1 = create_array(original, analyzed, i+1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 4:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 9:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 14:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 19:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])

        if key == "new":
            if i == 0:
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>6s}\t{7:>4s}".format(
                    "Pos", "Name", "Club", races_syntax, "Total", "Nett", "Silver", "Gold"))
                f.write("\t"+"|"+"\t")
                f.write("{0:>3s}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:>6s}\t{5:>5s}\t{6:>7s}".format(
                    "Pos", "Name", "Club", races_syntax_new, "Total", "Nett", "Change"))
                f.write("\n")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}".format(
                i + 1, sailor.name, sailor.club, races, total, nett, silver, gold))
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
                i + 1, sailor.name, sailor.club, races, total, nett))
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
                i + 1, sailor.name, sailor.club, races, total, nett, silver, gold))
            f.write("\t" + "|" + "\t")
            f.write("{0:3d}\t{1:<25s}\t{2:<10s}\t{3:>}\t{4:6}\t{5:5}\t{6:>6s}\t{7:>4s}\t{8:>7d}".format(
                i + 1, analyzed[i].name, analyzed[i].club, races_new, total_new, nett_new, silver_new, gold_new,
                change))
            f.write("\n")
    f.write("-" * 303)
    f.write("\n")
    for k, one in enumerate(correl):
        if k == 0:
            s = 3
        else:
            s = k + 4*k
        write_correl(f, one[0], one[1], s)
        f.write("\t")
        write_change(f, changes[k], s)
        f.write("\n")
    f.write("-"*303)
    f.write("\n")



def create_array(list1, list2, count):
    x = []
    y = []
    for i, line in enumerate(list1):
        x.append(i+1)
        for j, line2 in enumerate(list2):
            if line.name == line2.name:
                y.append(j+1)
        if i == count:
            break
    return x, y


def create_array_season(list1, list2, count):
    x = []
    y = []
    for i, line in enumerate(list1):
        x.append(i+1)
        for j, line2 in enumerate(list2):
            if line[0] == line2[0]:
                y.append(j+1)
        if i == count:
            break
    return x, y


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
    chan = 0
    changes = []
    correl = []
    for i, row in enumerate(original):
        for k in original:
            if converted[i][0] == k[0]:
                change = original.index(k) - i
                chan = chan + change
        if i == 2:
            changes.append(round(chan/(i+1), 2))
            x1, y1 = create_array_season(original, converted, i+1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 4:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 9:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 14:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 19:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i + 1)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
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
    for k, one in enumerate(correl):
        if k == 0:
            s = 3
        else:
            s = k + 4 * k
        write_correl(f, one[0], one[1], s)
        f.write("\t")
        write_change(f, changes[k], s)
        f.write("\n")
    f.write("-" * 303)
    f.write("\n")

def write_correl(fi, x, y, top):
    correl = round(pearsonr(x, y)[0], 2)
    li = "Correlation_"+str(top)+ " = "
    fi.write(li)
    fi.write(str(correl))

def write_change(f, change, top):
    li = "Medium_change_" + str(top) + " = "
    f.write(li)
    f.write(str(change))


if __name__ == "__main__":
    analyzer = Analyzer()
    year = "2014_"
    files = ["./example_data.csv", "./example_data_2.csv"]
    for k, file in enumerate(files):
        regatta = Regatta(file)
        analyzer.load_results(file)
        if analyzer.is_finals():


            filew = year+str(k+1)+".txt"
            f = open(filew, "w")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_normal(), key="new")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_2(), key="new")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_3(), key="new")
            write_file(f, regatta.get_results_normal_finals(), regatta.get_results_4())
            f.close()
        else:
            filew = year + str(k + 1) + ".txt"
            f = open(filew, "w")
            write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_1(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_2(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_3(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_1(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_2(), key="old")
            write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_3(), key="old")
            f.close()

    season = Season(files)
    if int(year.replace("_", "")) > 2014:

        filew = year + "conclusion" + ".txt"
        f = open(filew, "w")
        write_year(f, season.get_results_finals(), season.get_results(), files)
        write_year(f, season.get_results_finals(), season.get_results_old1(), files)
        write_year(f, season.get_results_finals(), season.get_results_old2(), files)
        write_year(f, season.get_results_finals(), season.get_results_old3(), files)
        f.close()
    else:

        filew = year + "conclusion" + ".txt"
        f = open(filew, "w")
        write_year(f, season.get_results(), season.get_results_new1(), files)
        write_year(f, season.get_results(), season.get_results_new2(), files)
        write_year(f, season.get_results(), season.get_results_new3(), files)
        write_year(f, season.get_results(), season.get_results_new4(), files)
        write_year(f, season.get_results(), season.get_results_new5(), files)
        write_year(f, season.get_results(), season.get_results_new6(), files)
        f.close()

