from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "robloxvault2026secretkey"
if os.environ.get("RENDER"):
    DB = os.path.join("/tmp", "codes.db")
else:
    DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes.db")

# === ADD A NEW PASSWORD FOR EACH PERSON WHO PAYS ₹10 ===
PREMIUM_PASSWORDS = [
    "PARTH001",   # Person 1 - test
    # "RIYA002",  # uncomment and add more as people pay
]
# ========================================================

ROBLOX_GAMES = [
    "Blox Fruits", "Anime Card Clash", "Bubble Gum Simulator",
    "Basketball Zero", "Blue Lock: Rivals", "Pet Simulator X",
    "Pet Simulator 99", "Shindo Life", "Anime Defenders",
    "Grand Piece Online", "King Legacy", "Fisch",
    "Fruit Battlegrounds", "AUT (A Universal Time)", "Peroxide",
    "Jailbreak", "Adopt Me!", "Murder Mystery 2", "Tower of Hell",
    "Brookhaven", "Royale High", "Doors", "Anime Adventures",
    "Sol's RNG", "Arcane Odyssey", "Muscle Legends", "Dragon Blox",
    "Ninja Legends", "Work at a Pizza Place", "Volleyball Legends", "Rivals", "Evade", "Hypershot", "Arm Wrestle Simulator", "Waste Time", "Tap Simulator", "Yeet a Friend", "Youtube Simulator Z", "Anime Vanguards", "99 Nights in the Forest", "Destroy Grandma", "Bed Wars", "Driving Empire", "Anime Infinity", "Basketball Legends", "Deathball", "Other"
]

PREMIUM_GAMES = [
    "Genshin Impact", "Honkai Star Rail", "Pokemon GO", "AFK Arena", "Mech Arena"
]

GAMES = ROBLOX_GAMES + PREMIUM_GAMES

PRELOADED_CODES = [
    # Blox Fruits
    ("LIGHTNINGABUSE", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("KITT_RESET", "Blox Fruits", "Free Stat Refund", ""),
    ("CHANDLER", "Blox Fruits", "Redeem for $0 (joke code)", ""),
    ("SUB2CAPTAINMAUI", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Enyu_is_Pro", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Starcodeheo", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Sub2Fer999", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Magicbus", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("JCWK", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("kittgaming", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Bluxxy", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("fudd10_v2", "Blox Fruits", "Redeem for $2", ""),
    ("SUB2GAMERROBOT_EXP1", "Blox Fruits", "2x EXP for 30 minutes", ""),
    ("SUB2GAMERROBOT_RESET1", "Blox Fruits", "Free Stat Refund", ""),
    ("Sub2UncleKizaru", "Blox Fruits", "Free Stat Refund", ""),
    ("Axiore", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Sub2Daigrock", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Bignews", "Blox Fruits", "In-game Title: Big News", ""),
    ("Sub2NoobMaster123", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("StrawHatMaine", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("TantaiGaming", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("TheGreatAce", "Blox Fruits", "2x EXP for 20 minutes", ""),
    ("Fudd10", "Blox Fruits", "Redeem for $1", ""),
    ("Sub2OfficialNoobie", "Blox Fruits", "2x EXP for 20 minutes", ""),

    # Anime Card Clash
    ("3UPDATE6", "Anime Card Clash", "New update reward", ""),
    ("2UPDATE6", "Anime Card Clash", "New update reward", ""),
    ("1UPDATE6", "Anime Card Clash", "New update reward", ""),
    ("0ROLLSCHALLENGE", "Anime Card Clash", "Rolls challenge reward", ""),
    ("PREANNIVERSARY6", "Anime Card Clash", "Pre-anniversary reward", ""),
    ("PREANNIVERSARY5", "Anime Card Clash", "Pre-anniversary reward", ""),
    ("PREANNIVERSARY4", "Anime Card Clash", "Pre-anniversary reward", ""),
    ("PREANNIVERSARY3", "Anime Card Clash", "Pre-anniversary reward", ""),
    ("PREANNIVERSARY2", "Anime Card Clash", "Pre-anniversary reward", ""),
    ("PREANNIVERSARY1", "Anime Card Clash", "Pre-anniversary reward", ""),

    # Bubble Gum Simulator
    ("ogbgs", "Bubble Gum Simulator", "3x Infinity Elixir", ""),
    ("throwback", "Bubble Gum Simulator", "3x Eggs Elixir", ""),
    ("halloween", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("obby", "Bubble Gum Simulator", "Obby keys and crates", ""),
    ("milestones", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("season7", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("update18", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("update17", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("update16", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("onemorebonus", "Bubble Gum Simulator", "1 of each Infinity Potion and 5 Secret Elixir", ""),
    ("update15", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("world3", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("fishe", "Bubble Gum Simulator", "Secret and Infinity Elixir", ""),
    ("update13", "Bubble Gum Simulator", "12x Infinity Elixir", ""),
    ("update12", "Bubble Gum Simulator", "12x Infinity Elixir", ""),
    ("update11", "Bubble Gum Simulator", "10x Infinity Elixir", ""),
    ("update10", "Bubble Gum Simulator", "12x Infinity Elixir", ""),
    ("update9", "Bubble Gum Simulator", "3x Light Box, 3x Egg Elixir, 5x Mythic Evolved", ""),
    ("update8", "Bubble Gum Simulator", "3x Infinity Elixir", ""),
    ("update6", "Bubble Gum Simulator", "2x Infinity Elixir and 3x Ancient Token", ""),
    ("update5", "Bubble Gum Simulator", "2x Infinity Elixir", ""),
    ("update4", "Bubble Gum Simulator", "2x Infinity Elixir and 5x Mystery Box", ""),
    ("sylentlyssorry", "Bubble Gum Simulator", "3x Infinity Elixir, 1x Giant Dice, 1x Golden Dice", ""),
    ("update3", "Bubble Gum Simulator", "2x Dice and 2x Giant Dice", ""),
    ("update2", "Bubble Gum Simulator", "5 Mystery Gifts", ""),
    ("Easter", "Bubble Gum Simulator", "4 Mystery Gifts", ""),
    ("Release", "Bubble Gum Simulator", "1 Mystery Gift", ""),
    ("Lucky", "Bubble Gum Simulator", "1 Luck Potion", ""),

    # Basketball Zero
    ("CHROLLOVSTATLIS", "Basketball Zero", "20 Lucky Spins, 50,000 Money", ""),
    ("30CHROLLOVSTATLIS", "Basketball Zero", "25 Lucky Spins, 100,000 Money", ""),
    ("1HRCHROLLOVSTATLIS", "Basketball Zero", "30 Lucky Spins, 150,000 Money", ""),
    ("EXTRASPINS", "Basketball Zero", "Lucky Spins", ""),
    ("IMINYOURWALLS", "Basketball Zero", "Lucky Spins", ""),

    # Blue Lock: Rivals
    ("NELSORRY", "Blue Lock: Rivals", "10 Lucky Style Spins", ""),
    ("RIPGENERATIONAL", "Blue Lock: Rivals", "10 Lucky Style Spins", ""),
    ("ISAGIEVOLUTION", "Blue Lock: Rivals", "5 Lucky Style Spins", ""),
    ("NAGIEVOLUTION", "Blue Lock: Rivals", "5 Lucky Flow Spins", ""),

    # Shindo Life
    ("RELLGIFTsc!", "Shindo Life", "Gift reward", ""),
    ("RELLGIFTbag!", "Shindo Life", "Gift reward", ""),
    ("Year5ShindoLife!", "Shindo Life", "5 Year Anniversary reward", ""),
    ("5YearsReleased!", "Shindo Life", "5 Year Anniversary reward", ""),
    ("5YearsOfShindoLife!", "Shindo Life", "5 Year Anniversary reward", ""),
    ("5YearSL2!", "Shindo Life", "5 Year Anniversary reward", ""),
    ("ShindoLife5YearCodes!", "Shindo Life", "5 Year Anniversary reward", ""),
    ("ITSBeen5Years!", "Shindo Life", "5 Year Anniversary reward", ""),
    ("ThankYouAllTruly!", "Shindo Life", "Thank you reward", ""),
    ("TimeFliesForFiveYears!", "Shindo Life", "Anniversary reward", ""),
    ("ItrulyDOMissTheseTimes!", "Shindo Life", "Bonus reward", ""),
    ("ButWelooktowardThe!", "Shindo Life", "Bonus reward", ""),
    ("FutureAndRELLSeas!", "Shindo Life", "Bonus reward", ""),
    ("IsTheNextinLine!", "Shindo Life", "Bonus reward", ""),
    ("ItsTrulyLegendary!", "Shindo Life", "Bonus reward", ""),
    ("OneOfaKind!", "Shindo Life", "Bonus reward", ""),
    ("ThisPlatformaintReady!", "Shindo Life", "Bonus reward", ""),
    ("TheCommunitygonnaEat!", "Shindo Life", "Bonus reward", ""),
    ("BoredomWillBeRescued!", "Shindo Life", "Bonus reward", ""),
    ("WePerfectedRELLSeas!", "Shindo Life", "Bonus reward", ""),
    ("forTheFuture!", "Shindo Life", "Bonus reward", ""),
    ("ofOurGames!", "Shindo Life", "Bonus reward", ""),
    ("WeGotaLotofTestingtoDo!", "Shindo Life", "Bonus reward", ""),
    ("beforeWerecord!", "Shindo Life", "Bonus reward", ""),
    ("RELLSeasMovie3!", "Shindo Life", "Bonus reward", ""),
    ("theWorkloadSeems!", "Shindo Life", "Bonus reward", ""),
    ("neverENDING!", "Shindo Life", "Bonus reward", ""),
    ("RELLbrothr3n!", "Shindo Life", "Bonus reward", ""),
    ("godd00dupdate!", "Shindo Life", "Bonus reward", ""),
    ("mansUPDATEalreadyg0d!", "Shindo Life", "Bonus reward", ""),
    ("updateDEtingMon!", "Shindo Life", "Bonus reward", ""),
    ("rellseasmoviehuh!", "Shindo Life", "Bonus reward", ""),
    ("RellenSparrow!", "Shindo Life", "Bonus reward", ""),
    ("pr3ssdeUPDATEbotton!", "Shindo Life", "Bonus reward", ""),
    ("nofampressopdatebotton!", "Shindo Life", "Bonus reward", ""),
    ("RELLseasmovie37!", "Shindo Life", "Bonus reward", ""),
    ("updateshindoOMG!", "Shindo Life", "Bonus reward", ""),
    ("updateb0ttonfam!", "Shindo Life", "Bonus reward", ""),
    ("wenrellseasmatewen!", "Shindo Life", "Bonus reward", ""),
    ("marchfam2025!", "Shindo Life", "Bonus reward", ""),
    ("fampressdeupdatebotton!", "Shindo Life", "Bonus reward", ""),
    ("rellseasmove3when!", "Shindo Life", "Bonus reward", ""),
    ("Apr1lF00lc00l!", "Shindo Life", "Bonus reward", ""),
    ("UPopUpd4te!", "Shindo Life", "Bonus reward", ""),
    ("RELLtopbrothers!", "Shindo Life", "Bonus reward", ""),
    ("updopdateop!", "Shindo Life", "Bonus reward", ""),
    ("justupdgamefam!", "Shindo Life", "Bonus reward", ""),
    ("DragonScammer!", "Shindo Life", "Bonus reward", ""),
    ("RELLbestBrothers!", "Shindo Life", "Bonus reward", ""),
    ("Merry2024Christmas!", "Shindo Life", "Christmas reward", ""),
    ("2025RELLmas!", "Shindo Life", "Christmas reward", ""),
    ("HappyHolidaysfromRELL!", "Shindo Life", "Holiday reward", ""),
    ("FixG4me239!", "Shindo Life", "Bonus reward", ""),
    ("Gem239!", "Shindo Life", "Gem reward", ""),
    ("2024NovCodes!", "Shindo Life", "November reward", ""),
    ("RELLbadBirthday!", "Shindo Life", "Birthday reward", ""),
    ("NovemberVM!", "Shindo Life", "November reward", ""),
    ("PlannedConcepts!", "Shindo Life", "Bonus reward", ""),
    ("Co0lConceptsbr0!", "Shindo Life", "Bonus reward", ""),
    ("siCkConceptsBr0!", "Shindo Life", "Bonus reward", ""),
    ("NoVeMmentality!", "Shindo Life", "Bonus reward", ""),
    ("S0back2025!", "Shindo Life", "Bonus reward", ""),
    ("r311SeasBigUps!", "Shindo Life", "Bonus reward", ""),
    ("RELLNindonSeas!", "Shindo Life", "Bonus reward", ""),
    ("BigManTingsTesting!", "Shindo Life", "Bonus reward", ""),
    ("NoMoremessingOnlyGrinding!", "Shindo Life", "Bonus reward", ""),

    # Anime Defenders
    ("merrychristmas", "Anime Defenders", "1000x Snowflakes", ""),
    ("hollydefenders", "Anime Defenders", "1 Exclusive Wish", ""),
    ("xmassoon", "Anime Defenders", "5x Divine Trait Crystals", ""),
    ("REDONE", "Anime Defenders", "1 Exclusive Wish", ""),
    ("ELEMENTS", "Anime Defenders", "1000 Ancient Relics", ""),
    ("SKILLTREES", "Anime Defenders", "5x Divine Trait Crystals", ""),
    ("subcool", "Anime Defenders", "50 Gems", ""),
    ("sub2toadboigaming", "Anime Defenders", "50 Gems", ""),
    ("sub2mozking", "Anime Defenders", "50 Gems", ""),
    ("sub2karizmaqt", "Anime Defenders", "50 Gems", ""),
    ("sub2jonaslyz", "Anime Defenders", "50 Gems", ""),
    ("sub2riktime", "Anime Defenders", "50 Gems", ""),
    ("sub2nagblox", "Anime Defenders", "50 Gems", ""),

    # Grand Piece Online
    ("CupidQueenEXP", "Grand Piece Online", "2x EXP boost", ""),
    ("CupidQueenDrops", "Grand Piece Online", "2x Drop boost", ""),
    ("RumblingDelay_1", "Grand Piece Online", "Delay compensation reward", ""),
    ("RumblingDelay_2", "Grand Piece Online", "Delay compensation reward", ""),
    ("RumblingDelay_3", "Grand Piece Online", "Delay compensation reward", ""),
    ("PRESTIGEWORLDENDERGRIND2!!", "Grand Piece Online", "Prestige grind reward", ""),
    ("PRESTIGEWORLDENDERGRIND!!", "Grand Piece Online", "Prestige grind reward", ""),
    ("HALLOWEENPART22XEXP", "Grand Piece Online", "2x EXP boost", ""),
    ("HEADLESSRACEREROLLS", "Grand Piece Online", "Race rerolls", ""),
    ("HALLOWEEN20252XDROPCODE", "Grand Piece Online", "2x Drop boost", ""),
    ("HALLOWEEN2025RACEREROLLCODE", "Grand Piece Online", "Race rerolls", ""),
    ("HALLOWEEN20252SPRESET", "Grand Piece Online", "Stat reset", ""),
    ("HALLOWEEN20252XEXP", "Grand Piece Online", "2x EXP boost", ""),
    ("REAL10FREERACEREROLLS", "Grand Piece Online", "10 Free race rerolls", ""),
    ("10FREERACEREROLLS!!!", "Grand Piece Online", "10 Free race rerolls", ""),
    ("FREE2XDROP!!", "Grand Piece Online", "2x Drop boost", ""),
    ("FREE2XEXP!!!!", "Grand Piece Online", "2x EXP boost", ""),
    ("1MILLIONLIKESRACEREROLLS", "Grand Piece Online", "Race rerolls", ""),
    ("1MILLIONLIKES2XDROP", "Grand Piece Online", "2x Drop boost", ""),
    ("1MILLIONLIKESSPRESET", "Grand Piece Online", "Stat reset", ""),
    ("ValentinesSoon_1", "Grand Piece Online", "Valentine reward", ""),
    ("ValentinesSoon_2", "Grand Piece Online", "Valentine reward", ""),
    ("MERRYCHRISTMAS2025_1", "Grand Piece Online", "Christmas reward", ""),
    ("MERRYCHRISTMAS2025_2", "Grand Piece Online", "Christmas reward", ""),
    ("PHOGIVING20252XEXP", "Grand Piece Online", "2x EXP boost", ""),
    ("PHOGIVING20252XDROPS", "Grand Piece Online", "2x Drop boost", ""),
    ("HALLOWEENPART32XEXP", "Grand Piece Online", "2x EXP boost", ""),
    ("1MILLIONLIKES2XEXP", "Grand Piece Online", "2x EXP boost", ""),

    # King Legacy
    ("FreePterSpin", "King Legacy", "10x Copper Key", ""),
    ("SKGames", "King Legacy", "2x EXP for 30 minutes", ""),
    ("RainbowDragon", "King Legacy", "100 Gems", ""),
    ("DragonColorRefund", "King Legacy", "50 Gems", ""),
    ("WELCOMETOKINGLEGACY", "King Legacy", "2x EXP for 30 minutes", ""),
    ("<3LEEPUNGG", "King Legacy", "2x EXP for 30 minutes", ""),
    ("FREESTATSRESET", "King Legacy", "Free Stat Refund", ""),
    ("2MFAV", "King Legacy", "Free Stat Refund", ""),
    ("Peodiz", "King Legacy", "100k Cash", ""),
    ("DinoxLive", "King Legacy", "100k Cash", ""),

    # Fisch
    ("SeventhOfMarch!", "Fisch", "Frigid Beauty Rod Skin", ""),
    ("JungleExpansion", "Fisch", "500 Coins, 5x Thorn Cluster, Random Item", ""),
    ("JungleExpansionSOON", "Fisch", "1111 Coins, Forestwing Rod Skin, 5x Thorn Cluster", ""),
    ("JOUNCE", "Fisch", "Chroma Blade of Glorp Skin", ""),
    ("BIGGLE", "Fisch", "1x Garbage", ""),
    ("Brinestorm", "Fisch", "Flamemourner Rod skin", ""),
    ("Tidefall", "Fisch", "Tiny Fabulous Rod skin and Random Hunt Totem", ""),
    ("Astraeus", "Fisch", "Shadow Pole Rod skin for the North Pole rod", ""),
    ("scarlet", "Fisch", "Scarlet skin for Nate's Blade", ""),
    ("TemporarySubmarine", "Fisch", "Submarine parts", ""),
    ("CARBON", "Fisch", "Free Carbon bobber", ""),

    # Fruit Battlegrounds
    ("ITSTHEBILLION!", "Fruit Battlegrounds", "600 Gems", ""),
    ("CODEFIX", "Fruit Battlegrounds", "Title", ""),

    # AUT
    ("GAROU", "AUT (A Universal Time)", "Reward", ""),
    ("BEOWULF", "AUT (A Universal Time)", "Reward", ""),

    # Peroxide
    ("ValentinesDay", "Peroxide", "50 Product Essence", ""),
    ("TheFirstDayOfWinter", "Peroxide", "50 Product Essence", ""),
    ("EvilWarlordTriumph", "Peroxide", "30 Product Essence", ""),
    ("HappyThanksgiving2025", "Peroxide", "30 Product Essence", ""),
    ("MayIngusRest", "Peroxide", "10 Product Essence and Dullahan Accessory", ""),
    ("TheEvilHalloweenDuper", "Peroxide", "50 Product Essence", ""),
    ("YayAHalloweenUpdate", "Peroxide", "10 Halloween Candy and 20 Product Essence", ""),

    # Jailbreak
    ("1bluebird", "Jailbreak", "25,000 Cash (1 hour limit)", ""),
    ("YoutubeHelloItsVG", "Jailbreak", "HelloItsVG Tire Sticker", ""),
    ("YoutubeNoobFreak", "Jailbreak", "NoobFreak Tire Sticker", ""),

    # Brookhaven
    ("1836448915", "Brookhaven", "Music: Irish Flute 30", ""),
    ("5776344796", "Brookhaven", "Music: Jujutsu Kaisen OP - Eve", ""),
    ("926493242", "Brookhaven", "Music: Chill Jazz", ""),
    ("915288747", "Brookhaven", "Music: Oofing in the 90s", ""),
    ("591276362", "Brookhaven", "Music: BTS Fire", ""),
    ("7020008209", "Brookhaven", "Music: iCarly freestyle", ""),
    ("131154740", "Brookhaven", "Music: Harlem Shake", ""),
    ("1837879082", "Brookhaven", "Music: Paradise Falls", ""),
    ("398159550", "Brookhaven", "Music: Nightcore (Titanium)", ""),
    ("169360242", "Brookhaven", "Music: Banana Song", ""),
    ("2862170886", "Brookhaven", "Music: Old Town Road", ""),
    ("130762736", "Brookhaven", "Music: Dubstep Remix", ""),
    ("6691673908", "Brookhaven", "Music: Rock - Dreams ft. Young Thug", ""),
    ("135308045", "Brookhaven", "Music: Sad Violin", ""),
    ("587156015", "Brookhaven", "Music: Nightcore - Light Em Up x Girl On Fire", ""),
    ("212675193", "Brookhaven", "Music: Caillou Trap Remix", ""),
    ("1845554017", "Brookhaven", "Music: Uptown", ""),
    ("1305251774", "Brookhaven", "Music: Wii Music", ""),
    ("9119119619", "Brookhaven", "Music: Elevator Music", ""),
    ("165065112", "Brookhaven", "Music: Mako Beam (Proximity)", ""),
    ("9045389581", "Brookhaven", "Music: Midnight Carnival Alternate", ""),
    ("142376088", "Brookhaven", "Music: Parry Gripp - Raining Tacos", ""),
    ("1845793864", "Brookhaven", "Music: The Will to Fight A", ""),
    ("168208965", "Brookhaven", "Music: Whatcha Say - Jason Derulo", ""),
    ("5410086218", "Brookhaven", "Music: Crab Rave", ""),
    ("130778839", "Brookhaven", "Music: Everybody do the flop", ""),
    ("186317099", "Brookhaven", "Music: 2Pac - Life Goes On", ""),
    ("5925841720", "Brookhaven", "Music: 2Pac ft. Dr. Dre - California Love", ""),
    ("1259050178", "Brookhaven", "Music: A Roblox Rap", ""),
    ("225150067", "Brookhaven", "Music: Baby Bash - Suga Suga", ""),
    ("6957372976", "Brookhaven", "Music: Bad Bunny - Yonaguni", ""),
    ("1845016505", "Brookhaven", "Music: Believer", ""),
    ("1321038120", "Brookhaven", "Music: Billie Eilish - Ocean Eyes", ""),
    ("6843558868", "Brookhaven", "Music: BTS - Butter", ""),
    ("1894066752", "Brookhaven", "Music: BTS - Fake Love", ""),
    ("5760198930", "Brookhaven", "Music: Clairo - Sofia", ""),
    ("6657083880", "Brookhaven", "Music: Doja Cat - Kiss Me More", ""),
    ("521116871", "Brookhaven", "Music: Doja Cat - Say So", ""),
    ("6432181830", "Brookhaven", "Music: Glass Animals - Heat Wave", ""),
    ("249672730", "Brookhaven", "Music: Illijiah - On My Way", ""),
    ("1243143051", "Brookhaven", "Music: Jingle Oof", ""),
    ("4591688095", "Brookhaven", "Music: Justin Bieber - Yummy", ""),
    ("6403599974", "Brookhaven", "Music: Kali Uchis - Telepatia", ""),
    ("6177409271", "Brookhaven", "Music: Kim Dracula - Paparazzi", ""),
    ("6620108916", "Brookhaven", "Music: Lil Nas X - Call Me By Your Name", ""),
    ("3340674075", "Brookhaven", "Music: Lil Nas X - Panini", ""),
    ("143666548", "Brookhaven", "Music: Mii Channel Music", ""),
    ("6833920398", "Brookhaven", "Music: Olivia Rodrigo - Good 4 U", ""),
    ("614018503", "Brookhaven", "Music: Pink Fong - Baby Shark", ""),
    ("6447077697", "Brookhaven", "Music: PinkPantheress - Pain", ""),
    ("3400778682", "Brookhaven", "Music: Pokemon Sword and Shield Gym Theme", ""),
    ("6678031214", "Brookhaven", "Music: Polo G - RAPSTAR", ""),
    ("6887728970", "Brookhaven", "Music: Rauw Alejandro - Todo De Ti", ""),
    ("5595658625", "Brookhaven", "Music: Royal and the Serpent - Overwhelmed", ""),
    ("6760592191", "Brookhaven", "Music: Silk Sonic - Leave The Door Open", ""),
    ("2623209752", "Brookhaven", "Music: Ski Mask The Slump God - Nuketown", ""),
    ("292861322", "Brookhaven", "Music: Snoop Dogg - Drop It Like Its Hot", ""),
    ("6794553622", "Brookhaven", "Music: Syko - Brooklyn Blood Pop", ""),
    ("6159978466", "Brookhaven", "Music: Taylor Swift - You Belong With Me", ""),
    ("6463211475", "Brookhaven", "Music: Tesher - Jalebi Baby", ""),
    ("6815150969", "Brookhaven", "Music: The Kid LAROI ft. Justin Bieber - Stay", ""),
    ("4982789390", "Brookhaven", "Music: The Weeknd - Blinding Lights", ""),
    ("5619169255", "Brookhaven", "Music: The Weeknd - Save Your Tears", ""),
    ("224845627", "Brookhaven", "Music: The Kitty Cat Dance", ""),
    ("5145539495", "Brookhaven", "Music: Tina Turner - Whats Love Got to Do with It", ""),
    ("1725273277", "Brookhaven", "Music: Frank Ocean - Chanel", ""),
    ("189105508", "Brookhaven", "Music: Frozen - Let It Go", ""),
    ("5253604010", "Brookhaven", "Music: Capone - Oh No", ""),
    ("5937000690", "Brookhaven", "Music: Chikatto - Chika Chika", ""),
    ("154664102", "Brookhaven", "Music: You've Been Trolled", ""),

    # Royale High
    ("SmythsChandelier2024", "Royale High", "Exclusive reward", ""),

    # Doors
    ("SCREECHSUCKS", "Doors", "25 Knobs", ""),
    ("CRUSADERS", "Doors", "5 Stardust", ""),
    ("KUBZ SCOUTS", "Doors", "5 Knobs", ""),
    ("LORE", "Doors", "5 Knobs", ""),
    ("PENGUINZ0", "Doors", "5 Knobs", ""),
    ("CHEDDAR BALLS", "Doors", "1 Knob", ""),
    ("RAGDOLL COMBAT", "Doors", "1 Stardust", ""),
    ("PATHSWAP", "Doors", "1 Stardust", ""),
    ("JUMP OVER THE BRICK", "Doors", "1 Stardust", ""),
    ("VOCAB HAVOC", "Doors", "1 Stardust", ""),

    # Sol's RNG
    ("RaidCH2", "Sol's RNG", "3 Red Potion and 1 Red Moon Potion", ""),
    ("UPD20260228", "Sol's RNG", "20 Potion Chests and 5 Rare Potion Chests", ""),

    # Muscle Legends
    ("mightygems2500", "Muscle Legends", "2,500 Gems", ""),
    ("ultimate250", "Muscle Legends", "250 Strength", ""),
    ("spacegems50", "Muscle Legends", "5,000 Gems", ""),
    ("megalift50", "Muscle Legends", "250 Strength", ""),
    ("speedy50", "Muscle Legends", "250 Agility", ""),
    ("epicreward500", "Muscle Legends", "500 Gems", ""),
    ("MillionWarriors", "Muscle Legends", "1,500 Strength", ""),
    ("frostgems10", "Muscle Legends", "10,000 Gems", ""),
    ("Musclestorm50", "Muscle Legends", "1,500 Strength", ""),
    ("Skyagility50", "Muscle Legends", "500 Agility", ""),
    ("galaxycrystal50", "Muscle Legends", "5,000 Gems", ""),
    ("supermuscle100", "Muscle Legends", "200 Strength", ""),
    ("superpunch100", "Muscle Legends", "100 Strength", ""),
    ("launch250", "Muscle Legends", "250 Gems", ""),

    # Dragon Blox
    ("VALENTINE", "Dragon Blox", "5 Premium Wishes", ""),
    ("WHENUPDATE", "Dragon Blox", "10 Premium Wishes", ""),
    ("FEBRUARY", "Dragon Blox", "5 Premium Wishes", ""),
    ("SNEAKSSOON", "Dragon Blox", "5 Premium Wishes", ""),
    ("QOL", "Dragon Blox", "5 Premium Wishes", ""),
    ("QUICKUPDATE", "Dragon Blox", "10 Premium Wishes", ""),
    ("JANUARY", "Dragon Blox", "5 Premium Wishes", ""),
    ("FIRSTWISH", "Dragon Blox", "15 Premium Wishes", ""),
    ("DB2026", "Dragon Blox", "15 Premium Wishes", ""),
    ("HAPPYNEWYEAR", "Dragon Blox", "5 Premium Wishes", ""),
    ("HAPPYHOLIDAYS25", "Dragon Blox", "5 Premium Wishes", ""),
    ("XMAS2025", "Dragon Blox", "10 Premium Wishes", ""),

    # Ninja Legends
    ("soulhunter5", "Ninja Legends", "5 Souls", ""),
    ("chaosblade1000", "Ninja Legends", "1K Chi", ""),
    ("christmasninja500", "Ninja Legends", "500 Gems", ""),
    ("epictrain15", "Ninja Legends", "15 Minutes of Auto-Training", ""),
    ("roboninja15", "Ninja Legends", "15 Minutes of Auto-Training", ""),
    ("zenmaster15K", "Ninja Legends", "15K Chi", ""),
    ("soulninja1000", "Ninja Legends", "1K Chi", ""),
    ("darkelements2000", "Ninja Legends", "2K Chi", ""),
    ("omegasecrets5000", "Ninja Legends", "5K Chi", ""),
    ("ultrasecrets10k", "Ninja Legends", "10K Chi", ""),
    ("elementmaster750", "Ninja Legends", "750 Chi", ""),
    ("secretcrystal1000", "Ninja Legends", "750 Chi", ""),
    ("skymaster750", "Ninja Legends", "750 Chi", ""),
    ("legends700m", "Ninja Legends", "1.2K Chi", ""),
    ("dojomasters500", "Ninja Legends", "500 Chi", ""),
    ("dragonlegend750", "Ninja Legends", "750 Chi", ""),
    ("zenmaster500", "Ninja Legends", "500 Chi", ""),
    ("epicelements500", "Ninja Legends", "500 Chi", ""),
    ("goldupdate500", "Ninja Legends", "500 Chi", ""),
    ("legends500m", "Ninja Legends", "1000 Chi", ""),
    ("senseisanta500", "Ninja Legends", "500 Chi", ""),
    ("blizzardninja500", "Ninja Legends", "500 Chi", ""),
    ("mythicalninja500", "Ninja Legends", "500 Chi", ""),
    ("legendaryninja500", "Ninja Legends", "500 Chi", ""),
    ("shadowninja500", "Ninja Legends", "500 Chi", ""),
    ("legends200M", "Ninja Legends", "1.1K Chi", ""),
    ("epicflyingninja500", "Ninja Legends", "500 Chi", ""),
    ("flyingninja500", "Ninja Legends", "500 Chi", ""),
    ("dragonwarrior500", "Ninja Legends", "500 Chi", ""),
    ("swiftblade300", "Ninja Legends", "300 Chi", ""),
    ("DesertNinja250", "Ninja Legends", "250 Chi", ""),
    ("fastninja100", "Ninja Legends", "100 Chi", ""),
    ("epicninja250", "Ninja Legends", "250 Chi", ""),
    ("masterninja750", "Ninja Legends", "1K Chi", ""),

    # Volleyball Legends
    ("UPDATE_60", "Volleyball Legends", "5 Lucky Style Spins", ""),
    ("KIJO", "Volleyball Legends", "5 Lucky Style Spins", ""),
    ("SUPER_TILTS", "Volleyball Legends", "5 Lucky Ability Spins", ""),

    # === PREMIUM GAMES (password protected) ===

    # Genshin Impact
    ("ZECVVP1DT7Z2", "Genshin Impact", "10k Mora, 10 Adventurer's Experience, 5 Fine Enhancement Ore", ""),
    ("8BHA0KFRG94K", "Genshin Impact", "60 Primogems, 5 Adventurer's Experience", ""),
    ("8X73KH58KDHN", "Genshin Impact", "60 Primogems, 5 Adventurer's Experience", ""),
    ("GENSHINGIFT", "Genshin Impact", "50 Primogems, 3 Hero's Wit (works periodically)", ""),
    ("LTT3DVKVLUQZ", "Genshin Impact", "30 Primogems, 20k Mora, 3 Broken Drive Shafts", ""),

    # Honkai Star Rail
    ("7T3R83MMMTY3", "Honkai Star Rail", "Stellar Jade x100, Refined Aether x4", ""),
    ("CSJ882LL4BHF", "Honkai Star Rail", "Stellar Jade x100, Traveler's Guide x5", ""),
    ("DBJ9RJLMLSZB", "Honkai Star Rail", "Stellar Jade x100, Credit x50,000", ""),
    ("4T28RJM4MS3B", "Honkai Star Rail", "Stellar Jade x50, Credit x10,000", ""),
    ("SUB2SPARXIE", "Honkai Star Rail", "Traveler's Guide x3, Sparxie Plushie x2", ""),
    ("ALETTERFORYOU", "Honkai Star Rail", "Adventure Log x6, Dreamlight Mixed Sweets x2", ""),
    ("HailYaoGuang", "Honkai Star Rail", "Traveler's Guide x3, Songlotus Cake x2", ""),
    ("KBJ8VZ6Y27QX", "Honkai Star Rail", "Stellar Jade x60, Traveler's Guide x2, Refined Aether x3, Credit x5,000", ""),
    ("MH5KC", "Honkai Star Rail", "Stellar Jade x100, Refined Aether x4", ""),
    ("BGF3A", "Honkai Star Rail", "Stellar Jade x100, Traveler's Guide x5", ""),
    ("AT45Q", "Honkai Star Rail", "Stellar Jade x100, Credit x50,000", ""),
    ("OMEGA", "Honkai Star Rail", "Stellar Jade x60, Fuel x1", ""),
    ("CREATIONNYMPH", "Honkai Star Rail", "Stellar Jade x60, Fuel x1, Heroic Variable x1", ""),
    ("FAREWELL", "Honkai Star Rail", "Stellar Jade x60, Fuel x1", ""),
    ("IFYOUAREREADINGTHIS", "Honkai Star Rail", "Stellar Jade x60, Fuel x1", ""),
    ("STARRAILGIFT", "Honkai Star Rail", "Stellar Jade x100, Traveler's Guide x4, Bottled Soda x5, Credit x50,000", ""),

    # Pokemon GO
    ("FENDIxFRGMTxPOKEMON", "Pokemon GO", "FENDI x FRGMT x Pokemon Hoodie", ""),
    ("TH4NKY0UF41RYMUCH", "Pokemon GO", "Very Fairy Timed Research Quest", ""),
    ("QFWM3SRJPVRY5", "Pokemon GO", "Unown X Bonus Timed Research Quest", ""),
    ("6K343X373BDQM", "Pokemon GO", "Unown Y Bonus Timed Research Quest", ""),
    ("2PKXPAT2RJXKL", "Pokemon GO", "Unown Z and A Bonus Timed Research Quest", ""),

    # AFK Arena
    ("2bxn4k86qd", "AFK Arena", "3x 8h Dust, 3x 8h Gold, 3x 8h EXP, 1000 Diamonds", ""),
    ("2bfe265g6x", "AFK Arena", "3x 8h Dust, 3x 8h Gold, 3x 8h EXP, 1000 Diamonds", ""),
    ("2b9pyu99rn", "AFK Arena", "10x Stargazer Scrolls, 60 Honourable Soulstones, 10x Faction Scrolls", ""),
    ("2bjzpbed53", "AFK Arena", "2000 Diamonds, 10x Stargazer Scrolls, 10x Common Scrolls, 10x Faction Scrolls", ""),
    ("belovedhero2025", "AFK Arena", "1000 Diamonds, 10x Common Scrolls", ""),
    ("vdj82fht4r", "AFK Arena", "3000 Diamonds, 10x Time Emblems, 10x Stargazer Scrolls, 10x Common Scrolls", ""),
    ("lilithhappy2026", "AFK Arena", "5x Common Scrolls, 5x Stargazer Scrolls", ""),
    ("DON2026classic", "AFK Arena", "10x Common Scrolls, 15x Draconis Insignias, 10x Stargazer Scrolls, 10x Wish Leafs", ""),
    ("ujqrukd2at", "AFK Arena", "1x 8h Dust, 1x 8h Gold, 1x 8h EXP, 1200 Diamonds", ""),
    ("uj5fs5z58s", "AFK Arena", "10x Faction Scrolls, 10x Stargazer Scrolls, 60 Elite Soulstones", ""),
    ("u4fctemje2", "AFK Arena", "3x 8h Dust, 3x 8h Gold, 3x 8h EXP, 1000 Diamonds", ""),
    ("DTZDMHXU83", "AFK Arena", "Free sticker", ""),
    ("mystery2023", "AFK Arena", "Free sticker", ""),
    ("special2023", "AFK Arena", "Free sticker", ""),
    ("misevj66yi", "AFK Arena", "500 Diamonds, 5 Summon Scrolls, 1 Rare Hero", ""),
    # Mech Arena (PREMIUM)
    ("MIDGAME", "Mech Arena", "Starter reward", ""),
    ("SPOOKYSEASON", "Mech Arena", "Halloween reward", ""),
    ("HAPPYBDAYMA", "Mech Arena", "Anniversary reward", ""),
    ("SUMMERPILOTS", "Mech Arena", "Summer reward", ""),
    ("NEWYEAR2026", "Mech Arena", "New Year reward", ""),
    ("CHILLBOT", "Mech Arena", "Reward", ""),
    ("MIDGAMEYOUTUBECHANNEL", "Mech Arena", "YouTube reward", ""),
    ("DISCORD100k", "Mech Arena", "Discord milestone reward", ""),
    ("WARTEX", "Mech Arena", "200 A-Coins, 100k Credits, Prodigy Crate, Vortex Mech (New Players)", ""),
    ("FOR42OLDS", "Mech Arena", "242 A-Coins, 42,000 Credits, 420 Implant Parts", ""),
    ("ILOVEMIDGAME", "Mech Arena", "2x Rank 4 Nade Launcher 6, 100 A-Coins (Best value: 870 A-Coins)", ""),
    ("MIDTENGUGIFT", "Mech Arena", "Rank 3 Tengu, 100 A-Coins", ""),
    ("GGTBONUS", "Mech Arena", "2x Rank 3 Javelin Rack 8", ""),
    ("BLASTZONE", "Mech Arena", "Rank 3 Guardian Mech, 200 A-Coins, 50k Credits, Prodigy Crate", ""),
    ("MIDGAMEMELEE", "Mech Arena", "2x Rank 4 Arc Torrent 6, 250 A-Coins, Amateur Crate", ""),
    # Rivals
    ("COMMUNITY22", "Rivals", "1 Community Wrap", ""),
    ("FREE160", "Rivals", "3 Keys", ""),
    ("COMMUNITY21", "Rivals", "1 Community Wrap", ""),
    ("BONUS", "Rivals", "1 Key", ""),
    ("BOOST", "Rivals", "1 Key", ""),
    ("roblox_rtc", "Rivals", "5 Keys", ""),

    # Evade
    ("900", "Evade", "10 Points", ""),
    ("901", "Evade", "12 Points", ""),
    ("hdc_roblox", "Evade", "30 Points", ""),
    ("halloween_23", "Evade", "23 Points", ""),
    ("indebt", "Evade", "30 Points", ""),
    ("indebt2", "Evade", "1000 Tokens", ""),
    ("THANKSGIVING2025", "Evade", "15 Points", ""),
    ("iloveevadewinterupdate", "Evade", "20 Points", ""),
    ("HappyNewYears2026", "Evade", "26 Points", ""),

    # Hypershot
    ("100K", "Hypershot", "Free Present", ""),
    # Arm Wrestle Simulator
    ("SlightWaitLol", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("thenewlab", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("chaoticbosses", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("atomicishere", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("dungeonsopen", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("planetzorp", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("massiveqol", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("merrychristmas", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("qolupdate", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("wildwest", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("abandonedthemepark", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("mansionunderworld", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("mansionbasement", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("hauntedmansion", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("hollowsorry", "Arm Wrestle Simulator", "2x event strength boost for 2 hours", ""),
    ("spookyseason", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("citymines", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("playfulmines", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("desertmines", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("welovemining", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("sorryfordelay", "Arm Wrestle Simulator", "1B Mining Bicep Strength", ""),
    ("egyptian", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("pyramids", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("21iscoming", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("brainrot", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("removal", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("octogames", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("glassbridge", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("celebration", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("banker", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("sorryoops", "Arm Wrestle Simulator", "3x strength boost for 24 hours", ""),
    ("timetravel", "Arm Wrestle Simulator", "48 hours of 3x strength and +5% boost on all stats", ""),
    ("world19", "Arm Wrestle Simulator", "5% on all strengths and 3x stat boost for 48 hours", ""),
    ("bulk", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("superhero", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("tokenstore", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("captain", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("skullbeard", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("pirate", "Arm Wrestle Simulator", "5% on all strengths and 1,000 Gold Coins", ""),
    ("athlete", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("tradingback", "Arm Wrestle Simulator", "5% boost on all strengths", ""),
    ("blossom", "Arm Wrestle Simulator", "3x stat boost for 48 hours and 1500 Prison Coins", ""),
    ("ninja", "Arm Wrestle Simulator", "3x stat boost for 48 hours and 1500 Prison Coins", ""),
    ("snowops", "Arm Wrestle Simulator", "3x stat boost for 48 hours", ""),
    ("hideout", "Arm Wrestle Simulator", "3x stat boost for 48 hours and 2500 Prison Coins", ""),
    ("cosmic", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("stocking", "Arm Wrestle Simulator", "3x stat boost for 72 hours and Christmas Title", ""),
    ("frostlands", "Arm Wrestle Simulator", "3x stat boost for 24 hours and 150 Ice Cubes", ""),
    ("polar", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("shiny", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("Christmas", "Arm Wrestle Simulator", "3x stat boost for 72 hours", ""),
    ("hacker", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("classic", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("clans", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("rifted", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("hauntedmanor", "Arm Wrestle Simulator", "3x stat boost for 24 hours and Free candy", ""),
    ("trainers", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("ghosthunting", "Arm Wrestle Simulator", "3x stat boost for 24 hours and 1 Halloween card", ""),
    ("spooky", "Arm Wrestle Simulator", "3x stat boost for 24 hours and 3,500 candy", ""),
    ("soon", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("hatching", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("billion", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("Heavenly", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("rework", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("paradise", "Arm Wrestle Simulator", "3x stat boost for 24 hours and 1 gold", ""),
    ("wasteland", "Arm Wrestle Simulator", "3x stat boost for 24 hours", ""),
    ("apocalypse", "Arm Wrestle Simulator", "3x boost for 24 hours", ""),
    ("energy", "Arm Wrestle Simulator", "3x boost for 24 hours", ""),
    ("royalty", "Arm Wrestle Simulator", "3x boost for 24 hours", ""),
    ("performance", "Arm Wrestle Simulator", "3x boost for 24 hours", ""),
    ("charms", "Arm Wrestle Simulator", "3x boost for 24 hours", ""),
    ("wizard", "Arm Wrestle Simulator", "3x boost for 24 hours and 25 Miner Crystal", ""),
    ("atlantis", "Arm Wrestle Simulator", "3x boost for 8 hours", ""),
    ("800mvisits", "Arm Wrestle Simulator", "3x stat boost for 8 hours", ""),
    ("icecold", "Arm Wrestle Simulator", "3x boost for 24 hours", ""),
    ("forging", "Arm Wrestle Simulator", "3x boost for 24 hours", ""),
    ("axel", "Arm Wrestle Simulator", "50 Wins", ""),
    # Waste Time
    ("Chapter3", "Waste Time", "Free Rewards", ""),
    ("yesanothercode", "Waste Time", "Free Rewards", ""),
    ("quick", "Waste Time", "12 Locks", ""),
    ("StPatricks", "Waste Time", "Free Rewards", ""),
    ("Central", "Waste Time", "Free Rewards", ""),
    ("Valentines2", "Waste Time", "Free Rewards", ""),
    ("QuestsHere", "Waste Time", "Free Rewards", ""),
    ("imsorrylowk", "Waste Time", "Free Rewards", ""),
    ("Valentines", "Waste Time", "Free Rewards", ""),
    ("sorry3", "Waste Time", "Free Rewards", ""),
    ("adminpanel", "Waste Time", "Free Rewards", ""),
    ("wowowoowowowowowoowowowo", "Waste Time", "Free Rewards", ""),
    ("Compensation", "Waste Time", "Free Rewards", ""),
    ("cards", "Waste Time", "Free Rewards", ""),
    ("sorryfornotfixingclansyet", "Waste Time", "Free Rewards", ""),
    ("gullible", "Waste Time", "Free Rewards", ""),
    ("sorryforbrokenclans", "Waste Time", "Free Rewards", ""),
    ("10millionvisitswow", "Waste Time", "+10 Enchantments locks", ""),
    ("20kccu", "Waste Time", "+2 Enchantments locks", ""),
    ("holymoly", "Waste Time", "x1.25 highest reset stat", ""),
    ("superduperhidden", "Waste Time", "+2 Enchantments rerolls", ""),
    ("freererollsfr", "Waste Time", "+10 Enchantments rerolls", ""),
    ("freelocksfr", "Waste Time", "+5 Enchantments locks", ""),
    ("sorryforP2W", "Waste Time", "+50 Enchantments rerolls", ""),
    ("yetanothercompensation", "Waste Time", "+20 Enchantments rerolls", ""),
    ("imsosorry", "Waste Time", "+50k Button Clicks", ""),
    ("freeclicks", "Waste Time", "+2k Button Clicks", ""),
    ("wehavecodesnow", "Waste Time", "x2 Highest Reset Stat", ""),
    ("moreclicksfr", "Waste Time", "+500 Other Button Clicks", ""),

    # Tap Simulator
    ("VALENTINES", "Tap Simulator", "1 Love Luck III Potion", ""),
    ("SPEEDYTOTEM", "Tap Simulator", "2 Totems of Hatch Speed", ""),
    ("LUCKYTOTEM", "Tap Simulator", "1 Totem of Luck", ""),
    ("TELEPORT", "Tap Simulator", "2 Teleport Crystals", ""),
    ("lucky", "Tap Simulator", "Luck Potion III", ""),
    ("tacos", "Tap Simulator", "Taco Potion", ""),
    ("russo", "Tap Simulator", "Five Tokens", ""),
    ("enchant", "Tap Simulator", "Five Enchant Crystals", ""),

    # Yeet a Friend
    ("YEETOLYMPICS", "Yeet a Friend", "10K Stars", ""),
    ("YAFTOBER", "Yeet a Friend", "Free Boosts", ""),
    ("GRAFFITI", "Yeet a Friend", "Power Boost", ""),
    ("GOTHICSCHOOL", "Yeet a Friend", "Energy, Luck, Power, Magnet and Rock Fuel Boosts", ""),
    ("Camp", "Yeet a Friend", "2 Magnet10 Boost", ""),
    ("Octopus", "Yeet a Friend", "Energy, Luck, Power, Magnet and Rock Fuel Boosts", ""),
    ("BOMBARDINO", "Yeet a Friend", "Mythic Slime Pet", ""),
    ("GYMSTAR", "Yeet a Friend", "7.77k Stars", ""),
    ("SUPERCAR", "Yeet a Friend", "3 Wheel Spins", ""),
    ("VALENTINE", "Yeet a Friend", "3 Energy Boosts, 3 Luck Boosts, 3 Power Boosts", ""),
    ("OLYMP", "Yeet a Friend", "Mythic Slime Pet", ""),
    ("IPLAYEVERYDAY", "Yeet a Friend", "Legendary Slime Pet", ""),
    ("Junk", "Yeet a Friend", "Power Boost", ""),
    ("Halloween", "Yeet a Friend", "50K Stars", ""),
    ("XMAS24", "Yeet a Friend", "30K Stars", ""),
    ("CHRISTMAS", "Yeet a Friend", "10k Stars", ""),
    ("GIFTING", "Yeet a Friend", "5 Wheel Spins", ""),
    ("Reap", "Yeet a Friend", "10k Stars", ""),
    ("Aztec", "Yeet a Friend", "3 Wheel Spins", ""),
    ("MAGIC", "Yeet a Friend", "x3 Energy Boost", ""),
    ("AFK", "Yeet a Friend", "x2 Luck Boost", ""),
    ("Glacier", "Yeet a Friend", "10k Stars", ""),
    ("Enchanted", "Yeet a Friend", "5k Stars", ""),
    ("Teleporter", "Yeet a Friend", "5k Stars", ""),
    ("EASYEET", "Yeet a Friend", "Power Boost", ""),
    ("DimensionBoost", "Yeet a Friend", "Energy Boost", ""),
    ("Dimension", "Yeet a Friend", "Power Boost", ""),
    ("Collector", "Yeet a Friend", "10k Stars", ""),
    ("StarShopper", "Yeet a Friend", "5k Stars", ""),
    ("YeetCartoon", "Yeet a Friend", "Power Boost", ""),
    ("FreeStars", "Yeet a Friend", "750 Stars", ""),
    ("FreePower", "Yeet a Friend", "Power Boost", ""),
    ("iLoveYeeting", "Yeet a Friend", "Legendary Slime Pet", ""),

    # Youtube Simulator Z
    ("RUBY_Z", "Youtube Simulator Z", "Access to a room that rains Rubies", ""),
    ("MONEYRAIN", "Youtube Simulator Z", "Access to a room that rains normal Money", ""),
    ("TileZ", "Youtube Simulator Z", "Access to a room that rains Tiles", ""),
    ("ICEmoneyRAIN", "Youtube Simulator Z", "Access to a room that rains Ice Money", ""),
    ("Coinflip", "Youtube Simulator Z", "Flip for Normal Tokens (Requires 1 Rebirth)", ""),
    ("CoinflipICE", "Youtube Simulator Z", "Flip for Ice Tokens (Requires Ice Room access)", ""),
    ("Verified", "Youtube Simulator Z", "Verified badge next to your name", ""),
    ("Challenges", "Youtube Simulator Z", "Reward bonuses", ""),
    ("YTZ", "Youtube Simulator Z", "General reward", ""),

    # Anime Vanguards
    ("Chainsaws", "Anime Vanguards", "5000 Gems, 20 Rerolls, 20 Memoria Shards", ""),
    ("1WeekDelay", "Anime Vanguards", "50 Rerolls, 50 Memoria Shards", ""),
    ("NoCustoms", "Anime Vanguards", "10000 Gems, 30 Rerolls, 30 Memoria Shards", ""),
    ("SorryForBugs", "Anime Vanguards", "Free Rewards", ""),
    ("ALMOST100K", "Anime Vanguards", "100 Trait Rerolls, 100 Memoria Shards", ""),
    ("Winter26", "Anime Vanguards", "Free Rewards", ""),
    ("Memoria", "Anime Vanguards", "Free Rewards", ""),
    ("ItsCold", "Anime Vanguards", "Free Rewards", ""),
    ("FreedomsCallPart2", "Anime Vanguards", "5000 Gems, 50 Stat Chips", ""),
    ("PinkVillainRaid", "Anime Vanguards", "50 Rerolls", ""),
    ("FallEndsSoon", "Anime Vanguards", "50 Rerolls, 25000 Leaves", ""),
    ("2026", "Anime Vanguards", "200 Rerolls (level 30 required)", ""),

    # 99 Nights in the Forest
    ("afterparty", "99 Nights in the Forest", "15 Gems", ""),
    ("yay fishing", "99 Nights in the Forest", "2 Gems (type in chat while fishing)", ""),
    ("DIAMONDS", "99 Nights in the Forest", "15 Gems", ""),

    # Destroy Grandma
    ("BETA", "Destroy Grandma", "15,000 Cash", ""),
    ("YGDS!", "Destroy Grandma", "15,000 Cash", ""),
    ("DESTROY", "Destroy Grandma", "2x XP and Mastery Boost for 15 minutes", ""),

    # Bed Wars
    ("Femboy-yuzi", "Bed Wars", "Kit", ""),
    # Driving Empire
    ("10KITS", "Driving Empire", "10 Tuning Kits", ""),
    ("MARCH2026", "Driving Empire", "Chevrolet Camaro ZL1", ""),
    ("HAPPY2026", "Driving Empire", "New Year gift", ""),
    ("HAPPYXMAS", "Driving Empire", "Festive themed bike", ""),
    ("CALL911", "Driving Empire", "50,911 Cash", ""),
    ("GOBBLEGOBBLE", "Driving Empire", "10 Tuning Kits", ""),
    ("SPOOKY", "Driving Empire", "80,000 Cash", ""),
    ("VEGAS2025", "Driving Empire", "50,000 Cash", ""),
    ("WHOOPS", "Driving Empire", "75,000 Cash", ""),
    ("RDCNASCAR25", "Driving Empire", "Driving Empire NASCAR", ""),
    ("2MLIKES", "Driving Empire", "2017 Nissan GT-R Bolt", ""),
    ("NASCAR100M", "Driving Empire", "200 Trophies", ""),
    ("CUSTOMIZATION2025", "Driving Empire", "10 Tuning Kits", ""),
    ("1MILCASH", "Driving Empire", "1 Cash", ""),
    ("200KMEMBERS", "Driving Empire", "50,000 Cash", ""),
    ("NEWYEAR2025", "Driving Empire", "75,000 Cash", ""),
    ("ZOOM", "Driving Empire", "2023 Fairway Zoomer", ""),
    # Anime Infinity
    ("9KFavs!", "Anime Infinity", "15x Trait Shards, 3x Rainbow Orbs, 1.5k Gems", ""),
    ("MBShutdown!", "Anime Infinity", "15x Trait Shards, 3x Rainbow Orbs, 1.5k Gems", ""),
    ("Update3!", "Anime Infinity", "15x Trait Shards, 3x Rainbow Orbs, 1.5k Gems", ""),
    ("NewGamemode!", "Anime Infinity", "15x Trait Shards, 3x Rainbow Orbs, 1.5k Gems", ""),
    ("Fusion!", "Anime Infinity", "15x Trait Shards, 3x Rainbow Orbs, 1.5k Gems", ""),
    ("YOSHAA!", "Anime Infinity", "15x Trait Shards, 3x Rainbow Orbs, 1.5k Gems", ""),
    ("DelayInfinity!", "Anime Infinity", "15x Trait Shards, 3x Rainbow Orbs, 1.5k Gems", ""),

    # Basketball Legends
    ("500KFAVS", "Basketball Legends", "Free Rewards", ""),
    ("TURKEY25", "Basketball Legends", "1x Halloween Skin Case (FL) or 1x Halloween Effect Case (BL)", ""),
    ("CLANS", "Basketball Legends", "1x Halloween Case", ""),
    ("DELAYED", "Basketball Legends", "1x Halloween Skin Case", ""),
    ("SUPERSPOOKY", "Basketball Legends", "1x Halloween Case", ""),
    ("SUPERSCARY", "Basketball Legends", "1x Halloween Skin Case", ""),
    ("JAMALCHOCOLATEPUDDING", "Basketball Legends", "1x Effect Crate", ""),
    ("JAMALBANANAPUDDING", "Basketball Legends", "1x Skin Crate", ""),
    ("banana", "Basketball Legends", "1x Elite Crate", ""),
    ("MAGICAL", "Basketball Legends", "1x Elite Crate", ""),
    ("SUMMER25", "Basketball Legends", "1x Summer25 Effect Crate", ""),
    ("DELAYCASE", "Basketball Legends", "1x Summer25 Effect Crate", ""),
    ("DELAYSKIN", "Basketball Legends", "1x Summer25 Skin Crate", ""),
    ("ANIMEBOSSRAID", "Basketball Legends", "10K Coins", ""),
    ("325KLIKES", "Basketball Legends", "5K Coins", ""),
    ("320KLIKES", "Basketball Legends", "5K Coins", ""),
    ("310KLIKES", "Basketball Legends", "5K Coins", ""),
    ("COINBOOST", "Basketball Legends", "2x Coin Boost for 30 minutes", ""),
    # Deathball
    ("KSTELLAR", "Deathball", "25,000 Gems", ""),
    ("SUPERNOVANOW", "Deathball", "25,000 Gems", ""),
    ("SUPERNOVASOON", "Deathball", "25,000 Gems", ""),
    ("DRAGONQUEST", "Deathball", "25,000 Gems", ""),
    ("XMASUPD3", "Deathball", "25,000 Gems", ""),
    ("SANTASOON", "Deathball", "25,000 Gems", ""),
    ("XMASUPD2", "Deathball", "500 Crystals", ""),
    ("CHRISTMAS", "Deathball", "25,000 Gems", ""),
    ("XMASUPD1", "Deathball", "500 Crystals", ""),
    ("25KCCUTHNX", "Deathball", "25,000 Gems", ""),
    ("GREENMAN", "Deathball", "500 Crystals", ""),
    ("WINGS", "Deathball", "25,000 Gems", ""),
    ("BANNERSOON", "Deathball", "25,000 Gems", ""),
    ("DOCSTONE", "Deathball", "25,000 Gems", ""),
    ("CHAMPSOON", "Deathball", "25,000 Gems", ""),
    ("DBTIME", "Deathball", "15,000 Gems", ""),
    ("FREEGEMS", "Deathball", "500 Crystals", ""),
    ("GHOSTMODE", "Deathball", "500 Crystals", ""),
    ("DRPLAGUE", "Deathball", "500 Crystals", ""),
]


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                game TEXT NOT NULL,
                desc TEXT,
                exp TEXT,
                used INTEGER DEFAULT 0,
                added_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()
        count = db.execute("SELECT COUNT(*) FROM codes").fetchone()[0]
        if count == 0:
            for code, game, desc, exp in PRELOADED_CODES:
                db.execute(
                    "INSERT INTO codes (code, game, desc, exp) VALUES (?, ?, ?, ?)",
                    (code, game, desc, exp)
                )
            db.commit()


def expiry_info(exp_str):
    if not exp_str:
        return None, None
    try:
        exp = datetime.strptime(exp_str, "%Y-%m-%d").date()
        diff = (exp - date.today()).days
        if diff < 0:
            return "Expired", "expired"
        elif diff <= 7:
            return f"{diff}d left", "soon"
        else:
            return exp.strftime("%d %b"), "ok"
    except Exception:
        return None, None


def is_premium_unlocked():
    return session.get("premium") == True


@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    error = None
    if request.method == "POST":
        pw = request.form.get("password", "").strip()
        if pw in PREMIUM_PASSWORDS:
            session["premium"] = True
            return redirect(url_for("index"))
        else:
            error = "Wrong password! Contact Parth to get access."
    return render_template("unlock.html", error=error)


@app.route("/lock")
def lock():
    session.pop("premium", None)
    return redirect(url_for("index"))


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    filter_game = request.args.get("game", "")
    filter_status = request.args.get("status", "")
    premium = is_premium_unlocked()

    db = get_db()
    query = "SELECT * FROM codes WHERE 1=1"
    params = []

    # Hide premium games if not unlocked
    if not premium:
        placeholders = ",".join("?" for _ in PREMIUM_GAMES)
        query += f" AND game NOT IN ({placeholders})"
        params += PREMIUM_GAMES

    if search:
        query += " AND (UPPER(code) LIKE UPPER(?) OR LOWER(game) LIKE LOWER(?) OR LOWER(desc) LIKE LOWER(?))"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if filter_game:
        query += " AND game = ?"
        params.append(filter_game)
    if filter_status == "unused":
        query += " AND used = 0"
    elif filter_status == "used":
        query += " AND used = 1"

    query += " ORDER BY added_at DESC"
    codes = db.execute(query, params).fetchall()
    codes = [dict(c) for c in codes]

    for c in codes:
        lbl, cls = expiry_info(c["exp"])
        c["exp_label"] = lbl
        c["exp_cls"] = cls

    all_games_query = "SELECT DISTINCT game FROM codes"
    if not premium:
        placeholders = ",".join("?" for _ in PREMIUM_GAMES)
        all_games_query += f" WHERE game NOT IN ({placeholders})"
        all_games = [r["game"] for r in db.execute(all_games_query, PREMIUM_GAMES).fetchall()]
    else:
        all_games = [r["game"] for r in db.execute(all_games_query).fetchall()]

    total = len(codes)
    unused = sum(1 for c in codes if not c["used"])

    soon_count = 0
    for row in db.execute("SELECT exp FROM codes WHERE exp != '' AND exp IS NOT NULL").fetchall():
        _, cls = expiry_info(row["exp"])
        if cls == "soon":
            soon_count += 1

    return render_template("index.html",
        codes=codes, games=ROBLOX_GAMES, all_games=all_games,
        search=search, filter_game=filter_game, filter_status=filter_status,
        total=total, unused=unused, soon=soon_count,
        premium=premium, premium_games=PREMIUM_GAMES)


@app.route("/add", methods=["POST"])
def add_code():
    code = request.form.get("code", "").strip().upper()
    game = request.form.get("game", "").strip()
    desc = request.form.get("desc", "").strip()
    exp = request.form.get("exp", "").strip()

    if not code or not game:
        return redirect(url_for("index"))

    if exp:
        try:
            datetime.strptime(exp, "%Y-%m-%d")
        except ValueError:
            exp = ""

    with get_db() as db:
        db.execute("INSERT INTO codes (code, game, desc, exp) VALUES (?, ?, ?, ?)",
                   (code, game, desc, exp))
        db.commit()

    return redirect(url_for("index"))


@app.route("/toggle/<int:code_id>", methods=["POST"])
def toggle_used(code_id):
    with get_db() as db:
        current = db.execute("SELECT used FROM codes WHERE id=?", (code_id,)).fetchone()
        if current:
            db.execute("UPDATE codes SET used=? WHERE id=?",
                       (0 if current["used"] else 1, code_id))
            db.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<int:code_id>", methods=["POST"])
def delete_code(code_id):
    with get_db() as db:
        db.execute("DELETE FROM codes WHERE id=?", (code_id,))
        db.commit()
    return redirect(request.referrer or url_for("index"))


init_db()

if __name__ == "__main__":
    print("\n🎮 Roblox Code Vault is running!")
    print("Open this in your browser: http://localhost:5000")
    print("Press CTRL+C to stop.\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
