"""Results analyzer."""
import statistics


class Place(object):
    """Place obj."""

    def __init__(self, points: int, symbol: str):
        """Init."""
        self.points = points
        self.symbol = symbol

    def __le__(self, other):
        """Le."""
        if isinstance(other, Place):
            return other.points < self.points
        else:
            raise ValueError(f"Cannot compare {type(other)} and Place!")

    def __ge__(self, other):
        """Ge."""
        if isinstance(other, Place):
            return other.points > self.points
        else:
            raise ValueError(f"Cannot compare {type(other)} and Place!")

    def __add__(self, other):
        """Add."""
        if isinstance(other, Place):
            return Place(self.points + other.points, str(self.points + other.points))
        elif isinstance(other, int):
            return Place(self.points + other, str(self.points + other))
        else:
            raise ValueError("Invalid value for adding to place.")

    def __repr__(self):
        """Repr."""
        return self.symbol


class Sailor:
    """Sailor"""

    def __init__(self, name: str, sail_nr: str, gender: str, sub_categories: list, nationality: str, races: list,
                 club: str, silver: int = None, gold: int = None):
        """Init."""
        self.name = name
        self.sail_nr = sail_nr
        self.gender = gender
        self.sub_categories = sub_categories
        self.nationality = nationality
        self.races = races
        self.club = club
        self.silver = silver
        self.gold = gold

    @property
    def total_points(self) -> int:
        """Get total points."""
        return sum(x.points for x in self.races)

    @property
    def std_dev(self) -> float:
        """Get standard deviation."""
        return statistics.stdev([x.points for x in self.races])

    @property
    def best_race(self) -> Place:
        """Get place in best race."""
        return min(self.races, key=lambda x: x.points)

    def avg_place(self, discount: int = 0) -> float:
        """Get average place"""
        return self.get_points_after(len(self.races), discount) / (len(self.races) - discount)

    def get_worst_race(self, discount: int = 0) -> Place:
        """Get place in worst race"""
        discounted = sorted(self.races, key=lambda x: x.points, reverse=True)[:discount]
        return max([x for x in self.races if x not in discounted], key=lambda x: x.points)

    def get_points_after(self, races: int, discount: int = 0, calc_extras: bool = False) -> int:
        """Get points after x races."""
        points_to_discount = sum(sorted([x.points for x in self.races[:races]], reverse=True)[:discount])
        extra = sum([(i + 1) * x.points * 10**-6 for i, x in enumerate(sorted(self.races, key=lambda x: x.points))])
        extra += sum([(i + 1)**7 * x.points * 10**-9 for i, x in enumerate(self.races)]) if calc_extras else 0
        return sum([x.points for x in self.races[:races]]) + extra - points_to_discount

    def __repr__(self):
        """Repr."""
        return f"Name: {self.name}, club: {self.club}, sail nr: {self.sail_nr}, races: {self.races}, " + \
            f"points: {self.total_points}"


class Analyzer:
    """Results Analyzer."""

    def __init__(self):
        """Init."""
        self.data = None
        self.syntax = None
        self.special_codes = ["dne", "ocs", "ufd", "bfd", "dsq", "ret", "dnc", "dns"]

    def load_results(self, file_name: str):
        """Load results from file."""
        import csv
        self.data = []
        with open(file_name, 'r') as f:
            lines = csv.reader(f, delimiter=',')
            for i, line in enumerate(lines):
                if i == 0:
                    self.try_get_syntax(line)
                    continue

                obj = self.get_clean_data(line)
                self.data.append(obj)

    def import_data(self, data: list):
        """Import races."""
        if isinstance(data, list) and isinstance(data[0], Sailor):
            self.data = data
        else:
            raise ValueError("Invalid data type for importing, must be list[Sailor]!")

    def try_get_syntax(self, data) -> bool:
        syntax = []
        for n in data:
            if n.lower() in ["sailno", "sailnr", "sail"]:
                syntax.append("sail_nr")
            elif n.lower() in ["club", "klubi"]:
                syntax.append("club")
            elif n.lower() in ["helmname", "name", "skipper"]:
                syntax.append("name")
            elif n.lower() in ["gender", "sugu"]:
                syntax.append("gender")
            elif n.lower() in ["nat", "nationality"]:
                syntax.append("nat")
            elif n.lower() in ["u21", "junior", "u19"]:
                syntax.append(f"sub_cat_{n}")  # something better here
            elif ((n.lower().startswith('r') or n.lower().startswith('q')) and n[1:].isdigit()) or n.lower().isdigit():
                syntax.append("race")
            elif n.lower() in ["silver", "poolfinaal", "hõbe", "hõbefinaal"]:
                syntax.append("silver")
            elif n.lower() in ["gold", "finaal", "kuldfinaal", "kuld"]:
                syntax.append("gold")
            else:
                syntax.append("null")
        self.syntax = syntax
        if data:
            return True
        return False

    def get_clean_data(self, line) -> Sailor:
        """Get clean data."""
        name = None
        sail_nr = None
        gender = None
        sub_cats = []
        nat = None
        races = []
        club = ''
        silver = None
        gold = None
        for i, node in enumerate(line):
            if self.syntax[i] == "name":
                name = node
            elif self.syntax[i] == "sail_nr":
                sail_nr = node
            elif self.syntax[i] == "club":
                club += node
            elif self.syntax[i] == "nat":
                nat = node
            elif self.syntax[i] == "gender":
                gender = node
            elif "sub_cat" in self.syntax[i]:
                sub_cats.append(self.syntax[i].replace("sub_cat_", ""))
            elif self.syntax[i] == "race":
                node = node.replace('(', '').replace(')', '').replace('[', '').replace(']', '').strip()
                if '/' in node:
                    pos = int(node.split('/')[0].replace('.0', ''))
                    sym = node.split('/')[1]
                elif ' ' in node:
                    pos = int(node.split(' ')[0].replace('.0', ''))
                    sym = node.split(' ')[1]
                else:
                    pos = int(node.replace('.0', ''))
                    sym = str(pos)
                races.append(Place(pos, sym))
            elif self.syntax[i] == "silver":
                silver = node
            elif self.syntax[i] == "gold":
                gold = node

        return Sailor(name.strip(), sail_nr, gender, sub_cats, nat, races, club.strip(), silver, gold)

    def get_competitors(self) -> list:
        """Get competitors"""
        return self.data.copy()

    def get_results(self, discount: int = 0, races: int = None) -> list:
        """Get results"""
        if not races:
            races = len(self.data[0].races)
        elif races < 1:
            while races < 1:
                races += len(self.data[0].races)

        if races <= discount or discount < 0:
            raise ValueError("You cannot discount all races nor negative amount of races!")
        results = sorted(self.data, key=lambda x: x.get_points_after(races, discount, True))
        for n in results:
            n.races = n.races[:races]
        return results
