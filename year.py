from results_analyzer import Analyzer
from results_analyzer import Place

class Participant:
    def __init__(self, name: str, points: int, extra: int):
        self.name = name
        self.points = points
        self.extra = extra


class Competition:
    def __init__(self, number: int, points: int, extra: int):
        self.number = number
        self.points = points
        self.extra = extra
        self.total = self.points + self.extra


class Regatta:
    def __init__(self, data_path: str):
        self.analyzer = Analyzer()
        self.analyzer.load_results(data_path)

    def get_real_places(self, list_1):
        results = list_1
        for n, i in enumerate(results[:4]):
            i.silver = None
            i.gold = Place(n + 1, str(n + 1))
        for n, i in enumerate(results[3:10]):
            if n == 0:
                i.silver = Place(n + 1, str(n + 1))
            else:
                i.gold = None
                i.silver = Place(n + 1, str(n + 1))
        return results

    def get_results_normal(self):
        return self.analyzer.get_results(discount=1)

    def get_results_normal_finals(self):
        return self.analyzer.get_results_final_gold(discount=1)

    def get_results_2(self):
        new = self.analyzer.get_competitors()
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
        return new_analyzer.get_results(discount=1)

    def get_results_3(self):
        new_2 = self.analyzer.get_competitors()
        for i in new_2:
            if not i.silver and not i.gold:
                i.races.append(i.races[len(i.races) - 2])
                i.races.append(i.races[len(i.races) - 2])
            elif i.silver and i.gold:
                i.races.append(i.silver)
                i.races.append(i.gold)
            elif i.gold and not i.silver:
                i.races.append(i.races[len(i.races) - 2])
                i.races.append(i.gold)
            elif i.silver and not i.gold:
                i.races.append(i.silver)
                i.races.append(i.races[len(i.races) - 2])

        new_analyzer_2 = Analyzer()
        new_analyzer_2.import_data(new_2)
        return new_analyzer_2.get_results(discount=1)

    def get_results_4(self):
        return self.analyzer.get_results_final(discount=1)

    def convert_finals(self):
        new_3_data = self.analyzer.get_competitors()
        new_analyzer_3 = Analyzer()
        new_analyzer_3.import_data(new_3_data)
        new_3 = new_analyzer_3.get_results(discount=1)
        for i in new_3[:10]:
            i.silver = i.races[len(i.races) - 2]
            i.gold = i.races[len(i.races) - 1]
        return new_3

    def convert_finals_2(self):
        new_4_data = self.analyzer.get_competitors()
        new_analyzer_4 = Analyzer()
        new_analyzer_4.import_data(new_4_data)
        new_4 = new_analyzer_4.get_results(discount=1, races=-2)
        for i in new_4[:10]:
            i.silver = i.races[len(i.races) - 2]
            i.gold = i.races[len(i.races) - 1]
        return new_4

    def convert_finals_3(self):
        new_5_data = self.analyzer.get_competitors()
        new_analyzer_5 = Analyzer()
        new_analyzer_5.import_data(new_5_data)
        new_5 = new_analyzer_5.get_results(discount=1, races=-1)
        for i in new_5[:10]:
            i.silver = i.races[len(i.races) - 1]
            i.gold = i.races[len(i.races) - 1]
        return new_5

    def get_results_newfinals_1(self):
        new_3 = self.convert_finals()
        new_analyzer_3 = Analyzer()
        new_analyzer_3.import_data(new_3)
        results = new_analyzer_3.get_results_final_gold(discount=1)
        return results

    def get_results_oldfinals_1(self):
        new_3 = self.convert_finals()
        new_analyzer_3 = Analyzer()
        new_analyzer_3.import_data(new_3)
        results = new_analyzer_3.get_results_final(discount=1)
        results = self.get_real_places(results)
        return results

    def get_results_newfinals_2(self):
        new_4 = self.convert_finals_2()
        new_analyzer_4 = Analyzer()
        new_analyzer_4.import_data(new_4)
        results = new_analyzer_4.get_results_final_gold(discount=1, races=-2)
        return results

    def get_results_oldfinals_2(self):
        new_4 = self.convert_finals_2()
        new_analyzer_4 = Analyzer()
        new_analyzer_4.import_data(new_4)
        results = new_analyzer_4.get_results_final(discount=1, races=-2)
        return results

    def get_results_newfinals_3(self):
        new_5 = self.convert_finals_3()
        new_analyzer_5 = Analyzer()
        new_analyzer_5.import_data(new_5)
        results = new_analyzer_5.get_results_final_gold(discount=1, races=-1)
        return results

    def get_results_oldfinals_3(self):
        new_5 = self.convert_finals_3()
        new_analyzer_5 = Analyzer()
        new_analyzer_5.import_data(new_5)
        results = new_analyzer_5.get_results_final(discount=1, races=-1)
        return results



class Season:

    def __init__(self, regattas):
        self.regattas = regattas

    def sort_year(self, dic):
        for i in dic:
            total = 0
            for j in dic[i]:
                total = total + j.total
            extra = sum([(i + 1) ** -1 * x.total * 10 ** -3 for i, x in enumerate(sorted(dic[i], key=lambda x: x.total))])
            extra += sum([(i + 1) ** 7 * x.total * 10 ** -15 for i, x in enumerate(dic[i])])
            dic[i].append(total)
            dic[i].append(extra)
        return sorted(dic.items(), key=lambda x: x[1][len(x[1]) - 1], reverse=True)

    def get_results(self):
        results = {}
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            for i, sailor in enumerate(newregatta.get_results_normal()):
                if i < 3:
                    extra = 3-i
                else:
                    extra = 0
                if sailor.name not in results:
                    results[sailor.name] = [Competition(n+1, 50-i, extra)]
                else:
                    results[sailor.name].append(Competition(n+1, 50-i, extra))
        return self.sort_year(results)

    def get_results_finals(self):
        results = {}
        analyzer = Analyzer()
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            analyzer.load_results(regatta)
            if analyzer.is_finals():
                for i, sailor in enumerate(newregatta.get_results_normal_finals()):
                    for j, man in enumerate(newregatta.get_results_normal()):
                        if sailor.name == man.name:
                            if j < 3:
                                extra = 3 - i
                            else:
                                extra = 0
                            break
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))
            else:
                for i, sailor in enumerate(newregatta.get_results_normal()):
                    if i < 3:
                        extra = 3 - i
                    else:
                        extra = 0
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_old1(self):
        results = {}
        analyzer = Analyzer()
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            analyzer.load_results(regatta)
            if analyzer.is_finals():
                for i, sailor in enumerate(newregatta.get_results_2()):
                    for j, man in enumerate(newregatta.get_results_normal()):
                        if sailor.name == man.name:
                            if j < 3:
                                extra = 3 - i
                            else:
                                extra = 0
                            break
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))
            else:
                for i, sailor in enumerate(newregatta.get_results_normal()):
                    if i < 3:
                        extra = 3 - i
                    else:
                        extra = 0
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))

        return self.sort_year(results)

    def get_results_old2(self):
        results = {}
        analyzer = Analyzer()
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            analyzer.load_results(regatta)
            if analyzer.is_finals():
                for i, sailor in enumerate(newregatta.get_results_3()):
                    for j, man in enumerate(newregatta.get_results_normal()):
                        if sailor.name == man.name:
                            if j < 3:
                                extra = 3 - i
                            else:
                                extra = 0
                            break
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))
            else:
                for i, sailor in enumerate(newregatta.get_results_normal()):
                    if i < 3:
                        extra = 3 - i
                    else:
                        extra = 0
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_old3(self):
        results = {}
        analyzer = Analyzer()
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            analyzer.load_results(regatta)
            if analyzer.is_finals():
                for i, sailor in enumerate(newregatta.get_results_4()):
                    for j, man in enumerate(newregatta.get_results_normal()):
                        if sailor.name == man.name:
                            if j < 3:
                                extra = 3 - i
                            else:
                                extra = 0
                            break
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))
            else:
                for i, sailor in enumerate(newregatta.get_results_normal()):
                    if i < 3:
                        extra = 3 - i
                    else:
                        extra = 0
                    if sailor.name not in results:
                        results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                    else:
                        results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_new1(self):
        results = {}
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            for i, sailor in enumerate(newregatta.get_results_newfinals_1()):
                for j, man in enumerate(newregatta.get_results_normal()):
                    if sailor.name == man.name:
                        if j < 3:
                            extra = 3 - i
                        else:
                            extra = 0
                        break
                if sailor.name not in results:
                    results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                else:
                    results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_new2(self):
        results = {}
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            for i, sailor in enumerate(newregatta.get_results_newfinals_2()):
                for j, man in enumerate(newregatta.get_results_normal()):
                    if sailor.name == man.name:
                        if j < 3:
                            extra = 3 - i
                        else:
                            extra = 0
                        break
                if sailor.name not in results:
                    results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                else:
                    results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_new3(self):
        results = {}
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            for i, sailor in enumerate(newregatta.get_results_newfinals_3()):
                for j, man in enumerate(newregatta.get_results_normal()):
                    if sailor.name == man.name:
                        if j < 3:
                            extra = 3 - i
                        else:
                            extra = 0
                        break
                if sailor.name not in results:
                    results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                else:
                    results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_new4(self):
        results = {}
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            for i, sailor in enumerate(newregatta.get_results_oldfinals_1()):
                for j, man in enumerate(newregatta.get_results_normal()):
                    if sailor.name == man.name:
                        if j < 3:
                            extra = 3 - i
                        else:
                            extra = 0
                        break
                if sailor.name not in results:
                    results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                else:
                    results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_new5(self):
        results = {}
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            for i, sailor in enumerate(newregatta.get_results_oldfinals_2()):
                for j, man in enumerate(newregatta.get_results_normal()):
                    if sailor.name == man.name:
                        if j < 3:
                            extra = 3 - i
                        else:
                            extra = 0
                        break
                if sailor.name not in results:
                    results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                else:
                    results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)

    def get_results_new6(self):
        results = {}
        for n, regatta in enumerate(self.regattas):
            newregatta = Regatta(regatta)
            for i, sailor in enumerate(newregatta.get_results_oldfinals_3()):
                for j, man in enumerate(newregatta.get_results_normal()):
                    if sailor.name == man.name:
                        if j < 3:
                            extra = 3 - i
                        else:
                            extra = 0
                        break
                if sailor.name not in results:
                    results[sailor.name] = [Competition(n + 1, 50 - i, extra)]
                else:
                    results[sailor.name].append(Competition(n + 1, 50 - i, extra))
        return self.sort_year(results)
