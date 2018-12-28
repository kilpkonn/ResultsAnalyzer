"""Results analyzer."""


class Place(object):
    """Place obj."""

    def __init__(self, points: int, symbol: str):
        """Init."""
        self.points = points
        self.symbol = symbol

    def __repr__(self):
        """Repr."""
        return self.symbol


class Sailor:
    """Sailor"""

    def __init__(self, name: str, sail_nr: str, gender: str, sub_categories: list, nationality: str, races: list,
                 club: str):
        """Init."""
        self.name = name
        self.sail_nr = sail_nr
        self.gender = gender
        self.sub_categories = sub_categories
        self.nationality = nationality
        self.races = races
        self.club = club

    @property
    def total_points(self):
        """Get total points."""
        return sum(x.points for x in self.races)

    def get_points_after(self, races: int, discount: int = 0):
        """Get points after x races."""
        points_to_discount = sum(sorted([x.points for x in self.races[:races]], reverse=True)[:discount])
        return sum([x.points for x in self.races[:races]]) - points_to_discount

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
            lines = csv.reader(f, delimiter=",")
            for i, line in enumerate(lines):
                if i == 0:
                    self.try_get_syntax(line)
                    continue

                obj = self.get_clean_data(line)
                self.data.append(obj)

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
            elif (n.lower().startswith('r') and n[1:].isdigit()) or n.lower().isdigit():
                syntax.append("race")
            else:
                syntax.append("null")
        self.syntax = syntax
        if data:
            return True
        return False

    def get_clean_data(self, line) -> Sailor:
        """Get clean data."""
        name = ''
        sail_nr = None
        gender = None
        sub_cats = None
        nat = None
        races = None
        club = ''
        for i, node in enumerate(line):
            if self.syntax[i] == "name":
                name += node
            elif self.syntax[i] == "sail_nr":
                sail_nr = node
            elif self.syntax[i] == "club":
                club += node
            elif self.syntax[i] == "nat":
                nat = node
            elif self.syntax[i] == "gender":
                gender = node
            elif "sub_cat" in self.syntax[i]:
                if node == "":
                    sub_cats = []
                sub_cats.append(self.syntax[i].replace("sub_cat_", ""))
            if self.syntax[i] == "race":
                node = node.replace('(', '').replace(')', '').replace('[', '').replace(']', '').strip()
                if not races:
                    races = []
                if '/' in node:
                    pos = int(node.split('/')[0].replace(".0", ""))
                    sym = node.split('/')[1]
                else:
                    pos = int(node.replace(".0", ""))
                    sym = str(pos)
                races.append(Place(pos, sym))
        return Sailor(name.strip(), sail_nr, gender, sub_cats, nat, races, club.strip())

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
        return sorted(self.data, key=lambda x: x.get_points_after(races, discount))
