# ids and ordering taken from lastepochtools (window.classSkillSources / masterySkillSources)
import json
CLASSES = [  # classId, key, i18n class name key, masteries in game order (mastery 1..3)
 (0,'primalist','Primalist',[('beastmaster','Beastmaster','Beastmaster'),('shaman','Shaman','Shaman'),('druid','Druid','Druid')]),
 (1,'mage','Mage',[('sorcerer','Sorcerer','Sorcerer'),('spellblade','Spellblade','Spellblade'),('runemaster','Runemaster','Runemaster')]),
 (2,'sentinel','Sentinel',[('void-knight','Void Knight','VoidKnight'),('forge-guard','Forge Guard','ForgeGuard'),('paladin','Paladin','Paladin')]),
 (3,'acolyte','Acolyte',[('necromancer','Necromancer','Necromancer'),('lich','Lich','Lich'),('warlock','Warlock','Warlock')]),
 (4,'rogue','Rogue',[('bladedancer','Bladedancer','Bladedancer'),('marksman','Marksman','Marksman'),('falconer','Falconer','Falconer')]),
]
DESC_KEY = {'runemaster':'UI.MasteryPanel_Runemaster_Description','void-knight':'UI.Mastery_VoidKnight_Description','forge-guard':'UI.Mastery_Forge_Guard_Description'}
BONUS_PREFIX = {'runemaster':'UI.PassiveTree_Panel_Runemaster'}
LANGS = ['en','de','es','fr','ja','ko','pl','pt','ru','zh']
