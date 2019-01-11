from results_analyzer import Analyzer
from results_analyzer import Place


class Participant:
    """Participant."""

    def __init__(self, name: str, points: int, extra: int):
        """Init."""
        self.name = name
        self.points = points
        self.extra = extra


class Competition:
    """Competition."""

    def __init__(self, number: int, points: int, extra: int):
        """Init."""
        self.number = number
        self.points = points
        self.extra = extra
        self.total = self.points + self.extra


class Regatta:
    """Regatta."""

    def __init__(self, data_path: str):
        """Init."""
        self.analyzer = Analyzer()
        self.analyzer.load_results(data_path)

    def get_real_places(self, list_1):
        """Get real places"""
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
        """Get normal results."""
        return self.analyzer.get_results(discount=1)

    def get_results_normal_finals(self):
        """Get normal results with finals."""
        return self.analyzer.get_results_final_gold(discount=1)

    def get_results_2(self):
        """Get results 2."""
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
        """Get results 3."""
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
        """Get results 4."""
        return self.analyzer.get_results_final(discount=1)

    def convert_finals(self):
        """Convert finals."""
        new_3_data = self.analyzer.get_competitors()
        new_analyzer_3 = Analyzer()
        new_analyzer_3.import_data(new_3_data)
        new_3 = new_analyzer_3.get_results(discount=1)
        for i in new_3[:10]:
            i.silver = i.races[len(i.races) - 2]
            i.gold = i.races[len(i.races) - 1]
        return new_3

    def convert_finals_2(self):
        """Convert finals 2."""
        new_4_data = self.analyzer.get_competitors()
        new_analyzer_4 = Analyzer()
        new_analyzer_4.import_data(new_4_data)
        new_4 = new_analyzer_4.get_results(discount=1, races=-2)
        for i in new_4[:10]:
            i.silver = i.races[len(i.races) - 2]
            i.gold = i.races[len(i.races) - 1]
        return new_4

    def convert_finals_3(self):
        """Convert finals 3."""
        new_5_data = self.analyzer.get_competitors()
        new_analyzer_5 = Analyzer()
        new_analyzer_5.import_data(new_5_data)
        new_5 = new_analyzer_5.get_results(discount=1, races=-1)
        for i in new_5[:10]:
            i.silver = i.races[len(i.races) - 1]
            i.gold = i.races[len(i.races) - 1]
        return new_5

    def get_results_newfinals_1(self):
        """Get results with new finals."""
        new_3 = self.convert_finals()
        new_analyzer_3 = Analyzer()
        new_analyzer_3.import_data(new_3)
        results = new_analyzer_3.get_results_final_gold(discount=1)
        return results

    def get_results_oldfinals_1(self):
        """Get results with old finals."""
        new_3 = self.convert_finals()
        new_analyzer_3 = Analyzer()
        new_analyzer_3.import_data(new_3)
        results = new_analyzer_3.get_results_final(discount=1)
        results = self.get_real_places(results)
        return results

    def get_results_newfinals_2(self):
        """Get results with new finals 2."""
        new_4 = self.convert_finals_2()
        new_analyzer_4 = Analyzer()
        new_analyzer_4.import_data(new_4)
        results = new_analyzer_4.get_results_final_gold(discount=1, races=-2)
        return results

    def get_results_oldfinals_2(self):
        """Get results with old finals 2."""
        new_4 = self.convert_finals_2()
        new_analyzer_4 = Analyzer()
        new_analyzer_4.import_data(new_4)
        results = new_analyzer_4.get_results_final(discount=1, races=-2)
        return results

    def get_results_newfinals_3(self):
        """Get results with new finals 3."""
        new_5 = self.convert_finals_3()
        new_analyzer_5 = Analyzer()
        new_analyzer_5.import_data(new_5)
        results = new_analyzer_5.get_results_final_gold(discount=1, races=-1)
        return results

    def get_results_oldfinals_3(self):
        """Get results with old finals 3."""
        new_5 = self.convert_finals_3()
        new_analyzer_5 = Analyzer()
        new_analyzer_5.import_data(new_5)
        results = new_analyzer_5.get_results_final(discount=1, races=-1)
        return results


class Season:
    """Season"""

    def __init__(self, regattas):
        """Init."""
        self.regattas = regattas

    def sort_year(self, dic):
        """Sort year."""
        for i in dic:
            total = 0
            for j in dic[i]:
                total = total + j.total
            extra = sum([(i + 1) ** -1 * x.total * 10 ** -3 for i, x in
                         enumerate(sorted(dic[i], key=lambda x: x.total))])
            extra += sum([(i + 1) ** 7 * x.total * 10 ** -15 for i, x in enumerate(dic[i])])
            dic[i].append(total)
            dic[i].append(extra)
        return sorted(dic.items(), key=lambda x: x[1][len(x[1]) - 1], reverse=True)

    def get_results(self):
        """Get results."""
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
        """Get results with finals."""
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
        """Get results old."""
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
        """Get results old 2."""
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
        """Get results old 3."""
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
        """Get results new."""
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
        """Get results new 2."""
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
        """Get results new 3."""
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
        """Get results new 4."""
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
        """Get results new 5."""
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
        """Get results new 6."""
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
