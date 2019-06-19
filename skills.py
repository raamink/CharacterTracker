"""File containing class definitions for things on the character sheet, like skills, feats, etc"""

# Toggle for printing in commands of the different methods. Disabled by default.
PRINTING = False 

# Saved me writing hundreds of quotation marks. That was a pain I rather avoid.
Int = 'Int'
Cha = 'Cha'
Str = 'Str'
Dex = 'Dex'
Con = 'Con'
Wis = 'Wis'


class bonus:
    """Contains placeholders for all the bonus types. Attempting to make a base bonus class.
    This is useful for when trying to see which bonuses to add (type bonuses, stacking, etc)."""

    def __init__(self, name, **kwargs):
        self.name = name
        self.AbilMod = 0
        self.Alchemical = 0
        self.Armour = 0
        self.Circumstance = 0
        self.Competence = 0
        self.Deflection = 0
        self.Dodge = []
        self.Enhancement = 0
        self.Insight = 0
        self.Luck = 0
        self.Morale = 0
        self.NaturalArmour = 0
        self.Profane = 0
        self.Racial = 0
        self.Resistance = 0
        self.Sacred = 0
        self.Shield = 0
        self.Size = 0
        self.group = None

    def __call__(self):
        variable = self.Circumstance + self.Competence + self.Insight + self.Luck \
            + self.Morale + self.Profane + self.Sacred
        if self.group == 'Armour':
            return self.Armour + self.NaturalArmour + self.Enhancement \
                + self.Deflection + self.Shield + sum(self.Dodge) \
                + variable
        elif self.group == 'Weapon':
            return self.AbilMod + self.Enhancement + self.Racial + self.Size + variable
        elif self.group == 'Skill':
            return self.AbilMod + self.Racial + variable
        elif self.group == 'Other':
            raise NotImplementedError
        else:
            return None


class skill():
    '''Class for skills. Methods for training, modifying and sundry will be attached
    
    A single skill instance can be called with minimal data by invoking it's name and associated ability.
    It returns the bonus when called, assuming untrained use is allowed. Otherwise None
    
    >>> a = skill("Decipher Script", "Int", useUntrained = False)
    >>> print(a())
    None
    >>> a.train(3)
    >>> a()
    1
    >>> a.train(1)
    >>> a.ranks
    4
    >>> a()
    2
    >>> a.classSkill = True
    >>> a.train(1)
    >>> a()
    3
    >>> 
    
    Missing parts of the class are:
     - loading in ability modifier
     - elegant size modifier resolution
     - elegant Armour check penalty resolution
     - a reliable training resolution
     - Splitting of Knowledge/Perform/Profession/Craft into subskills
     - Add spaces to skill names when actually multiple words (marked by CamelCase)
    
    '''

    def __init__(self, name, ability, *ignored, **defaults):
        """
        Initialises the absolute minimum requirements to track a skill. 
        
        Assumes average case, so not a class skill, can use untrained, 
        doesn't have ACP and no random bonuses.
        
        Takes as an input the following: 
         - Name of skill
         - Three letter string representation of ability modifier (Str, Int, etc.)
         - Any other defaults you feel like overriding, but as a keyword pair
            * Size of character (e.g. size=L) [to be implemented]
            * Armour Check Penalty (e.g ACP=True, ACPMod = 3) [t.b.i.]
            * Miscelaneous modifiers like a racial bonus: miscMod=2
            * if it's a class skill: classSkill = True
        
        *Spurious inputs that get added are not used for any calculations.*
        """
        self.name = name
        self.type = 'skill'
        self.abil = ability
        self.abilMod = 0
        self.size = False
        self.sizeMod = 4
        self.ACP = False
        self.ACPMod = 0
        self.ranks = 0
        self.miscMod = 0
        self.useUntrained = True
        self.classSkill = False
        self.setMaxRanks(1)                         # Defaults to Character Level 1
        self.__dict__.update(defaults)

    def setMaxRanks(self, CharLevel):
        if self.classSkill:
            self.maxRanks = CharLevel + 3
        else:
            self.maxRanks = (CharLevel + 3) / 2

    def investPoints(self, pointsSpending):
        """
        Raises the amount of ranks you have in a skill. Returns the remaining skill points.
        Calculates how much points you're allowed to spend training the skill and ranks it
        that far. 
        """
        # Sets up calculations to work on amount of skill points, not on skill ranks.
        if self.classSkill:
            scaling = 1
        else:
            scaling = 2
        maxrank = self.maxRanks * scaling
        actualranks = self.ranks * scaling

        # Finds out if the maximum rank is achieved. If yes, then calculates the amount of leftover skillpoints
        test = actualranks + pointsSpending
        if test > maxrank:
            overflow = test - maxrank
        else:
            overflow = 0

        self.ranks = min(maxrank, test) / scaling
        if PRINTING:
            print("{} now has {} ranks.".format(self.name, self.ranks))
        return overflow

    def bonus(self):
        if self.useUntrained or self.ranks != 0:
            return int(self.ranks + self.abilMod + self.miscMod + self.size * self.sizeMod + self.ACP + self.ACPMod)
        else:
            return None

    def toggleClassSkill(self):
        self.classSkill = not self.classSkill
        if self.classSkill:
            self.maxRanks *= 2
        else:
            self.maxRanks /= 2
        if PRINTING:
            print("CS: {} \t maxRanks: {}".format(self.classSkill, self.maxRanks))

    def toggleUntrained(self):
        self.useUntrained = not self.useUntrained
        if PRINTING:
            print(f'The skill {self.name} is usable untrained: {self.useUntrained}')

    def __call__(self):
        return self.bonus()

    def __repr__(self):
        return "{} is currently trained to {} ranks of maximum {}".format(self.name, self.ranks, self.maxRanks)


class skillList:
    def __init__(self):
        self._skills = ["Appraise", "Balance", "Bluff", 'Climb', 'Craft', 'Concentration',
                        'DecipherScript', 'Diplomacy', 'DisableDevice', 'Disguise',
                        'EscapeArtist', 'Forgery', 'GatherInformation', 'HandleAnimal',
                        'Heal', 'Hide', 'Intimidate', 'Jump', 'Knowledge', 'Listen',
                        'MoveSilently', 'OpenLock', 'Perform', 'Profession', 'Ride',
                        'Search', 'SenseMotive', 'SleightofHand', 'Spellcraft', 'Spot',
                        'Survival', 'Swim', 'Tumble', 'UseMagicDevice', 'UseRope']
        _skills = self._skills
        _ClassSkills = ["Bluff", 'Climb']
        _abils = [Int, Dex, Cha, Str, Int, Con,
                  Int, Cha, Int, Cha,
                  Dex, Int, Cha, Cha,
                  Wis, Dex, Cha, Str, Int, Wis,
                  Dex, Dex, Cha, Wis, Dex,
                  Int, Wis, Dex, Int, Wis,
                  Wis, Str, Dex, Cha, Dex]
        for i in range(len(_skills)):
            setattr(self, _skills[i], skill(_skills[i], _abils[i]))
        self.setClassSkills(_ClassSkills)
        self._skillPointsAvailable = 0
        self._skillPointsSpent = 0

    def setClassSkills(self, ClassSkillList):
        for CS in ClassSkillList:
            self.__dict__[CS].toggleClassSkill()

    def maxRanks(self, lvl):
        for skill in Skills:
            self.__dict__[skill].setMaxRanks(lvl)
            
    def addSkill(self, Skill):
        if Skill.name not in self._skills:
            setattr(self, Skill.name, Skill)
            self._skills.append(Skill.name)
            self._skills.sort()
        else:
            if PRINTING: 
                print('Already in list')

    def goUpALevel(self, skillsPointsGained):
        self._skillPointsAvailable = skillsPointsGained
        options = 0
        for skill in self._skills:
            pass

    def __repr__(self):
        representation = ''
        for i in range(len(self._skills)):
            SkillName = self._skills[i]
            SkillBonus = self.__dict__[SkillName].bonus()
            SkillClass = self.__dict__[SkillName].classSkill
            representation += f"Name : {SkillName.ljust(20)}\tBonus : {SkillBonus}\tClass Skill: : {SkillClass}\n"
        return representation


if __name__ == '__main__':
    a = skill('Appraise', 'Int')
    A = skillList()
    PRINTING = True
