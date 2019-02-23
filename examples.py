"""Examples."""
from results_analyzer import Analyzer
from season import Regatta, Season
from grapher import draw_graph
import os
from numpy import array
from scipy.stats import pearsonr


def get_line(i, name, club, races, total, nett, separator = str, silver=None, gold=None, change=None, show_finals=False,
             display_stats=False):
    """Get line."""
    always = separator.join(["{0:>3}", "{1:<30}", "{2:<25}", "{3:>}"])
    total_net = separator.join(["", "{0:>6}", "{1:>5}"])
    finals = separator.join(["{0:>8}", "{1:>4}"])
    stats = separator + "{0:>7}"
    line = always.format(i, name, club, separator.join([format(str(x).replace('.0',''), '>4') for x in races]))
    line += total_net.format(str(total).replace('.0', ''), str(nett).replace('.0', ''))
    line += finals.format(str(silver), str(gold)) if show_finals else ''
    line += stats.format(change) if display_stats else ''
    return line.replace("None", ' ' * 4)


def get_line_syntax(races_count, separator, show_finals=False, display_stats=False):
    """Get syntax for line."""
    return get_line("Pos", "Name", "Club", [format("R" + str(x + 1), '>3') for x in range(races_count)],
                    "Total", "Nett", separator, "Silver", "Gold", "Change", show_finals, display_stats)


def write_file(f, original, analyzed, original_has_finals):
    changes = []
    correl = []
    chan = 0
    f.write(get_line_syntax(len(original[0].races), "\t", original_has_finals, False))
    f.write("\t | \t")
    f.write(get_line_syntax(len(analyzed[0].races), "\t", not original_has_finals, True))
    f.write("\n")
    for i, sailor in enumerate(original):
        for b in original:
            if analyzed[i].name == b.name:
                orig = original.index(b)
        change = orig - i
        for g in analyzed:
            if sailor.name == g.name:
                ch = i - analyzed.index(g)
        chan += abs(ch)
        f.write(get_line(i + 1, sailor.name, sailor.club, sailor.races, sailor.get_points_after(races = len(sailor.races)),
                         sailor.get_points_after(races = len(sailor.races), discount=1), "\t", sailor.silver, sailor.gold, change, original_has_finals, False))
        f.write("\t | \t")
        f.write(get_line(i + 1, analyzed[i].name, analyzed[i].club, analyzed[i].races, analyzed[i].get_points_after(races = len(analyzed[i].races)),
                         analyzed[i].get_points_after(races = len(analyzed[i].races), discount=1), "\t", analyzed[i].silver, analyzed[i].gold, change, not original_has_finals, True))
        f.write("\n")
        if i == 2:
            changes.append(round(chan/(i+1), 2))
            x1, y1 = create_array(original, analyzed, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        elif i == 4:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        elif i == 9:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        elif i == 14:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        elif i == 19:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array(original, analyzed, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])



    f.write("-" * 303)
    f.write("\n")
    for k, one in enumerate(correl):
        if k == 0:
            s = 3
        else:
            s = k + 4*k
        write_correl(f, one[0], one[1], s)
        f.write(format("\t", "4"))
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
            x1, y1 = create_array_season(original, converted, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 4:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 9:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 14:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i)
            x = array(x1)
            y = array(y1)
            correl.append([x, y])
        if i == 19:
            changes.append(round(chan / (i + 1), 2))
            x1, y1 = create_array_season(original, converted, i)
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
                                                                     converted[i][1][len(converted[i][1])-2], change))
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
    correl = int(pearsonr(x, y)[0]*100)/100
    li = "Correlation (top"+str(top)+ ") = \t"
    fi.write(format(li, "<22"))
    fi.write(format(str(correl), ">4"))

def write_change(f, change, top):
    li = "Medium change (top"+str(top)+ ") = \t"
    f.write(format(li, "<24"))
    f.write(format(str(change), ">4"))

def write_medium_correl(f, path, original, list1, list2, list3):
    x = []
    y = []
    n = -1
    for i, sailor in enumerate(original):
        x.append(i+1)
        a = 0
        b = 0
        for j, man in enumerate(list1):
            if sailor.name == man.name:
                a += j + 1
                b += 1
            if sailor.name == list2[j].name:
                a += j + 1
                b += 1
            if sailor.name == list3[j].name:
                a += j + 1
                b += 1
            if b == 3:
                break
        y.append(a/3)
        if i == 2 or 5 * n + 4 == i and i < 20:
            if i == 9:
                draw_graph(x, y, path)
            line = "Correlation all (top" + str(i+1) + ") =\t" + str(int(pearsonr(x, y)[0] * 100) / 100)
            f.write(line)
            f.write("\n")
            n += 1
    f.write("-"*303)
    f.write("\n")

def write_medium_correl_year(f, path, original, list1, list2, list3):
    x = []
    y = []
    n = -1
    for i, sailor in enumerate(original):
        x.append(i+1)
        a = 0
        b = 0
        for j, man in enumerate(list1):
            if sailor[0] == man[0]:
                a += j + 1
                b += 1
            if sailor[0] == list2[j][0]:
                a += j + 1
                b += 1
            if sailor[0] == list3[j][0]:
                a += j + 1
                b += 1
            if b == 3:
                break
        y.append(a/3)
        if i == 2 or 5 * n + 4 == i and i < 20:
            if i == 9:
                draw_graph(x, y, path)
            line = "Correlation all (top" + str(i+1) + ") =\t" + str(int(pearsonr(x, y)[0] * 100) / 100)
            f.write(line)
            f.write("\n")
            n += 1
    f.write("-"*303)
    f.write("\n")


def table_row(rang, a):
    return '{0:>4}\t{1:>}'.format(rang, "\t".join([format(str(x), '>5') for x in a]))

def table_syntax(a):
    return '{0:>4}\t{1:>}'.format("", "\t".join([format("M" + str(x+1), '>5') for x in range(len(a))]))

def write_table(f,original,list1,list2,list3,list4=None):
    n = -1
    a = []
    b = []
    c = []
    d = []
    e = []
    tablematrix = []
    for i, sailor in enumerate(original):
        a.append(i+1)
        end = 0
        for j, man in enumerate(list1):
            if sailor.name == man.name:
                end += 1
                b.append(j+1)
            if sailor.name == list2[j].name:
                end += 1
                c.append(j+1)
            if sailor.name == list3[j].name:
                end += 1
                d.append(j+1)
            if list4 and sailor.name == list4[j].name:
                end += 1
                e.append(j+1)
            if end == 4:
                break
        if i == 2 or 5 * n + 4 == i and i < 20:
            maybe = [int(pearsonr(a, b)[0] * 100) / 100, int(pearsonr(a, c)[0] * 100) / 100,
                     int(pearsonr(a, d)[0] * 100) / 100]
            full = maybe if not list4 else maybe + [int(pearsonr(a, e)[0] * 100) / 100]
            if i == 2:
                f.write(table_syntax(full))
                f.write("\n")
            f.write(table_row('1-' + str(i+1), full))
            f.write("\n")
            n += 1
            tablematrix.append(full)
    f.write("-"*303)
    f.write("\n")
    return tablematrix

def write_fulltable(f, matrix):
    for n in range(7):
        if n == 0:
            f.write(format('', '>2')+'\t')
            for num, race in enumerate(matrix):
                for k in range(len(race)):
                    if k == 0:
                        f.write(format(str(num + 1), '>4') + '\t')
                    else:
                        f.write(format("", '>4')+'\t')
            f.write("\n")
            f.write(format('', '>2') + '\t')
            for num, race in enumerate(matrix):
                for k in range(len(race)):
                    if k == 0:
                        f.write(format('1-3', '>4') + '\t')
                    else:
                        f.write(format('1-' + str(k * 5), '>4') + '\t')
            f.write("\n")
        if n < 4:
            f.write(format('M' + str(n + 1), '>2') + '\t')
        else:
            f.write(format('M' + str(n - 3), '>2') + '\t')
        for race in matrix:
            for k in range(len(race)):
                if len(race[0]) > 4 and n > 2:
                    if n == 3:
                        f.write(format("-", '>4') + '\t')
                    else:
                        f.write(format(race[k][n - 1], '>4') + '\t')
                elif len(race[0]) - 1 >= n:
                    f.write(format(race[k][n], '>4') + '\t')
                else:
                    f.write(format("-", '>4') + '\t')
        if n != 6:
            f.write("\n")


if __name__ == "__main__":
    analyzer = Analyzer()
    year_folders = [f.path for f in os.scandir("./Data/") if f.is_dir()]
    for folder in year_folders:
        class_folders = [f.path for f in os.scandir(folder) if f.is_dir()]
        for boat in class_folders:
            k = 0
            files = []
            yearmatrix = []
            for csvfile in os.listdir(boat):
                if csvfile.endswith(".csv"):
                    k += 1
                    file = os.path.join(boat, csvfile)
                    files.append(file)
                    regatta = Regatta(file)
                    analyzer.load_results(file)
                    picpath = boat + "/" + "Graph " + str(k)
                    if analyzer.is_finals():
                        filew = boat+ "/" +str(k)+".txt"
                        f = open(filew, "w")
                        write_file(f, regatta.get_results_normal_finals(), regatta.get_results_normal(), True)
                        write_file(f, regatta.get_results_normal_finals(), regatta.get_results_2(), True)
                        write_file(f, regatta.get_results_normal_finals(), regatta.get_results_3(), True)
                        write_medium_correl(f, picpath, regatta.get_results_normal_finals(), regatta.get_results_normal(),
                                            regatta.get_results_2(), regatta.get_results_3())
                        write_file(f, regatta.get_results_normal_finals(), regatta.get_results_4(), True)
                        compmatrix = write_table(f, regatta.get_results_normal_finals(), regatta.get_results_normal(),
                                            regatta.get_results_2(), regatta.get_results_3(), regatta.get_results_4())
                        f.close()
                    else:
                        filew = boat+ "/" +str(k) + ".txt"
                        picpath2 = boat + "/" + "Graph " + str(k) + ".1.png"
                        f = open(filew, "w")
                        write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_1(), False)
                        write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_2(), False)
                        write_file(f, regatta.get_results_normal(), regatta.get_results_newfinals_3(), False)
                        write_medium_correl(f, picpath, regatta.get_results_normal(), regatta.get_results_newfinals_1(),
                                            regatta.get_results_newfinals_2(), regatta.get_results_newfinals_3())
                        compmatrix = write_table(f, regatta.get_results_normal(), regatta.get_results_newfinals_1(),
                                    regatta.get_results_newfinals_2(), regatta.get_results_newfinals_3())
                        write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_1(), False)
                        write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_2(), False)
                        write_file(f, regatta.get_results_normal(), regatta.get_results_oldfinals_3(), False)
                        write_medium_correl(f, picpath2, regatta.get_results_normal(), regatta.get_results_oldfinals_1(),
                                            regatta.get_results_oldfinals_2(), regatta.get_results_oldfinals_3())
                        compmatrix1 = write_table(f, regatta.get_results_normal(), regatta.get_results_oldfinals_1(),
                                            regatta.get_results_oldfinals_2(), regatta.get_results_oldfinals_3())
                        f.close()
                        for g,com in enumerate(compmatrix):
                            com += compmatrix1[g]
                    yearmatrix.append(compmatrix)
            season = Season(files)
            ypicpath = boat + "/" + "Year Graph"
            if int(folder.replace(os.curdir + "/Data/", "")) > 2014:
                filew = boat+ "/conclusion" + ".txt"
                f = open(filew, "w")
                write_year(f, season.get_results_finals(), season.get_results(), files)
                write_year(f, season.get_results_finals(), season.get_results_old1(), files)
                write_year(f, season.get_results_finals(), season.get_results_old2(), files)
                write_medium_correl_year(f, ypicpath, season.get_results_finals(), season.get_results(), season.get_results_old1(), season.get_results_old2())
                write_year(f, season.get_results_finals(), season.get_results_old3(), files)
                f.close()
            else:
                filew = boat+ "/conclusion" + ".txt"
                ypicpath2 = boat + "/" + "Year Graph 1"
                f = open(filew, "w")
                write_year(f, season.get_results(), season.get_results_new1(), files)
                write_year(f, season.get_results(), season.get_results_new2(), files)
                write_year(f, season.get_results(), season.get_results_new3(), files)
                write_medium_correl_year(f, ypicpath, season.get_results(), season.get_results_new1(), season.get_results_new2(), season.get_results_new3())
                write_year(f, season.get_results(), season.get_results_new4(), files)
                write_year(f, season.get_results(), season.get_results_new5(), files)
                write_year(f, season.get_results(), season.get_results_new6(), files)
                write_medium_correl_year(f, ypicpath2, season.get_results(), season.get_results_new4(), season.get_results_new5(),
                                         season.get_results_new6())
                f.close()
            ofile = boat + "/Correl table.txt"
            with open(ofile, "w") as f:
                write_fulltable(f, yearmatrix)