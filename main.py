# Pokemon Battle Tree Team Type Synergy Calculator GUI with Kivy aka "PokeTeamCalc" app script
# Input a single pokemon type combo and get best possible 2 ally pokemon with fewest weaknesses and un-resists.
# v1.3.3  Add all typing rows from the start, allow for teams of 6, ability to hide rows instead of remove

__author__ = "Josh Kibler"
__version__ = "1.3"
__status__ = "dev"
__date__ = "9.14.2022"

import copy, re, kivy, time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.properties import ListProperty, ObjectProperty, ColorProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
#from kivy.event import EventDispatcher
from kivmob import KivMob, TestIds

# Global variables

gen1typeMUs = {"nor": {2:["fig"],.5:[],0:["gho"]},
         "fir": {2:["wat","gro","roc"],.5:["fir","gra","bug"],0:[]},
         "wat": {2:["ele","gra"],.5:["fir","wat","ice"],0:[]},
         "ele": {2:["gro"],.5:["ele","fly"],0:[]},
         "gra": {2:["fir","ice","poi","fly","bug"],.5:["wat","ele","gra","gro"],0:[]},
         "ice": {2:["fir","fig","roc"],.5:["ice"],0:[]},
         "fig": {2:["fly","psy"],.5:["bug","roc"],0:[]},
         "poi": {2:["gro","psy","bug"],.5:["gra","fig","poi"],0:[]},
         "gro": {2:["wat","gra","ice"],.5:["poi","roc"],0:["ele"]},
         "fly": {2:["ele","ice","roc"],.5:["gra","fig","bug"],0:["gro"]},
         "psy": {2:["bug"],.5:["fig","psy"],0:["gho"]},
         "bug": {2:["fir","fly","roc","poi"],.5:["gra","fig","gro"],0:[]},
         "roc": {2:["wat","gra","fig","gro"],.5:["nor","fir","poi","fly"],0:[]},
         "gho": {2:["gho"],.5:["poi","bug"],0:["nor","fig"]},
         "dra": {2:["ice","dra"],.5:["fir","wat","ele","gra"],0:[]}}
gen2typeMUs = {"nor": {2:["fig"],.5:[],0:["gho"]},
         "fir": {2:["wat","gro","roc"],.5:["fir","gra","ice","bug","ste"],0:[]},
         "wat": {2:["ele","gra"],.5:["fir","wat","ice","ste"],0:[]},
         "ele": {2:["gro"],.5:["ele","fly","ste"],0:[]},
         "gra": {2:["fir","ice","poi","fly","bug"],.5:["wat","ele","gra","gro"],0:[]},
         "ice": {2:["fir","fig","roc","ste"],.5:["ice"],0:[]},
         "fig": {2:["fly","psy"],.5:["bug","roc","dar"],0:[]},
         "poi": {2:["gro","psy"],.5:["gra","fig","poi","bug"],0:[]},
         "gro": {2:["wat","gra","ice"],.5:["poi","roc"],0:["ele"]},
         "fly": {2:["ele","ice","roc"],.5:["gra","fig","bug"],0:["gro"]},
         "psy": {2:["bug","gho","dar"],.5:["fig","psy"],0:[]},
         "bug": {2:["fir","fly","roc"],.5:["gra","fig","gro"],0:[]},
         "roc": {2:["wat","gra","fig","gro","ste"],.5:["nor","fir","poi","fly"],0:[]},
         "gho": {2:["gho","dar"],.5:["poi","bug"],0:["nor","fig"]},
         "dra": {2:["ice","dra"],.5:["fir","wat","ele","gra"],0:[]},
         "dar": {2:["fig","bug"],.5:["gho","dar"],0:["psy"]},
         "ste": {2:["fir","fig","gro"],.5:["nor","gra","ice","fly","psy","bug","roc","dra","ste","gho","dar"],0:["poi"]}}
gen6typeMUs = {"nor": {2:["fig"],.5:[],0:["gho"]},
         "fir": {2:["wat","gro","roc"],.5:["fir","gra","ice","bug","ste","fai"],0:[]},
         "wat": {2:["ele","gra"],.5:["fir","wat","ice","ste"],0:[]},
         "ele": {2:["gro"],.5:["ele","fly","ste"],0:[]},
         "gra": {2:["fir","ice","poi","fly","bug"],.5:["wat","ele","gra","gro"],0:[]},
         "ice": {2:["fir","fig","roc","ste"],.5:["ice"],0:[]},
         "fig": {2:["fly","psy","fai"],.5:["bug","roc","dar"],0:[]},
         "poi": {2:["gro","psy"],.5:["gra","fig","poi","bug","fai"],0:[]},
         "gro": {2:["wat","gra","ice"],.5:["poi","roc"],0:["ele"]},
         "fly": {2:["ele","ice","roc"],.5:["gra","fig","bug"],0:["gro"]},
         "psy": {2:["bug","gho","dar"],.5:["fig","psy"],0:[]},
         "bug": {2:["fir","fly","roc"],.5:["gra","fig","gro"],0:[]},
         "roc": {2:["wat","gra","fig","gro","ste"],.5:["nor","fir","poi","fly"],0:[]},
         "gho": {2:["gho","dar"],.5:["poi","bug"],0:["nor","fig"]},
         "dra": {2:["ice","dra","fai"],.5:["fir","wat","ele","gra"],0:[]},
         "dar": {2:["fig","bug","fai"],.5:["gho","dar"],0:["psy"]},
         "ste": {2:["fir","fig","gro"],.5:["nor","gra","ice","fly","psy","bug","roc","dra","ste","fai"],0:["poi"]},
         "fai": {2:["poi","ste"],.5:["fig","bug","dar"],0:["dra"]}}
typecolors = {"non": '#000000',
         "nor": '#aaaa99',
         "fir": '#ff4422',
         "wat": '#339999',
         "ele": '#ffcc33',
         "gra": '#77cc55',
         "ice": '#66ccff',
         "fig": '#bb5644',
         "poi": '#aa5599',
         "gro": '#ddbb55',
         "fly": '#889aff',
         "psy": '#ff5599',
         "bug": '#a9bb22',
         "roc": '#bbaa66',
         "gho": '#454582',
         "dra": '#7866ee',
         "dar": '#775544',
         "ste": '#aaaabb',
         "fai": '#ee99ee'}
typeMUs = gen6typeMUs
allTypeMUs = copy.deepcopy(typeMUs)
allTypeMUs_simp = copy.deepcopy(typeMUs)
genlist = ["RBY", "GSC", "RSE FRLG", "DPPt HGSS", "BW B2W2", "XY ORAS", "SM USUM LGPE", "SwSh BDSP PLA"]
exclude = True
# excluded = False
unusedTypes = {1: ["ice", "fly", "roc", "gho", "nor fir", "nor wat", "nor ele", "nor gra",
"nor ice", "nor fig", "nor poi", "nor gro", "nor psy","nor bug", "nor roc",
"nor gho", "nor dra", "fir wat", "fir ele", "fir gra", "fir ice", "fir fig",
"fir poi", "fir gro", "fir psy", "fir bug", "fir roc", "fir gho", "fir dra", "wat ele",
"wat gra", "wat gro", "wat bug", "wat gho", "wat dra", "ele gra", "ele ice",
"ele fig", "ele poi", "ele gro", "ele psy", "ele bug", "ele roc",
"ele gho", "ele dra", "gra ice", "gra fig", "gra gro", "gra fly", "gra roc",
"gra gho", "gra dra", "ice fig", "ice poi", "ice gro", "ice bug", "ice roc", "ice gho",
"ice dra", "fig poi", "fig gro", "fig fly", "fig psy", "fig bug",
"fig roc", "fig gho", "fig dra", "poi psy", "poi roc", "poi dra", "gro fly",
"gro psy", "gro bug", "gro gho", "gro dra", "fly psy", "fly gho", "psy bug",
"psy roc", "psy gho", "psy dra", "bug roc", "bug gho", "bug dra", "roc gho", "roc dra",
"gho dra"],
2: ["ice", "fly", "ste", "nor fir", "nor wat", "nor ele", "nor gra", "nor ice",
"nor fig", "nor poi", "nor gro","nor bug", "nor roc", "nor gho", "nor dra",
"nor dar", "nor ste", "fir wat", "fir ele", "fir gra", "fir ice", "fir fig", "fir poi",
"fir gro", "fir psy", "fir bug", "fir gho", "fir dra", "fir ste", "wat gra", "wat bug",
"wat gho", "wat dar", "wat ste", "ele gra", "ele ice", "ele fig", "ele poi",
"ele gro", "ele psy", "ele bug", "ele roc", "ele gho", "ele dra",
"ele dar", "gra ice", "gra fig", "gra gro", "gra roc", "gra gho", "gra dra",
"gra dar", "gra ste", "ice fig", "ice poi", "ice bug", "ice roc", "ice gho", "ice dra", "ice ste",
"fig poi", "fig gro", "fig fly", "fig psy", "fig roc", "fig gho",
"fig dra", "fig dar", "fig ste", "poi psy", "poi roc", "poi dra", "poi dar",
"poi ste", "gro psy", "gro bug", "gro gho", "gro dra", "gro dar", "fly gho",
"psy bug", "psy roc", "psy gho", "psy dra", "psy dar", "psy ste", "bug gho",
"bug dra", "bug dar", "roc gho", "roc dra", "roc ste", "gho dra", "gho dar", "gho ste",
"dra dar", "dra ste", "dar ste"],
3: ["fly", "nor fir", "nor wat", "nor ele", "nor gra", "nor ice", "nor fig",
"nor poi", "nor gro", "nor bug", "nor roc", "nor gho", "nor dra", "nor dar",
"nor ste", "fir wat", "fir ele", "fir gra", "fir ice", "fir poi", "fir psy", "fir bug",
"fir gho", "fir dra", "fir ste", "wat gho", "wat ste", "ele gra", "ele ice",
"ele fig", "ele poi", "ele gro", "ele psy", "ele bug", "ele roc",
"ele gho", "ele dra", "ele dar", "gra ice", "gra gro", "gra gho", "gra dra",
"gra ste", "ice fig", "ice poi", "ice bug", "ice roc", "ice gho", "ice dra", "ice ste",
"fig poi", "fig gro", "fig fly", "fig roc", "fig gho", "fig dra",
"fig dar", "fig ste", "poi psy", "poi roc", "poi dra", "poi dar", "poi ste",
"gro gho", "gro dar", "fly gho", "psy bug", "psy gho", "psy dar", "bug dra", "bug dar",
"roc gho", "roc dra", "gho dra", "gho ste", "dra dar", "dra ste", "dar ste"],
4: ["nor fir", "nor ele", "nor gra", "nor ice", "nor fig", "nor poi", "nor gro",
"nor bug", "nor roc", "nor gho", "nor dra", "nor dar", "nor ste", "fir wat", "fir ele",
"fir gra", "fir ice", "fir poi", "fir psy", "fir bug", "fir gho", "fir dra", "wat gho",
"ele gra", "ele ice", "ele fig", "ele poi", "ele gro", "ele psy",
"ele bug", "ele roc", "ele dra", "ele dar", "gra gho", "gra dra", "gra ste",
"ice fig", "ice poi", "ice bug", "ice roc", "ice dra", "ice ste", "fig gro", "fig fly",
"fig roc", "fig gho", "fig dra", "fig dar", "poi psy", "poi roc", "poi dra",
"poi ste", "gro gho", "gro dar", "psy bug", "psy gho", "psy dar", "bug dra", "bug dar",
"roc gho", "roc dra", "gho ste", "dra dar", "dar ste"],
5: ["nor fir", "nor ele", "nor ice", "nor poi", "nor gro", "nor bug", "nor roc",
"nor gho", "nor dra", "nor dar", "nor ste", "fir wat", "fir gra", "fir ice", "fir poi",
"ele fig", "ele poi", "ele psy", "ele roc", "ele dar", "gra gho",
"gra dra", "ice fig", "ice poi", "ice bug", "ice roc", "ice ste", "fig gro", "fig fly",
"fig gho", "fig dra", "poi psy", "poi roc", "poi dra", "poi ste", "psy bug",
"psy gho", "psy dar", "bug dra", "bug dar", "roc gho", "roc dra", "gho ste"],
6: ["nor ice", "nor poi", "nor bug", "nor roc", "nor gho", "nor dra", "nor dar",
"nor ste", "fir gra", "fir ice", "fir poi", "fir fai", "ele fig", "ele poi",
"ele psy", "ele roc", "ele dar", "ice fig", "ice poi", "ice bug", "ice ste", "ice fai",
"fig gro", "fig gho", "fig dra", "fig fai", "poi psy", "poi roc",
"poi ste", "poi fai", "psy bug", "gro fai", "bug dra", "bug dar", "bug fai", "roc gho",
"gho fai", "dar fai"],
7: ["nor ice", "nor poi", "nor bug", "nor roc", "nor gho", "nor ste", "fir gra",
"fir ice", "fir fai", "ele fig", "ele poi", "ele dar", "ice poi", "ice bug",
"fig gro", "fig fai", "poi psy", "poi ste", "poi fai", "psy bug", "gro fai",
"bug dra", "bug dar", "roc gho", "dar fai"],
# gen 8 pokedexes don't match, actually more pokemon removed from SwSh, if need to fix or specify/separate which games
# could at least add a disclaimer for now, ask what users might prefer
8: ["nor ice", "nor poi", "nor bug", "nor roc", "nor ste", "fir gra", "fir fai",
"ele fig", "ice poi", "fig gro", "fig fai", "poi ste", "gro fai", "bug dra",
"bug dar", "roc gho"]}

# testdict = {'gra ste/ste fai': {'rating': 10.50, 'tweaks': ['fir', 'wat', 'ice'], 'tURs': ['fir']},
#             'wat gro/ste fai': {'rating': 10.25, 'tweaks': ['nor', 'bug'], 'tURs': []}}

# Team -----------------------------------------------------------------------------------------------------------------
class Team:
    def __init__(self, pkmn1, pkmn2, pkmn3="non", pkmn4="non", pkmn5="non", pkmn6="non"):
        self.pkmn1 = pkmn1
        self.pkmn2 = pkmn2
        self.pkmn3 = pkmn3
        self.pkmn4 = pkmn4
        self.pkmn5 = pkmn5
        self.pkmn6 = pkmn6
        #self.teamEffectsUnsorted = {}
        self.teamEffects = {}
        self.teamRating = 0
        if pkmn3 == "non": # means team of 2
            self.teamTypes = pkmn1.types + "/" + pkmn2.types
            #self.teamTypes_simp = pkmn2.types # not using these currently, could to improve "output splitting"
        elif pkmn4 == "non": # means team of 3
            self.teamTypes = pkmn1.types + "/" + pkmn2.types + "/" + pkmn3.types
            #self.teamTypes_simp = pkmn2.types + "/" + pkmn3.types
        elif pkmn5 == "non": # means team of 4
            self.teamTypes = pkmn1.types + "/" + pkmn2.types + "/" + pkmn3.types + "/" + pkmn4.types
            #self.teamTypes_simp = pkmn2.types + "/" + pkmn3.types + "/" + pkmn4.types
        elif pkmn6 == "non": # means team of 5
            self.teamTypes = pkmn1.types + "/" + pkmn2.types + "/" + pkmn3.types + "/" + pkmn4.types + "/" + pkmn5.types
            #self.teamTypes_simp = pkmn2.types + "/" + pkmn3.types + "/" + pkmn4.types + "/" + pkmn4.types
        else: # means team of 6
            self.teamTypes = pkmn1.types + "/" + pkmn2.types + "/" + pkmn3.types + "/" + pkmn4.types + "/" + pkmn5.types + "/" + pkmn6.types
            #self.teamTypes_simp = pkmn2.types + "/" + pkmn3.types + "/" + pkmn4.types + "/" + pkmn5.types + "/" + pkmn6.types
        self.weaksNum = 0
        self.weaksList = []
        self.resistsList = []
        self.URList = []

    # get effects (strengths and weaknesses) of pokemon team type combo
    # accept boolean whether simplified or unsimplified effects wanted?
    def getTeamEffects(self):
        #pkmn1Effects = self.pkmn1.effects
        #pkmn2Effects = self.pkmn2.effects
        #print(pkmn1Effects)
        #print(pkmn2Effects)
        # merge effect list values in all 3 type dicts (could also try using .format and replace variable name w/loop)
        if self.pkmn1.types in allTypeMUs_simp:
            types1dict = copy.deepcopy(allTypeMUs_simp[self.pkmn1.types])
        else:
            types1dict = copy.deepcopy(allTypeMUs_simp[self.pkmn1.typesR])
        if self.pkmn2.types in allTypeMUs_simp:
            types2dict = copy.deepcopy(allTypeMUs_simp[self.pkmn2.types])
        else:
            types2dict = copy.deepcopy(allTypeMUs_simp[self.pkmn2.typesR])
        if self.pkmn3 != "non": # means team of at least 3
            if self.pkmn3.types in allTypeMUs_simp:
                types3dict = copy.deepcopy(allTypeMUs_simp[self.pkmn3.types])
            else:
                types3dict = copy.deepcopy(allTypeMUs_simp[self.pkmn3.typesR])
            #print("types3dict set:", types3dict)
        if self.pkmn4 != "non": # means team of 4
            if self.pkmn4.types in allTypeMUs_simp:
                types4dict = copy.deepcopy(allTypeMUs_simp[self.pkmn4.types])
            else:
                types4dict = copy.deepcopy(allTypeMUs_simp[self.pkmn4.typesR])
        if self.pkmn5 != "non":  # means team of 5
            if self.pkmn5.types in allTypeMUs_simp:
                types5dict = copy.deepcopy(allTypeMUs_simp[self.pkmn5.types])
            else:
                types5dict = copy.deepcopy(allTypeMUs_simp[self.pkmn5.typesR])
        if self.pkmn6 != "non":  # means team of 6
            if self.pkmn6.types in allTypeMUs_simp:
                types6dict = copy.deepcopy(allTypeMUs_simp[self.pkmn6.types])
            else:
                types6dict = copy.deepcopy(allTypeMUs_simp[self.pkmn6.typesR])
            #print("types4dict set:", types4dict)
        merged = {4:[],2:[],1:[],0.5:[],0.25:[],0:[]}
        #print(types1dict)
        #print(types2dict)
        # for each effect key in merged
        for key in merged:
            # append from all 3 pkmn types dicts to same effect key in merged dict
            if key in types1dict:
                for value in types1dict[key]:
                    #print(value)
                    #print(merged[key])
                    merged[key].append(value)
            if key in types2dict:
                for value in types2dict[key]:
                    # print(value)
                    # print(merged[key])
                    merged[key].append(value)
            if self.pkmn3 != "non": # means team of at least 3
                if key in types3dict:
                    for value in types3dict[key]:
                        # print(value)
                        # print(merged[key])
                        merged[key].append(value)
            if self.pkmn4 != "non": # means team of 4
                if key in types4dict:
                    for value in types4dict[key]:
                        # print(value)
                        # print(merged[key])
                        merged[key].append(value)
            if self.pkmn5 != "non": # means team of 5
                if key in types5dict:
                    for value in types5dict[key]:
                        # print(value)
                        # print(merged[key])
                        merged[key].append(value)
            if self.pkmn6 != "non": # means team of 6
                if key in types6dict:
                    for value in types6dict[key]:
                        # print(value)
                        # print(merged[key])
                        merged[key].append(value)
            #print(merged)

        # find effect of type in all 3 dicts, multiply together then form new dict based on results
        # v1.3 should do 2-4
        for type in typeMUs:
            multlist = []
            #print(type)
            # for each effect key in merged
            for key in merged:
                count = merged[key].count(type)
                if count > 0:
                    multlist.append(key**count)
                    # must get resists before multiplication
                    if key < 1 and type not in self.resistsList:
                        # print(key,type,self.URList)
                        self.resistsList.append(type)
            # if self.teamTypes == 'fir dra/fly/nor ste':
            #     print(type, key, merged[key].count(type), key**count)
            #print(merged)
            result = 1
            for x in multlist:
                result = result * x
            # if self.teamTypes == 'fir dra/fly/nor ste':
            #     print(multlist, result)
            # add effect to corresponding list in teamEffects dict
            self.teamEffects.setdefault(result, []).append(type)

        # get unresists based on types absent from resists list
        for type in typeMUs:
            if type not in self.resistsList:
                self.URList.append(type)

        # sort effects from high to low
        # sort = sorted(self.teamEffectsUnsorted.items(), reverse=True)
        # for e in sort:
        #     self.teamEffects[e] = sort[e]
        return sorted(self.teamEffects.items(), reverse=True)
        #return self.teamEffects

    # get rating of pokemon team type combo
    def getTeamRating(self):
        # get effect number for each type
        for type in typeMUs:
            typeEffectFound = False
            # while typeEffectFound:
            # for each effect number list
            for effect in self.teamEffects:
                # if type in effect number list
                if type in self.teamEffects[effect]:
                    #print(type, effect)
                    self.teamRating += effect
                    typeEffectFound = True
                    break
            if typeEffectFound == False:
                # print(type)
                # print(1)
                self.teamRating += 1
        return self.teamRating

    # get number of team weaknesses
    def getWeaks(self):
        # if no weaknesses
        if max(self.teamEffects) < 2:
            self.weaksNum = 0
            #self.weaksList.append('non')
        # if weaknesses
        else: #if max(self.teamEffects) > 1:
            #print(self.teamTypes)
            for key in self.teamEffects:
                if key > 1:
                    self.weaksNum += len(self.teamEffects[key]) * key/2
                    if key == 4:
                        for weak in self.teamEffects[key]:
                            self.weaksList.append(weak + "X2")
                    elif key == 8:
                        for weak in self.teamEffects[key]:
                            self.weaksList.append(weak + "X4")
                    else:
                        for weak in self.teamEffects[key]:
                            self.weaksList.append(weak)
        return self.weaksList

# Pokemon --------------------------------------------------------------------------------------------------------------
class Pokemon:
    #type 2 optional, blank by default
    def __init__(self,type1,type2=""):
        self.type1 = type1
        self.type2 = type2
        if type2 != "":
            self.types = type1 + " " + type2
        else:
            self.types = type1
        self.typesR = type2 + " " + type1
        #self.effectsUnsorted = {}
        self.effects = {}
        self.effectsSimp = {}
        self.rating = 0
    # get effects (strengths and weaknesses) of pokemon type combo
    def getEffects(self):
        # merge effect list values in both type dicts (if 2 types)
        if self.type2 != "":
            typesChecked = []
            type1dict = copy.deepcopy(typeMUs[self.type1])
            type2dict = copy.deepcopy(typeMUs[self.type2])
            merged = type1dict
            #for each effect key in type2 dict
            for key in type2dict:
                #append type to same effect key in merged dict
                for value in type2dict[key]:
                    merged[key].append(value)
            #for each key in merged dict
            for key in merged:
                for value in merged[key]:
                    multlist = []
                    #make sure type not checked already
                    if value not in typesChecked:
                        typesChecked.append(value)
                        for key2 in merged:
                            for value2 in merged[key2]:
                                #where type match, append to list to multiply
                                if value == value2:
                                    multlist.append(key2)
                        result = 1
                        for x in multlist:
                            result = result * x
                        #add effect to corresponding list in effects dict
                        self.effects.setdefault(result, []).append(value)
        else:
            self.effects = typeMUs[self.type1]
        # sort effects from high to low
        #sort = sorted(self.effectsUnsorted.items(), reverse=True)
        #self.effects = collections.OrderedDict(sort)
        # for e in sort:
        #     #print(e[0])
        #     ekey = e[0]
        #     self.effects[e] = sort[ekey]
        return self.effects

    # get simplified effects (without quad strengths and weaknesses) of pokemon type combo
    def getEffectsSimp(self):
        self.effectsSimp = copy.deepcopy(self.effects)
        if 4 in self.effectsSimp:
            if 2 not in self.effectsSimp:
                self.effectsSimp[2] = []
            for e in self.effectsSimp[4]:
                self.effectsSimp[2].append(e)
            self.effectsSimp.pop(4)
        if 0.25 in self.effectsSimp:
            if 0.5 not in self.effectsSimp:
                self.effectsSimp[0.5] = []
            for e in self.effectsSimp[0.25]:
                self.effectsSimp[0.5].append(e)
            self.effectsSimp.pop(0.25)
        if 0 in self.effectsSimp:
            if 0.5 not in self.effectsSimp:
                self.effectsSimp[0.5] = []
            for e in self.effectsSimp[0]:
                self.effectsSimp[0.5].append(e)
            self.effectsSimp.pop(0)
        return self.effectsSimp

    # get rating of pokemon type combo
    def getRating(self):
        # get effect number for each type
        for type in typeMUs:
            typeEffectFound = False
            #while typeEffectFound:
            # for each effect number list
            for effect in self.effects:
                # if type in effect number list
                if type in self.effects[effect]:
                    #print(type, effect)
                    self.rating += effect
                    typeEffectFound = True
                    break
            if typeEffectFound == False:
                # print(type)
                # print(1)
                self.rating += 1
        return self.rating

# Global functions -----------------------------------------------------------------------------------------------------
def initialize():
    # first correct all single types to simplified effects
    for key in allTypeMUs_simp:
        split = key.split()
        if len(split) == 2:
            pkmn = Pokemon(split[0], split[1])
        else:
            pkmn = Pokemon(split[0])
        allTypeMUs_simp[key] = pkmn.getEffects()
        allTypeMUs_simp[key] = pkmn.getEffectsSimp()

    # iterate all possible type combos to generate all their effects
    for key in typeMUs:
        for key2 in typeMUs:
            # do not generate same type combos (e.g. nor nor)
            if key != key2:
                pkmn = Pokemon(key, key2)
                # do not generate already generated combos in opposite order (e.g. nor wat, wat nor)
                if pkmn.typesR not in allTypeMUs:
                    allTypeMUs[pkmn.types] = pkmn.getEffects()
                    allTypeMUs_simp[pkmn.types] = pkmn.getEffectsSimp()

def calculate(TrowsTypesDict, tsize, gen):
    # global variables
    global rsort1,rsort2,psort1,psort2,wsort1,wsort2,usort1,usort2,noWeakTeamsNum,oneWeakTeamsNum,teamsDict2, typeMUs,\
        allTypeMUs, allTypeMUs_simp #, excluded
    rsort1 = {}
    rsort2 = {}
    psort1 = {}
    psort2 = {}
    wsort1 = {}
    wsort2 = {}
    usort1 = {}
    usort2 = {}

    # reset variables
    teamsDict = {}
    teamsDict2 = {}
    noWeakTeamsNum = 0
    oneWeakTeamsNum = 0
    ratingMin = 100
    ratingMax = 0
    tfilter = '-'
    writable = True
    #pkmn1 = Pokemon('','')

    # analyze dict to figure out how many typing rows, what types, and what team size to calc
    # set pkmn based on dict
    for key, value in TrowsTypesDict.items():
        print(value[1])
        if value[1] == 'non':
            value[1] = ''
            # TrowsTypesDict[key][1] = ''
        print(value[1],TrowsTypesDict[key][1])
        print(key, value)
        if key == 1:
            pkmn1 = Pokemon(value[0], value[1])
        elif key == 2:
            pkmn2 = Pokemon(value[0], value[1])
        elif key == 3:
            pkmn3 = Pokemon(value[0], value[1])
        elif key == 4:
            pkmn4 = Pokemon(value[0], value[1])
        else: #if key == 5:
            pkmn5 = Pokemon(value[0], value[1])
        # exec(f'pkmn{key} = Pokemon(value[0], value[1])')
        # print(exec(f'pkmn{key}.types'))
    # print(pkmn1.types)
    # pkmn1 = Pokemon(pkmntype1, pkmntype2)
    nToCalc = tsize - len(TrowsTypesDict)
    print("Number of typings to calculate:", nToCalc)

    # print("allTypeMUs:")
    # for key, value in allTypeMUs.items():
    #     print(key, ' : ', value)

    #required to fill allTypeMUs dicts (can optimize?)
    initialize()

    #print("exclude", exclude, "excluded", excluded)
    if exclude:# and not excluded:
        # pop unused types by gen before calculations
        for type in unusedTypes[gen]:
            allTypeMUs.pop(type)
            allTypeMUs_simp.pop(type)
        # excluded = True

    # print("allTypeMUs_simp:")
    # for key, value in allTypeMUs_simp.items():
    #     print("'"+str(key)+"'"+": "+str(value)+",")

    #pkmn1.getEffects()
    lookupEffects(pkmn1, allTypeMUs)
    #pkmn1.getEffectsSimp()
    lookupEffects(pkmn1, allTypeMUs_simp)
    pkmn1.getRating()

    icount = 0
    # iterate over all type MUs SIMPLIFIED to get effects
    # check if user already provided pkmn2
    if len(TrowsTypesDict) > 1:
        lookupEffects(pkmn2, allTypeMUs_simp)

        # if tsize > 2: # 2 pokemon set, always at least one more
        # check if user already provided pkmn3
        if len(TrowsTypesDict) > 2:
            lookupEffects(pkmn3, allTypeMUs_simp)

            # check if user already provided pkmn4
            if len(TrowsTypesDict) > 3:
                lookupEffects(pkmn4, allTypeMUs_simp)

                # check if user already provided pkmn5
                if len(TrowsTypesDict) > 4:
                    lookupEffects(pkmn5, allTypeMUs_simp)
                    # loop for 6th pokemon, always last one to calc when 5 pokemon set
                    for key5 in allTypeMUs_simp:
                        # print(key3, pkmn3.types)
                        if key5 not in [pkmn1.types, pkmn2.types, pkmn3.types, pkmn4.types, pkmn5.types]:
                            # print(key)
                            split = key5.split()
                            if len(split) == 2:
                                pkmn6 = Pokemon(split[0], split[1])
                            else:
                                pkmn6 = Pokemon(split[0])
                            # Look up effectiveness from dict
                            lookupEffects(pkmn6, allTypeMUs_simp)
                            # print(pkmn6.effects)

                            # build results output for team of 6
                            # print("5 pokemon set, team size 6")
                            team = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn5, pkmn6)
                            icount += 1
                            team.getTeamEffects()  # MUST run before getTeamRating()
                            teamsDict[team.teamTypes] = {'rating': team.getTeamRating(), 'tweaks': team.getWeaks(),
                                                         'tURs': team.URList}
                            if team.teamRating < ratingMin:
                                ratingMin = team.teamRating
                            if team.teamRating > ratingMax:
                                ratingMax = team.teamRating
                            if team.weaksNum == 0:
                                noWeakTeamsNum += 1
                            elif team.weaksNum == 1:
                                oneWeakTeamsNum += 1

                # means 4 pokemon set, team size 5-6
                else:
                    # print("4 pokemon set, team size 5-6")
                    # loop for 5th pokemon
                    for key4 in allTypeMUs_simp:
                        # print(key3, pkmn3.types)
                        if key4 not in [pkmn1.types, pkmn2.types, pkmn3.types, pkmn4.types]:
                            # print(key)
                            split = key4.split()
                            if len(split) == 2:
                                pkmn5 = Pokemon(split[0], split[1])
                            else:
                                pkmn5 = Pokemon(split[0])
                            # Look up effectiveness from dict
                            lookupEffects(pkmn5, allTypeMUs_simp)
                            # print(pkmn5.effects)

                            if tsize > 5:
                                # loop for 6th
                                for key5 in allTypeMUs_simp:
                                    # print(key3, pkmn3.types)
                                    if key5 not in [pkmn1.types, pkmn2.types, pkmn3.types, pkmn4.types, pkmn5.types]:
                                        # print(key)
                                        split = key5.split()
                                        if len(split) == 2:
                                            pkmn6 = Pokemon(split[0], split[1])
                                        else:
                                            pkmn6 = Pokemon(split[0])
                                        # Look up effectiveness from dict
                                        lookupEffects(pkmn6, allTypeMUs_simp)
                                        # print(pkmn6.effects)

                                        # build results output for team of 6
                                        # print("4 pokemon set, team size 6")
                                        team = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn5, pkmn6)
                                        teamR = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn6, pkmn5)

                                        if teamR.teamTypes not in teamsDict:
                                            icount += 1
                                            team.getTeamEffects()  # MUST run before getTeamRating()
                                            teamsDict[team.teamTypes] = {'rating': team.getTeamRating(),
                                                                         'tweaks': team.getWeaks(), 'tURs': team.URList}
                                            if team.teamRating < ratingMin:
                                                ratingMin = team.teamRating
                                            if team.teamRating > ratingMax:
                                                ratingMax = team.teamRating
                                            if team.weaksNum == 0:
                                                noWeakTeamsNum += 1
                                            elif team.weaksNum == 1:
                                                oneWeakTeamsNum += 1

                            # means 4 pokemon set, team size 5
                            else:
                                # build results output for team of 5
                                # print("4 pokemon set, team size 5")
                                team = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn5)
                                icount += 1
                                team.getTeamEffects()  # MUST run before getTeamRating()
                                teamsDict[team.teamTypes] = {'rating': team.getTeamRating(), 'tweaks': team.getWeaks(),
                                                             'tURs': team.URList}
                                if team.teamRating < ratingMin:
                                    ratingMin = team.teamRating
                                if team.teamRating > ratingMax:
                                    ratingMax = team.teamRating
                                if team.weaksNum == 0:
                                    noWeakTeamsNum += 1
                                elif team.weaksNum == 1:
                                    oneWeakTeamsNum += 1

            # means 3 pokemon set, team size 4-6
            else:
                # print("3 pokemon set, team size 4-6")
                # loop for 4th pokemon
                for key3 in allTypeMUs_simp:
                    # print(key3, pkmn3.types)
                    if key3 not in [pkmn1.types, pkmn2.types, pkmn3.types]:
                        # print(key)
                        split = key3.split()
                        if len(split) == 2:
                            pkmn4 = Pokemon(split[0], split[1])
                        else:
                            pkmn4 = Pokemon(split[0])
                        # Look up effectiveness from dict
                        lookupEffects(pkmn4, allTypeMUs_simp)
                        # print(pkmn4.effects)

                        if tsize > 4:
                            # loop for 5th pokemon
                            for key4 in allTypeMUs_simp:
                                # print(key3, pkmn3.types)
                                if key4 not in [pkmn1.types, pkmn2.types, pkmn3.types, pkmn4.types]:
                                    # print(key)
                                    split = key4.split()
                                    if len(split) == 2:
                                        pkmn5 = Pokemon(split[0], split[1])
                                    else:
                                        pkmn5 = Pokemon(split[0])
                                    # Look up effectiveness from dict
                                    lookupEffects(pkmn5, allTypeMUs_simp)
                                    # print(pkmn5.effects)

                            if tsize > 5:
                                # loop for 6th pokemon
                                for key5 in allTypeMUs_simp:
                                    # print(key3, pkmn3.types)
                                    if key5 not in [pkmn1.types, pkmn2.types, pkmn3.types, pkmn4.types, pkmn5.types]:
                                        # print(key)
                                        split = key5.split()
                                        if len(split) == 2:
                                            pkmn6 = Pokemon(split[0], split[1])
                                        else:
                                            pkmn6 = Pokemon(split[0])
                                        # Look up effectiveness from dict
                                        lookupEffects(pkmn6, allTypeMUs_simp)
                                        # print(pkmn6.effects)

                                        # build results output for team of 6
                                        # print("3 pokemon set, team size 6")
                                        team = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn5, pkmn6)
                                        teamR1 = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn6, pkmn5)
                                        teamR2 = Team(pkmn1, pkmn2, pkmn3, pkmn5, pkmn4, pkmn6)
                                        teamR3 = Team(pkmn1, pkmn2, pkmn3, pkmn5, pkmn6, pkmn4)
                                        teamR4 = Team(pkmn1, pkmn2, pkmn3, pkmn6, pkmn4, pkmn5)
                                        teamR5 = Team(pkmn1, pkmn2, pkmn3, pkmn6, pkmn5, pkmn4)

                                        if teamR1.teamTypes not in teamsDict and teamR2.teamTypes not in teamsDict and \
                                                teamR3.teamTypes not in teamsDict and teamR4.teamTypes not in teamsDict and teamR5.teamTypes not in teamsDict:
                                            icount += 1
                                            team.getTeamEffects()  # MUST run before getTeamRating()
                                            teamsDict[team.teamTypes] = {'rating': team.getTeamRating(),
                                                                         'tweaks': team.getWeaks(),
                                                                         'tURs': team.URList}
                                            if team.teamRating < ratingMin:
                                                ratingMin = team.teamRating
                                            if team.teamRating > ratingMax:
                                                ratingMax = team.teamRating
                                            if team.weaksNum == 0:
                                                noWeakTeamsNum += 1
                                            elif team.weaksNum == 1:
                                                oneWeakTeamsNum += 1

                            # means 3 pokemon set, team size 5
                            else:
                                # print("3 pokemon set, team size 5")
                                # build results output for team of 5
                                team = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn5)
                                teamR = Team(pkmn1, pkmn2, pkmn3, pkmn5, pkmn4)

                                if teamR.teamTypes not in teamsDict:
                                    icount += 1
                                    team.getTeamEffects()  # MUST run before getTeamRating()
                                    teamsDict[team.teamTypes] = {'rating': team.getTeamRating(),
                                                                 'tweaks': team.getWeaks(), 'tURs': team.URList}
                                    if team.teamRating < ratingMin:
                                        ratingMin = team.teamRating
                                    if team.teamRating > ratingMax:
                                        ratingMax = team.teamRating
                                    if team.weaksNum == 0:
                                        noWeakTeamsNum += 1
                                    elif team.weaksNum == 1:
                                        oneWeakTeamsNum += 1

                        # means 3 pokemon set, team size 4
                        else:
                            # print("3 pokemon set, team size 4")
                            # build results output for team of 4
                            team = Team(pkmn1, pkmn2, pkmn3, pkmn4)
                            icount += 1
                            team.getTeamEffects()  # MUST run before getTeamRating()
                            teamsDict[team.teamTypes] = {'rating': team.getTeamRating(), 'tweaks': team.getWeaks(),
                                                         'tURs': team.URList}
                            if team.teamRating < ratingMin:
                                ratingMin = team.teamRating
                            if team.teamRating > ratingMax:
                                ratingMax = team.teamRating
                            if team.weaksNum == 0:
                                noWeakTeamsNum += 1
                            elif team.weaksNum == 1:
                                oneWeakTeamsNum += 1

        # means 2 pokemon set, team size 3-6
        else:
            # print("2 pokemon set, team size 3-6")
            # loop for 3rd pokemon
            for key2 in allTypeMUs_simp:
                # print(key2, pkmn2.types)
                if key2 != pkmn1.types and key2 != pkmn2.types:
                    # print(key)
                    split = key2.split()
                    if len(split) == 2:
                        pkmn3 = Pokemon(split[0], split[1])
                    else:
                        pkmn3 = Pokemon(split[0])
                    # Look up effectiveness from dict
                    lookupEffects(pkmn3, allTypeMUs_simp)
                    # print(pkmn3.effects)

                    if tsize > 3:
                        # loop for 4th pokemon
                        for key3 in allTypeMUs_simp:
                            # print(key3, pkmn3.types)
                            if key3 not in [pkmn1.types, pkmn2.types, pkmn3.types]:
                                # print(key)
                                split = key3.split()
                                if len(split) == 2:
                                    pkmn4 = Pokemon(split[0], split[1])
                                else:
                                    pkmn4 = Pokemon(split[0])
                                # Look up effectiveness from dict
                                lookupEffects(pkmn4, allTypeMUs_simp)
                                # print(pkmn4.effects)

                                if tsize > 4:
                                    # loop for 5th pokemon
                                    for key4 in allTypeMUs_simp:
                                        # print(key3, pkmn3.types)
                                        if key4 not in [pkmn1.types, pkmn2.types, pkmn3.types, pkmn4.types]:
                                            # print(key)
                                            split = key4.split()
                                            if len(split) == 2:
                                                pkmn5 = Pokemon(split[0], split[1])
                                            else:
                                                pkmn5 = Pokemon(split[0])
                                            # Look up effectiveness from dict
                                            lookupEffects(pkmn5, allTypeMUs_simp)
                                            # print(pkmn5.effects)

                                            # build results output for team of 5
                                            # print("2 pokemon set, team size 5")
                                            team = Team(pkmn1, pkmn2, pkmn3, pkmn4, pkmn5)
                                            teamR1 = Team(pkmn1, pkmn2, pkmn3, pkmn5, pkmn4)
                                            teamR2 = Team(pkmn1, pkmn2, pkmn4, pkmn3, pkmn5)
                                            teamR3 = Team(pkmn1, pkmn2, pkmn4, pkmn5, pkmn3)
                                            teamR4 = Team(pkmn1, pkmn2, pkmn5, pkmn3, pkmn4)
                                            teamR5 = Team(pkmn1, pkmn2, pkmn5, pkmn4, pkmn3)

                                            if teamR1.teamTypes not in teamsDict and teamR2.teamTypes not in teamsDict and \
                                                    teamR3.teamTypes not in teamsDict and teamR4.teamTypes not in teamsDict and teamR5.teamTypes not in teamsDict:
                                                icount += 1
                                                team.getTeamEffects()  # MUST run before getTeamRating()
                                                teamsDict[team.teamTypes] = {'rating': team.getTeamRating(),
                                                                             'tweaks': team.getWeaks(),
                                                                             'tURs': team.URList}
                                                if team.teamRating < ratingMin:
                                                    ratingMin = team.teamRating
                                                if team.teamRating > ratingMax:
                                                    ratingMax = team.teamRating
                                                if team.weaksNum == 0:
                                                    noWeakTeamsNum += 1
                                                elif team.weaksNum == 1:
                                                    oneWeakTeamsNum += 1

                                            # if tsize > 5: # CANNOT currently have 2 pokemon set, team size 6
                                                # loop for 6th pokemon

                                                # build results output for team of 6

                                            # means 2 pokemon set, team size 5, remove build above if plan to use
                                            # else:
                                                # build results output for team of 5

                                # means 2 pokemon set, team size 4
                                else:
                                    # print("2 pokemon set, team size 4")
                                    # build results output for team of 4
                                    team = Team(pkmn1, pkmn2, pkmn3, pkmn4)
                                    teamR = Team(pkmn1, pkmn2, pkmn4, pkmn3)

                                    if teamR.teamTypes not in teamsDict:
                                        icount += 1
                                        team.getTeamEffects()  # MUST run before getTeamRating()
                                        teamsDict[team.teamTypes] = {'rating': team.getTeamRating(),
                                                                     'tweaks': team.getWeaks(), 'tURs': team.URList}
                                        if team.teamRating < ratingMin:
                                            ratingMin = team.teamRating
                                        if team.teamRating > ratingMax:
                                            ratingMax = team.teamRating
                                        if team.weaksNum == 0:
                                            noWeakTeamsNum += 1
                                        elif team.weaksNum == 1:
                                            oneWeakTeamsNum += 1

                    # means 2 pokemon set, team size 3
                    else:
                        # print("2 pokemon set, team size 3")
                        team = Team(pkmn1, pkmn2, pkmn3)
                        icount += 1
                        team.getTeamEffects()  # MUST run before getTeamRating()
                        teamsDict[team.teamTypes] = {'rating': team.getTeamRating(), 'tweaks': team.getWeaks(),
                                                     'tURs': team.URList}
                        if team.teamRating < ratingMin:
                            ratingMin = team.teamRating
                        if team.teamRating > ratingMax:
                            ratingMax = team.teamRating
                        if team.weaksNum == 0:
                            noWeakTeamsNum += 1
                        elif team.weaksNum == 1:
                            oneWeakTeamsNum += 1

    # means 1 pokemon set, team size 2-6
    else:
        # loop for 2nd pokemon
        # print("1 pokemon set, team size 2-6")
        for key in allTypeMUs_simp:
            if key != pkmn1.types and key != pkmn1.typesR:
                # print(key)
                split = key.split()
                if len(split) == 2:
                    pkmn2 = Pokemon(split[0], split[1])
                else:
                    pkmn2 = Pokemon(split[0])
                # Look up effectiveness from dict
                lookupEffects(pkmn2, allTypeMUs_simp)
                # print(pkmn2.effects)

                if tsize > 2:
                    # loop for 3rd pokemon
                    for key2 in allTypeMUs_simp:
                        # print(key2, pkmn2.types)
                        if key2 != key and key2 != pkmn1.types:
                            # print(key)
                            split = key2.split()
                            if len(split) == 2:
                                pkmn3 = Pokemon(split[0], split[1])
                            else:
                                pkmn3 = Pokemon(split[0])
                            # Look up effectiveness from dict
                            lookupEffects(pkmn3, allTypeMUs_simp)
                            # print(pkmn3.effects)

                            if tsize > 3:
                                # loop for 4th pokemon
                                for key3 in allTypeMUs_simp:
                                    # print(key3, pkmn3.types)
                                    if key3 != key and key3 != key2 and key3 != pkmn1.types:
                                        # print(key)
                                        split = key3.split()
                                        if len(split) == 2:
                                            pkmn4 = Pokemon(split[0], split[1])
                                        else:
                                            pkmn4 = Pokemon(split[0])
                                        # Look up effectiveness from dict
                                        lookupEffects(pkmn4, allTypeMUs_simp)
                                        # print(pkmn4.effects)

                                        # build results output for team of 4
                                        # print("1 pokemon set, team size 4")
                                        # Build teams dict data output for 4 (only when team types reversed not already in to prevent dupes)
                                        # can use set() instead? would need teamTypes list instead of string
                                        team = Team(pkmn1, pkmn2, pkmn3, pkmn4)
                                        teamR1 = Team(pkmn1, pkmn2, pkmn4, pkmn3)
                                        teamR2 = Team(pkmn1, pkmn3, pkmn2, pkmn4)
                                        teamR3 = Team(pkmn1, pkmn3, pkmn4, pkmn2)
                                        teamR4 = Team(pkmn1, pkmn4, pkmn2, pkmn3)
                                        teamR5 = Team(pkmn1, pkmn4, pkmn3, pkmn2)

                                        if teamR1.teamTypes not in teamsDict and teamR2.teamTypes not in teamsDict and \
                                                teamR3.teamTypes not in teamsDict and teamR4.teamTypes not in teamsDict and teamR5.teamTypes not in teamsDict:
                                            icount += 1
                                            team.getTeamEffects()  # MUST run before getTeamRating()
                                            teamsDict[team.teamTypes] = {'rating': team.getTeamRating(),
                                                                         'tweaks': team.getWeaks(), 'tURs': team.URList}
                                            if team.teamRating < ratingMin:
                                                ratingMin = team.teamRating
                                            if team.teamRating > ratingMax:
                                                ratingMax = team.teamRating
                                            if team.weaksNum == 0:
                                                noWeakTeamsNum += 1
                                            elif team.weaksNum == 1:
                                                oneWeakTeamsNum += 1

                                        # if tsize > 4: # CANNOT currently have 1 pokemon set, team size 5
                                            # loop for 5th pokemon

                                            # if tsize > 5: # CANNOT currently have 1 pokemon set, team size 6
                                                # loop for 6th pokemon

                                                # build results output for team of 6

                                            # means 1 pokemon set, team size 5
                                            # else:
                                                # build results output for team of 5

                                        # means 1 pokemon set, team size 4
                                        # else:
                                            # build results output for team of 4

                            # means 1 pokemon set, team size 3
                            else:
                                # print("1 pokemon set, team size 3")
                                # build results output for team of 3
                                team = Team(pkmn1, pkmn2, pkmn3)
                                teamR = Team(pkmn1, pkmn3, pkmn2)

                                if teamR.teamTypes not in teamsDict:
                                    icount += 1
                                    team.getTeamEffects()  # MUST run before getTeamRating()
                                    teamsDict[team.teamTypes] = {'rating': team.getTeamRating(),
                                                                 'tweaks': team.getWeaks(), 'tURs': team.URList}
                                    if team.teamRating < ratingMin:
                                        ratingMin = team.teamRating
                                    if team.teamRating > ratingMax:
                                        ratingMax = team.teamRating
                                    if team.weaksNum == 0:
                                        noWeakTeamsNum += 1
                                    elif team.weaksNum == 1:
                                        oneWeakTeamsNum += 1

                # means 1 pokemon set, team size 2
                else:
                    # print("1 pokemon set, team size 2")
                    # build results output for team of 2, make into a method?
                    team = Team(pkmn1, pkmn2)
                    icount += 1
                    team.getTeamEffects()  # MUST run before getTeamRating()
                    teamsDict[team.teamTypes] = {'rating': team.getTeamRating(), 'tweaks': team.getWeaks(),
                                                 'tURs': team.URList}
                    if team.teamRating < ratingMin:
                        ratingMin = team.teamRating
                    if team.teamRating > ratingMax:
                        ratingMax = team.teamRating
                    if team.weaksNum == 0:
                        noWeakTeamsNum += 1
                    elif team.weaksNum == 1:
                        oneWeakTeamsNum += 1

    print("Total teams:", icount)
    # formula for percentage to use (inverse exponent based on tenth places)
    if nToCalc > 1:
        pToUse = 100 * 10 ** (1 - len(str(icount)))
        topPercent = (ratingMax - ratingMin) * pToUse + ratingMin
        print(str(tsize) + " teams, top " + str(100*pToUse) + "% threshold: " + str(topPercent))
    else:
        topPercent = ratingMax
        print(str(tsize) + " teams, no rating threshold since only 1 to calc for, max is: " + str(topPercent))
    # elif tsize == 3:
    #     topPercent = (ratingMax - ratingMin)/10 + ratingMin
    #     print("3 teams, top 10% rating threshold: " + str(topPercent))
    # else:
    #     topPercent = (ratingMax - ratingMin)/100 + ratingMin
    #     print("4 teams, top 1% rating threshold: " + str(topPercent))
    # topPercent_count = 0

    # Correct teamsDict key names to exclude first pokemon types after calc, and filter top 10%/all 0/1 weak teams
    # and add to full data to file
    try:
        file = open("teams_output.csv", "w")
    except:
        print('Warning: unable to export output to file.')
        writable = False
    for key,value in teamsDict.items():
        if(writable):
            rating = str(value['rating'])
            team = re.sub(" ", "_", key)
            tweaksnum = str(len(value['tweaks'])) + ":"
            tweaks = re.sub(" ", "_", str(value['tweaks']))
            tweaks = re.sub("[\[',\]]", "", tweaks)
            tURsnum = str(len(value['tURs'])) + ":"
            tURs = re.sub(" ", "_", str(value['tURs']))
            tURs = re.sub("[\[',\]]", "", tURs)
            file.write(rating + "\t" + team + "\t" + tweaksnum + tweaks + "\t" + tURsnum + tURs + "\n")

        # output splitting
        split = key.split('/')
        #print(split)
        if tsize == 3:
            if nToCalc == 2:
                new_key = split[1] + '/' + split[2]
            else: #nToCalc == 1:
                new_key = split[2]
        elif tsize == 4:
            if nToCalc == 3:
                new_key = split[1] + '/' + split[2] + '/' + split[3]
            elif nToCalc == 2:
                new_key = split[2] + '/' + split[3]
            else: #nToCalc == 1:
                new_key = split[3]
        elif tsize == 5:
            if nToCalc == 3:
                new_key = split[2] + '/' + split[3] + '/' + split[4]
            elif nToCalc == 2:
                new_key = split[3] + '/' + split[4]
            else: #nToCalc == 1:
                new_key = split[4]
        elif tsize == 6:
            if nToCalc == 3:
                new_key = split[3] + '/' + split[4] + '/' + split[5]
            elif nToCalc == 2:
                new_key = split[4] + '/' + split[5]
            else: #nToCalc == 1:
                new_key = split[5]
        else: #tsize ==2:
            new_key = split[1]
        #print(key, split, new_key)
        #teamsDict2[new_key] = value
        #print(new_key,value)

        # show 20 results minimum
        # if value['rating'] <= topPercent:
        #     topPercent_count += 1
        # print("topPercent_count:", topPercent_count)
        # if topPercent_count > 20:
        # just add all if team of 2, or less than 100 teams calced? actually when nToCalc=1 better
        if nToCalc == 1:
            teamsDict2[new_key] = value
        # exclude X2 when 3 tweaks which would be like 4 (and X4 or double X2 when 2 tweaks if necessary?)
        elif value['rating'] <= topPercent and (len(value['tweaks']) < 3 or (len(value['tweaks']) == 3 and 'X' not in str(value['tweaks']))):
            teamsDict2[new_key] = value
        elif len(value['tweaks']) == 0:
            teamsDict2[new_key] = value
        elif len(value['tweaks']) == 1:
            if 'X' not in value['tweaks'][0]:
                teamsDict2[new_key] = value
        # else:
        #     teamsDict2[new_key] = value
    if(writable):
        file.close()
    # print(rsort1)

    # teamsDict2 = {'gra ste/ste fai': {'rating': 10.50, 'tweaks': ['fir', 'wat', 'ice'], 'tURs': ['fir']},
    #           'wat gro/ste fai': {'rating': 10.25, 'tweaks': ['nor', 'bug'], 'tURs': []}}

    print("Number of results output:",len(teamsDict2))
    #print("teamsDict2.items()",teamsDict2.items())
    # Get different sorts by field
    rsort1 = sorted(teamsDict2.items(), key=lambda x: x[1]['rating'])
    rsort2 = sorted(teamsDict2.items(), key=lambda x: x[1]['rating'], reverse=True)
    # psort1 = sorted(teamsDict2.items(), key=lambda x: x[0])
    # psort2 = sorted(teamsDict2.items(), key=lambda x: x[0], reverse=True)
    wsort1 = sorted(teamsDict2.items(), key=lambda x: len(x[1]['tweaks']))
    wsort2 = sorted(teamsDict2.items(), key=lambda x: len(x[1]['tweaks']), reverse=True)
    usort1 = sorted(teamsDict2.items(), key=lambda x: len(x[1]['tURs']))
    usort2 = sorted(teamsDict2.items(), key=lambda x: len(x[1]['tURs']), reverse=True)

    # export full teams data to file
    # try:
    #     with open("teams_output.csv", "w") as file:
    #         # Output sorted data
    #         i = 0
    #         while i < len(rsort1):
    #             #print(str(team))
    #             rating = str(rsort1[i][1]['rating'])
    #             team = re.sub(" ", "_", str(rsort1[i][0]))
    #             tweaksnum = str(len(rsort1[i][1]['tweaks'])) + ":"
    #             tweaks = re.sub(" ", "_", str(rsort1[i][1]['tweaks']))
    #             tweaks = re.sub("[\[',\]]", "", tweaks)
    #             tURsnum = str(len(rsort1[i][1]['tURs'])) + ":"
    #             tURs = re.sub(" ", "_", str(rsort1[i][1]['tURs']))
    #             tURs = re.sub("[\[',\]]", "", tURs)
    #             file.write(rating + " " + team + " " + tweaksnum + tweaks + " " + tURsnum + tURs + "\n")
    #             # tsv file output (simpler but maybe less programs can read)
    #             # file.write(str(rsort1[i][1]['rating']) + "\t" + str(rsort1[i][0]) + "\t" + str(rsort1[i][1]['tweaks']) + "\t" + str(rsort1[i][1]['tURs']) + "\n")
    #             i += 1
    # except:
    #     print('Warning: unable to export output to file.')
    #     return
    # print('Teams from best to worst rating output to file "teams_output.csv".')
        # for team in rsort1:
        #     #strip = str(team).strip()
        #     print(team[0], team[1][0], team[1][1], team[1][2])
        #     file.write(str(team) + "\n")
            # print(team)

    # reset allTypeMUs
    if gen >= 6:
        typeMUs = gen6typeMUs
        # print("gen6+ typeMUs reset")
    elif gen >= 2:
        typeMUs = gen2typeMUs
        # print("gen2-5 typeMUs reset")
    else:
        typeMUs = gen1typeMUs
        # print("gen1 typeMUs reset")
    allTypeMUs = copy.deepcopy(typeMUs)
    allTypeMUs_simp = copy.deepcopy(typeMUs)


# Look up effectiveness from dict
def lookupEffects(pkmn, dict):
    if pkmn.type2 == "":
        pkmn.effects = dict[pkmn.type1]
    else:
        if pkmn.types in dict:
            pkmn.effects = dict[pkmn.types]
        else:
            pkmn.effects = dict[pkmn.typesR]

# Kivy GUI -------------------------------------------------------------------------------------------------------------
class MyLayout(BoxLayout):
    teams_data = ListProperty([])
    type1_input1 = ObjectProperty(None)
    type2_input1 = ObjectProperty(None)
    type1_input2 = ObjectProperty(None)
    type2_input2 = ObjectProperty(None)
    type1_input3 = ObjectProperty(None)
    type2_input3 = ObjectProperty(None)
    type1_input4 = ObjectProperty(None)
    type2_input4 = ObjectProperty(None)
    type1_input5 = ObjectProperty(None)
    type2_input5 = ObjectProperty(None)
    gen_input = ObjectProperty(None)
    tsize_input = ObjectProperty(None)
    old_filter_input = ObjectProperty(None)
    new_filter_input = ObjectProperty(None)
    color = ColorProperty(typecolors["non"])
    submit = ObjectProperty(None)
    remove2 = ObjectProperty(None)
    remove3 = ObjectProperty(None)
    remove4 = ObjectProperty(None)
    remove5 = ObjectProperty(None)
    addT = ObjectProperty(None)
    revert = ObjectProperty(None)
    #status = ObjectProperty(None)
    rsort = ObjectProperty(None)
    #psort = ObjectProperty(None)
    wsort = ObjectProperty(None)
    usort = ObjectProperty(None)
    #tdatatext = ObjectProperty(None)
    #spinopts = ObjectProperty(size_hint_y=None, height=25)

    calculated = False
    typegen_mismatch = False
    unusedCheck = False
    validCalc = True

    Trows = 1
    Trow = 8
    addT_able = True
    TrowsTypesDict = {}
    type1_input = ""
    type2_input = ""

    def genspinner_clicked(self, gen):
        global typeMUs, allTypeMUs, allTypeMUs_simp
        spinner_types = ["none", "normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison",
                         "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon"]
        self.ids.gen_label.text = '[i]'+ genlist[int(gen)-1] + '[/i]'
        if int(gen) >= 6:
            typeMUs = gen6typeMUs
            spinner_types.extend(["dark", "steel", "fairy"])
            self.ids.type1_input1.values = spinner_types
            self.ids.type2_input1.values = spinner_types
            self.ids.new_filter_input.values = spinner_types
            self.ids.new_filter_input.values[0] = "any"
        elif int(gen) >= 2:
            typeMUs = gen2typeMUs
            spinner_types.extend(["dark", "steel"])
            self.ids.type1_input1.values = spinner_types
            self.ids.type2_input1.values = spinner_types
            self.ids.new_filter_input.values = spinner_types
            self.ids.new_filter_input.values[0] = "any"
        else:
            typeMUs = gen1typeMUs
            self.ids.type1_input1.values = spinner_types
            self.ids.type2_input1.values = spinner_types
            self.ids.new_filter_input.values = spinner_types
            self.ids.new_filter_input.values[0] = "any"
        allTypeMUs = copy.deepcopy(typeMUs)
        allTypeMUs_simp = copy.deepcopy(typeMUs)
        #print(typeMUs)
        #print(allTypeMUs)

    def tsizespinner_clicked(self, ts):
        # global tsize
        # tsize = ts
        # for child in self.children:
        #     print(child)
        # auto-remove rows so always at least 1 to calc (can still revert options to undo)
        print("Tteam size:", ts, "Typing rows:", self.Trows)
        if int(ts)-1 < self.Trows:
            Trows_diff = self.Trows+1 - int(ts)
            print("Need to remove typing rows:", Trows_diff)

            print(self.children[self.Trows])
            # self.clear_widgets(self.Trow2)
            # self.remove_widget(self.Trow2)
            i = Trows_diff
            while i > 0:
                currentTrow = self.children[self.Trow - self.Trows-1+i]
                print("i:",i,"currentTrow:",currentTrow)
                # hide typing row
                currentTrow.height, currentTrow.opacity, currentTrow.disabled = 0, 0, True
                i-=1
            self.Trows = self.Trows - Trows_diff
            print("Trows after removal:", self.Trows)
            print(self.children[self.Trows])
        # if self.tsize_input != ts:
        #     self.tsize_input = ts

    def exclude_clicked(self, instance, x):
        # instance is necessary!
        global exclude
        exclude = x

# Typing row 1----------------------------------------------------------------------------------------------------------
    def spinner1_clicked1(self, type):
        self.ids.type1_input1.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])
        #self.ids.option_cls = spinopts

    def spinner2_clicked1(self, type):
        self.ids.type2_input1.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    def press1(self):
        # Update status text before any calc
        global typegen_mismatch,unusedCheck
        gen = int(self.gen_input.text)
        typegen_mismatch = False
        unusedCheck = False

        # Check if too many to calc
        Trows_diff = int(self.tsize_input.text) - self.Trows
        print("Trows_diff:", Trows_diff)
        if Trows_diff > 3:
            self.ids.status.text = "< Error: Unable to calculate more than 3 typings! Reduce team size or add more typings. >"
            print("Error: Unable to calculate more than 3 typings! Reduce team size or add more typings.")
            self.validCalc = False
            return

        # Set dict of types by typing row while checking if input valid to calc
        self.TrowsTypesDict.clear()
        for tr in range(1, self.Trows+1):
            exec(f'self.type1_input = self.type1_input{tr}.text[:3]')
            exec(f'self.type2_input = self.type2_input{tr}.text[:3]')
            # print(self.type1_input1.text[:3])
            print('Typing row', tr, 'types:', self.type1_input, self.type2_input)
            self.TrowsTypesDict[tr] = [self.type1_input, self.type2_input]

            if self.type1_input == 'non' and self.type2_input == 'non':
                self.ids.status.text = '< No typing row ' + str(tr) + ' types! Select and submit types! >'
                print('No typing row ' + str(tr) + ' types! Select and submit types!')
                self.validCalc = False
                return
            elif (gen < 6 and (self.type1_input == "fai" or self.type2_input == "fai")) or (
                        gen == 1 and (self.type1_input in ["dar", "ste"] or self.type2_input in ["dar", "ste"])):
                typegen_mismatch = True
                self.ids.status.text = "< Error: A selected typing row " + str(tr) +" type doesn't exist this gen! >"
                print("Error: A selected typing row " + str(tr) +" type doesn't exist this gen!")
                self.validCalc = False
                return
            else:
                # swap none types
                if self.type1_input == 'non':
                    self.type1_input = self.type2_input
                    self.type2_input = 'non'
                    print("swapped none types:", self.type1_input, self.type2_input)
                    self.TrowsTypesDict[tr] = [self.type1_input, self.type2_input]
                    print("swapped none types committed to dict:", self.TrowsTypesDict[tr])

                # check for unused type selected while excluding
                if exclude:
                    if self.type2_input == 'non' or self.type1_input == self.type2_input:
                        if self.type1_input in unusedTypes[gen]:
                            unusedCheck = True
                    else:  # type1_input != 'non' and type2_input == 'non' or type1_input == type2_input:
                        if self.type1_input + ' ' + self.type2_input in unusedTypes[gen] or self.type2_input + ' ' + self.type1_input in unusedTypes[gen]:
                            unusedCheck = True

                    # print(unusedCheck)
                    if unusedCheck:
                        self.ids.status.text = "< Error: Selected row " + str(tr) + " typing unused this gen! >"
                        print("Error: Selected row " + str(tr) + " typing unused this gen!")
                        self.validCalc = False
                        return
                    else:
                        #self.submit.disabled = True
                        if Trows_diff > 2:
                            self.ids.status.text = '< Calculating (for 3 may take some minutes)... >'
                        else:
                            self.ids.status.text = '< Calculating... >'
                        self.validCalc = True
                else:
                    if Trows_diff > 2:
                        self.ids.status.text = '< Calculating (for 3 may take some minutes)... >'
                    else:
                        self.ids.status.text = '< Calculating... >'
                    self.validCalc = True

        print(self.TrowsTypesDict)

    def release1(self):
        # Check types input before calc
        gen = int(self.gen_input.text)
        tsize = int(self.tsize_input.text)
        self.calculated = False

        if self.validCalc:
            calculate(self.TrowsTypesDict, tsize, gen)
            self.calculatedText = '< Calculated! Top rated teams including ' + str(noWeakTeamsNum) + ' with no weaks, ' + str(oneWeakTeamsNum) + ' with one.' + ' >'
            self.get_dataframe(rsort1, self.calculatedText)
        else:
            print("Invalid team, not calculating.")
            return
# Typing row 2----------------------------------------------------------------------------------------------------------
    def spinner1_clicked2(self, type):
        self.ids.type1_input2.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])
        # self.ids.option_cls = spinopts

    def spinner2_clicked2(self, type):
        self.ids.type2_input2.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    # def press2(self):
    #     print("Remove typing row 2 button press")

    def release2(self):
        # note reverse children order
        thisTrow_n = 6
        lastTrow = self.children[self.Trow - self.Trows]
        # lastTrowType1 = lastTrow.children[2].text
        # lastTrowType2 = lastTrow.children[1].text
        # print("lastTrow:", lastTrow.children[3].text, lastTrowType1, lastTrowType2)

        # correct typing rows for removal
        print(self.Trows, int(self.tsize_input.text))
        Trows_diff = self.Trows - 2 # for 2nd typing row
        print("Need to correct typing rows:", Trows_diff)
        for i in range(1, Trows_diff + 1):
            if not self.children[thisTrow_n - i].disabled:
                # set this Trow type same as next
                print("CORRECTED TYPES:", i)
                self.children[thisTrow_n - i + 1].children[2].text = self.children[thisTrow_n - i].children[2].text
                self.children[thisTrow_n - i + 1].children[1].text = self.children[thisTrow_n - i].children[1].text
                # set last Trow type looped as nones
                if i == Trows_diff:
                    self.children[thisTrow_n - i].children[2].text = "none"
                    self.children[thisTrow_n - i].children[1].text = "none"

        # hide typing row
        lastTrow.height, lastTrow.opacity, lastTrow.disabled = 0, 0, True
        print("Removed row:", self.Trows)
        self.Trows -= 1
# Typing row 3----------------------------------------------------------------------------------------------------------
    def spinner1_clicked3(self, type):
        self.ids.type1_input3.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    def spinner2_clicked3(self, type):
        self.ids.type2_input3.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    def release3(self):
        # note reverse children order
        thisTrow_n = 5
        lastTrow = self.children[self.Trow - self.Trows]
        # lastTrowType1 = lastTrow.children[2].text
        # lastTrowType2 = lastTrow.children[1].text
        # print("lastTrow:", lastTrow.children[3].text, lastTrowType1, lastTrowType2)

        # correct typing rows for removal
        print(self.Trows, int(self.tsize_input.text))
        Trows_diff = self.Trows - 3 # for 3rd typing row
        print("Need to correct typing rows:", Trows_diff)
        for i in range(1, Trows_diff+1):
            if not self.children[thisTrow_n - i].disabled:
                # set this Trow type same as next
                print("CORRECTED TYPES:", i)
                self.children[thisTrow_n - i + 1].children[2].text = self.children[thisTrow_n - i].children[2].text
                self.children[thisTrow_n - i + 1].children[1].text = self.children[thisTrow_n - i].children[1].text
                # set last Trow type looped as nones
                if i == Trows_diff:
                    self.children[thisTrow_n - i].children[2].text = "none"
                    self.children[thisTrow_n - i].children[1].text = "none"

        # hide typing row
        lastTrow.height, lastTrow.opacity, lastTrow.disabled = 0, 0, True
        print("Removed row:", self.Trows)
        self.Trows -= 1
# Typing row 4----------------------------------------------------------------------------------------------------------
    def spinner1_clicked4(self, type):
        self.ids.type1_input4.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    def spinner2_clicked4(self, type):
        self.ids.type2_input4.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    def release4(self):
        # note reverse Trow order
        thisTrow = self.children[4]
        nextTrow = self.children[4 - 1]
        lastTrow = self.children[self.Trow - self.Trows]
        thisTrowType1 = thisTrow.children[2].text
        thisTrowType2 = thisTrow.children[1].text
        nextTrowType1 = nextTrow.children[2].text
        nextTrowType2 = nextTrow.children[1].text
        lastTrowType1 = lastTrow.children[2].text
        lastTrowType2 = lastTrow.children[1].text
        print("thisTrow:", thisTrow.children[3].text, thisTrowType1, thisTrowType2)
        print("nextTrow:", nextTrow.children[3].text, nextTrowType1, nextTrowType2)
        print("lastTrow:", lastTrow.children[3].text, lastTrowType1, lastTrowType2)
        # print("lastTrow.disabled:", lastTrow.disabled)
        # print(self.children[self.Trow - self.Trows - 2].disabled)
        print("nextTrow.disabled:", nextTrow.disabled)
        # if nextTrow.disabled and (nextTrowType1 != "none" or nextTrowType2 != "none"):
        # if nextTrow.disabled or (nextTrowType1 != "none" or nextTrowType2 != "none"):
        if not nextTrow.disabled:
            # set this Trow type same as next and next as nones
            print("CORRECTED TYPES")
            thisTrow.children[2].text = nextTrowType1
            thisTrow.children[1].text = nextTrowType2
            nextTrow.children[2].text = "none"
            nextTrow.children[1].text = "none"
        # hide typing row
        lastTrow.height, lastTrow.opacity, lastTrow.disabled = 0, 0, True
        print("Removed row:", self.Trows)
        self.Trows -= 1
# Typing row 5----------------------------------------------------------------------------------------------------------
    def spinner1_clicked5(self, type):
        self.ids.type1_input5.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    def spinner2_clicked5(self, type):
        self.ids.type2_input5.background_color = kivy.utils.get_color_from_hex(typecolors[type[:3]])

    def release5(self):
        # always just need to remove last typing row here
        lastTrow = self.children[self.Trow - self.Trows]
        # hide typing row
        lastTrow.height, lastTrow.opacity, lastTrow.disabled = 0, 0, True
        print("Removed row:", self.Trows)
        self.Trows -= 1
# END Typing rows-------------------------------------------------------------------------------------------------------

    # Update status text before any sort
    def sort_press(self):
        # Don't sort if no data
        if len(self.teams_data) == 0:
            self.ids.status.text = '< No data to sort! Select and submit types! >'
            return
        else:
            self.ids.status.text = '< Sorting... >'

    # Function to sort on sort button presses
    def sort_release(self, field, arrow):
        #print(field, arrow)
        # Don't sort if no data
        if len(self.teams_data) == 0:
            #no types (already updated status on press)
            return
        else:
            # Sort based on field and arrow position (could make this into loop with format/dict)
            if field == 'r':
                if arrow == '^':
                    self.rsort.text = 'v'
                    self.new_filter_input.text = 'any'
                    self.wsort.text = '-'
                    self.usort.text = '-'
                    self.get_dataframe(rsort2, '< Sorted by worst to best rating! >')
                else:
                    self.rsort.text = '^'
                    self.new_filter_input.text = 'any'
                    self.wsort.text = '-'
                    self.usort.text = '-'
                    self.get_dataframe(rsort1, '< Sorted by best to worst rating! >')
            # elif field == 'p':
            #     if arrow == '^':
            #         self.rsort.text = '-'
            #         self.psort.text = 'v'
            #         self.wsort.text = '-'
            #         self.usort.text = '-'
            #         self.get_dataframe(psort2, '< Sorted by ally pokemon types descending! >')
            #     else:
            #         self.rsort.text = '-'
            #         self.psort.text = '^'
            #         self.wsort.text = '-'
            #         self.usort.text = '-'
            #         self.get_dataframe(psort1, '< Sorted by ally pokemon types ascending! >')
            elif field == 'w':
                if arrow == '^':
                    self.rsort.text = '-'
                    self.new_filter_input.text = 'any'
                    self.wsort.text = 'v'
                    self.usort.text = '-'
                    self.get_dataframe(wsort2, '< Sorted by most to least weaknesses! >')
                else:
                    self.rsort.text = '-'
                    self.new_filter_input.text = 'any'
                    self.wsort.text = '^'
                    self.usort.text = '-'
                    self.get_dataframe(wsort1, '< Sorted by least to most weaknesses! >')
            else:
                if arrow == '^':
                    self.rsort.text = '-'
                    self.new_filter_input.text = 'any'
                    self.wsort.text = '-'
                    self.usort.text = 'v'
                    self.get_dataframe(usort2, '< Sorted by most to least unresists! >')
                else:
                    self.rsort.text = '-'
                    self.new_filter_input.text = 'any'
                    self.wsort.text = '-'
                    self.usort.text = '^'
                    self.get_dataframe(usort1, '< Sorted by least to most unresists! >')

    def filter_clicked(self):
        # Don't filter if no data
        new_filter_input_unabv = self.new_filter_input.text
        new_filter_input = new_filter_input_unabv[:3]

        if len(self.teams_data) == 0:
            self.ids.status.text = '< No data to filter! Select and submit types! >'
            return
        elif new_filter_input == self.old_filter_input:
            # no need to change or filter anything
            return
        else:
            self.old_filter_input = new_filter_input
            self.ids.status.text = '< Filtering... >'
            self.rsort.text = '-'
            self.wsort.text = '-'
            self.usort.text = '-'
            if new_filter_input == 'any':
                self.get_dataframe(rsort1, '< Sorted by best to worst rating! >')
            else:
                pfilter = list(filter(lambda x: new_filter_input in x[0], teamsDict2.items()))
                if len(pfilter) == 0:
                    self.ids.status.text = '< No filterable ' + new_filter_input_unabv + ' type allies in top rated teams! >'
                    return
                else:
                    self.get_dataframe(pfilter, '< Filtered by allies with ' + new_filter_input_unabv + ' type! >')
                    print("Number filtered:", len(pfilter))

    # def filter_press(self):
    #     # Don't filter if no data
    #     filter_input = self.filter_input.text
    #
    #     if len(self.teams_data) == 0:
    #         self.ids.status.text = '< No data to filter! Select and submit types! >'
    #         return
    #     else:
    #         self.ids.status.text = '< Filtering... >'

    def addT_press(self):
        if self.Trows < int(self.tsize_input.text)-1:
            self.addT_able = True
            print("Ok to add row:", self.Trows+1)
        else:
            self.addT_able = False
            self.ids.status.text = f'< Unable to add typing row {self.Trows+1} based on team size! >'
            print("Unable to add row:", self.Trows+1)

    def addT_release(self):
        #global Trow2
        if self.addT_able:
            self.Trows += 1
            #print("test", self.children[3].children[3].text)
            # for child in self.children:
            #     # print(child)
            #     try:
            #         print(child.children[3].text)
            #     except:
            #         print("child with no text")
            currentTrow = self.children[self.Trow-self.Trows]
            # print("child at:", currentTrow)
            # unhide typing row
            # height isn't updating correctly on device, should be 40 but trying 80 to account for shortening
            # problem may be different across devices?
            currentTrow.height, currentTrow.opacity, currentTrow.disabled = 80, 1, False
            print("Added row:", self.Trows)

    # def revert_release(self):
    #     # revert settings to last calced on button release
    #     # problem is how to update other widgets... leave for next version
    #     self.tsizespinner_clicked('2')
    #     print("Reverted settings to last calced.")

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        #self.ids.status.text = 'Initialized. Select and submit types!'

    # Function to update sorted data
    def get_dataframe(self, currentsort, message):
        # Clear previous data
        self.teams_data = []
        #self.tdatatext.font_size = sp(10)

        # Output sorted data, with type color markups
        #[\['\]]|ing|tric|on|chic|al|nd
        i = 0
        while i < len(currentsort):
            rating = str(currentsort[i][1]['rating'])
            self.teams_data.append({'text': rating, 'index': rating, 'size_hint_x': None, 'width': kivy.metrics.dp(35), 'font_size': kivy.metrics.sp(10)})
            team = currentsort[i][0]
            #print(team)
            for key, value in typecolors.items():
                team = re.sub(str(key), str("[color="+str(value)+"]"+str(key)+"[/color]"), str(team))
            self.teams_data.append({'markup': True, 'text': team, 'index': team, 'font_size': kivy.metrics.sp(10)})
            tweaks = re.sub("[\['\]]", "", str(currentsort[i][1]['tweaks']))
            for key, value in typecolors.items():
                tweaks = re.sub(str(key), str("[color=" + str(value) + "]" + str(key) + "[/color]"), str(tweaks))
            self.teams_data.append({'markup': True, 'text': tweaks, 'index': tweaks, 'font_size': kivy.metrics.sp(10)})
            tURs = re.sub("[\['\]]", "", str(currentsort[i][1]['tURs']))
            for key, value in typecolors.items():
                tURs = re.sub(str(key), str("[color=" + str(value) + "]" + str(key) + "[/color]"), str(tURs))
            self.teams_data.append({'markup': True, 'text': tURs, 'index': tURs, 'font_size': kivy.metrics.sp(8)}) #, 'text_size': self.size
            i+=1
        self.teams_data.append({'text': '', 'index': '', 'size_hint_x': None, 'width': kivy.metrics.dp(35)})
        #print(self.teams_data)
        self.ids.status.text = message
        if not self.calculated:
            self.rsort.text = '^'
            self.new_filter_input.text = 'any'
            self.wsort.text = '-'
            self.usort.text = '-'
        #self.submit.disabled = False
        self.calculated = True


# class MyClass(EventDispatcher):
#     status = ObjectProperty(None)
#
#     def on_a(self, instance, value):
#         app = App.get_running_app()
#         app.status.text = str(value)
#
# def callback(instance, value):
#     print('My callback is call from', instance)
#     print('and the a value changed to', value)
#
# ins = MyClass()
# ins.bind(status=callback)

class main(App):
    def build(self):
        # test ad banner
        # self.ads = KivMob('ca-app-pub-3940256099942544~3347511713')
        # self.ads.new_banner('ca-app-pub-3940256099942544/6300978111', top_pos=False)
        self.ads = KivMob('ca-app-pub-9314162462794737~2460228955')
        self.ads.new_banner('ca-app-pub-9314162462794737/6084613346', top_pos=False)
        self.ads.request_banner()
        self.ads.show_banner()
        #initialize()
        return MyLayout()

    # def hide_widget(wid, dohide=True):
    #     if hasattr(wid, 'saved_attrs'):
    #         if not dohide:
    #             wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
    #             del wid.saved_attrs
    #     elif dohide:
    #         wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
    #         wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

if __name__ == "__main__":
    main().run()