import json
import random


def _is_wovel(char):
    return char.lower() in {'а', 'е', 'и', 'й', 'о', 'э', 'ю', 'я', 'ь', 'ы', 'у'}


def _wovel_count(name):
    number = 0
    for c in name:
        if _is_wovel(c):
            number += 1
    return number


def _is_soft(char):
    return char.lower() in {'е', 'и', 'й', 'о', 'э', 'ю', 'я', 'ь', 'с', 'л', 'н'}


class Names(object):
    def __init__(self, names_all_json, names_json, nicknames_json):
        """ Класс для генерации имён """

        # 1. Флаг отладки
        self.output_debug_info = False

        # 2. Парсим файлы с данными
        self.minorities = json.load(names_all_json)
        self.defnames = json.load(names_json)
        self.nicknames = json.loads(''.join([line for line in nicknames_json.readlines() if not line.startswith('/')]))
        self.nicknames_fullset = self.nicknames.copy()

    def new(self):
        """ Генерируем новое имя """

        def_first_names = []

        # строим список имен выбирая их из полного списка
        for name in self.defnames:
            if name.get("fl_name", False) and not name.get("fl_obsolete", False):
                def_first_names.append(name)

        minority_roll = random.randrange(100)
        i_ethno = 0
        for ethno in self.minorities:
            minority_roll -= ethno["chance"]
            if minority_roll >= 0:
                i_ethno += 1
            else:
                break

        if self.output_debug_info:
            print(f'ethno={i_ethno} ', end="")

        if i_ethno < len(self.minorities):
            if (random.randrange(2) != 0 or "names" not in self.minorities[i_ethno] or len(
                    self.minorities[i_ethno]["names"]) == 0):
                name = self._pick_a_name(def_first_names)
            else:
                name = random.choice(self.minorities[i_ethno]["names"])
            nick = self._pick_a_nick()
            return f'{name} {random.choice(self.minorities[i_ethno]["surnames"])} «{nick}»'

        # print(random.choice(def_first_names), end = " ")

        selname = random.choice(self.defnames)
        name = selname["base"]

        if self.output_debug_info:
            print(f'[base={name}] ', end="")

        f_ets = False
        f_whizzle = False
        if random.randrange(8) == 0 and not selname.get("fl_noets", False):  # добавить -ец
            if not selname["base"].endswith("ец") and not selname["nullpostfix"].endswith(
                    "ец") and not name.endswith(
                    "к") and not name.endswith("ч"):
                name += selname["postfix"]

                if name[-1] == 'ь':
                    name = name[:-1]
                elif name[-1] in {'ц', 'к'}:
                    name = name[:-1] + 'ч'
                elif name[-1] == 'х':
                    name = name[:-1] + 'ш'
                elif name[-1] == 'г':
                    name = name[:-1] + 'ж'

                if name[-1] == 'ч':
                    if name[-2] in {'с', 'ш'}:
                        name = name[:-2] + 'щ'
                    elif name[-2] in {'т', 'ц', 'ч'}:
                        name = name[:-2] + 'ч'

                name += "ец"
                f_ets = True

        if self.output_debug_info and f_ets:
            print('ets ', end="")

        i_postfix = random.randrange(8)

        if i_postfix == 0 and (not selname.get("fl_name", False) or f_ets):  # оригинальная форма фамилии, не имя
            if not f_ets:
                name += selname["nullpostfix"]
        else:
            if f_ets:
                if _is_wovel(name[-3]) and name[-2] == 'е':
                    name = name[:-2] + 'й' + name[-1]  # -еец => -ейц
                elif _wovel_count(selname["base"]) > 1:
                    if name[-3] in {'ч', 'ш', 'щ', 'ж'}:
                        f_whizzle = True
                    elif name[-3] == 'л':
                        name = name[:-2] + 'ь' + name[-1]
                    elif name[-3] == 'с':
                        name = name[:-3] + 'щ'
                    else:
                        name = name[:-2] + name[-1]
                else:
                    f_whizzle = True

            if i_postfix <= 5:  # ов/ев/ин + ич
                if f_ets:
                    name += "ов" if f_whizzle else "ев"
                else:
                    name += selname["postfix"]
                    if selname["gender"] != 0:
                        lc = selname["nullpostfix"][-1] if len(selname["nullpostfix"]) > 0 else ''
                        if (name[-1] == 'й' or name[
                            -1] == 'ь' or lc == 'й' or lc == 'ц' or lc == 'ь') and not selname.get(
                                "fl_adjective", False):
                            name += "ев"
                        else:
                            name += "ов"
                    else:
                        name += "ин"

                roll = random.randrange(16)
                if roll == 2:  # -ич
                    if name[-3] in {'ж', 'ц', 'ш', 'щ'}:
                        name = name[:-2] + "ев"
                        if name[-2] == 'и':
                            name = name[:-2]
                        name += "ич"
                elif roll == 3:
                    name += "ский"
                elif roll == 4:
                    name += "ских"
                elif roll == 5:
                    if random.randrange(2) != 0:  # уполовиниваем щанс
                        name += "ых"
            elif i_postfix <= 7:  # -енко/ченко/енков/ченков  -ук/юк/ик
                name += selname["postfix"]

                if name[-1] in {'к', 'ц'}:
                    if name[-2] == 'ш' or name[-2] == 'щ' or name[-2] == 'ч':
                        name = name[:-1]
                    else:
                        name = name[:-1] + 'ч'
                elif name[-1] == 'x':
                    name = name[:-1] + 'ш'
                elif name[-1] == 'г':
                    name = name[:-1] + 'ж'
                elif name[-1] == 'н':
                    if random.randrange(2) != 0:  # уполовиниваем щанс
                        name += 'ч'

                if random.randrange(2) != 0:
                    name += "енко"
                    if random.randrange(3) == 0:  # -в
                        name += 'в'
                else:
                    if random.randrange(4) == 0:
                        name += "ик"
                    else:
                        if not f_ets and _is_soft(name[-1]):
                            name += "юк"
                        else:
                            name += "ук"

        # прозвище
        if selname.get("fl_nick", False) and random.randrange(
                4) == 0:  # если фамилия может быть базой прозвища, то с вероятностью 25% используем её
            nick = self._pick_a_nick(selname["base"] + selname["nullpostfix"])
        else:
            nick = self._pick_a_nick()

        return f'{self._pick_a_name(def_first_names)} {name} «{nick}»'

    def _pick_a_nick(self, nick=None):

        if nick is None:
            if len(self.nicknames) == 0:
                self.nicknames = self.nicknames_fullset.copy()
            nick = random.choice(self.nicknames)

        if nick in self.nicknames:
            self.nicknames.remove(nick)

        return nick

    @staticmethod
    def _pick_a_name(def_first_names):
        if len(def_first_names) == 0:
            return ""

        name = random.choice(def_first_names)
        if ("alt_names" in name) and random.randrange(
                4) == 0:  # если есть альтернативные формы имени, то выбираем их с шансом 25%
            return random.choice(name["alt_names"])

        return name["base"] + name["nullpostfix"]


if __name__ == '__main__':

    # Открываем файлы с данными
    names_all_json_ = open("names_all.json", "r", encoding="utf-8")
    names_json_ = open("names.json", "r", encoding="utf-8")
    nicknames_json_ = open("nicknames.json", "r", encoding="utf-8")

    # Создаём экземпляр класса
    names = Names(names_all_json_, names_json_, nicknames_json_)

    # Генерируем имена в цикле для отладки
    s = None
    while not s:
        s = input(names.new())
