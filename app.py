from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime, date

app = Flask(__name__)
DB = os.path.join(os.environ.get("TMPDIR", "/tmp"), "codes.db")

GAMES = [
    "Blox Fruits", "Anime Card Clash", "Bubble Gum Simulator",
    "Basketball Zero", "Blue Lock: Rivals", "Pet Simulator X",
    "Pet Simulator 99", "Shindo Life", "Anime Defenders",
    "Grand Piece Online", "King Legacy", "Fisch",
    "Fruit Battlegrounds", "AUT (A Universal Time)", "Peroxide",
    "Jailbreak", "Adopt Me!", "Murder Mystery 2", "Tower of Hell",
    "Brookhaven", "Royale High", "Doors", "Anime Adventures",
    "Sol's RNG", "Arcane Odyssey", "Muscle Legends", "Dragon Blox",
    "Ninja Legends", "Work at a Pizza Place", "Volleyball Legends", "Other"
]

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
    ("IMINYOURWALLS", "Basketball Zero", "50 Lucky Spins", ""),
    ("LOOKBEHINDYOU", "Basketball Zero", "500,000 Money", ""),
    ("DOMAINCLASH", "Basketball Zero", "20 Lucky Spins, 50,000 Money", ""),
    ("CURSEKING", "Basketball Zero", "20 Lucky Spins, 50,000 Money", ""),
    ("30CURSEKING", "Basketball Zero", "25 Lucky Spins, 100,000 Money", ""),
    ("1HRCURSEKING", "Basketball Zero", "30 Lucky Spins, 150,000 Money", ""),

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
    ("SKGames", "King Legacy", "2x EXP for 30 minutes (join Sea King Games group)", ""),
    ("RainbowDragon", "King Legacy", "100 Gems", ""),
    ("DragonColorRefund", "King Legacy", "50 Gems (or 10 if original red color)", ""),
    ("WELCOMETOKINGLEGACY", "King Legacy", "2x EXP for 30 minutes", ""),
    ("<3LEEPUNGG", "King Legacy", "2x EXP for 30 minutes", ""),
    ("FREESTATSRESET", "King Legacy", "Free Stat Refund", ""),
    ("2MFAV", "King Legacy", "Free Stat Refund", ""),
    ("Peodiz", "King Legacy", "100k Cash", ""),
    ("DinoxLive", "King Legacy", "100k Cash", ""),

    # Fisch
    ("SeventhOfMarch!", "Fisch", "Frigid Beauty Rod Skin", ""),
    ("JungleExpansion", "Fisch", "500 Coins, 5x Thorn Cluster, Random Item", ""),
    ("JungleExpansionSOON", "Fisch", "1111 Coins, Forestwing Rod Skin, 5x Thorn Cluster, Colossal Dragon Hunt Totem", ""),
    ("JOUNCE", "Fisch", "Chroma Blade of Glorp Skin", ""),
    ("BIGGLE", "Fisch", "1x Garbage", ""),
    ("Brinestorm", "Fisch", "Flamemourner Rod skin for Tidemourner Rod", ""),
    ("Tidefall", "Fisch", "Tiny Fabulous Rod skin and Random Hunt Totem", ""),
    ("Astraeus", "Fisch", "Shadow Pole Rod skin for the North Pole rod", ""),
    ("scarlet", "Fisch", "Scarlet skin for Nate's Blade", ""),
    ("TemporarySubmarine", "Fisch", "Submarine parts", ""),
    ("CARBON", "Fisch", "Free Carbon bobber", ""),

    # Fruit Battlegrounds
    ("ITSTHEBILLION!", "Fruit Battlegrounds", "600 Gems", ""),
    ("CODEFIX", "Fruit Battlegrounds", "Title", ""),

    # AUT (A Universal Time)
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

    # Brookhaven music codes
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
            print(f"Loaded {len(PRELOADED_CODES)} codes!")


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


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    filter_game = request.args.get("game", "")
    filter_status = request.args.get("status", "")

    db = get_db()
    query = "SELECT * FROM codes WHERE 1=1"
    params = []

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

    all_games = [r["game"] for r in db.execute("SELECT DISTINCT game FROM codes ORDER BY game").fetchall()]

    total = db.execute("SELECT COUNT(*) FROM codes").fetchone()[0]
    unused = db.execute("SELECT COUNT(*) FROM codes WHERE used=0").fetchone()[0]

    soon_count = 0
    for row in db.execute("SELECT exp FROM codes WHERE exp != '' AND exp IS NOT NULL").fetchall():
        _, cls = expiry_info(row["exp"])
        if cls == "soon":
            soon_count += 1

    return render_template("index.html",
        codes=codes, games=GAMES, all_games=all_games,
        search=search, filter_game=filter_game, filter_status=filter_status,
        total=total, unused=unused, soon=soon_count)


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


if __name__ == "__main__":
    init_db()
    print("\n🎮 Roblox Code Vault is running!")
    print("Open this in your browser: http://localhost:5000")
    print("Others on your network can visit: http://<your-ip>:5000")
    print("Press CTRL+C to stop.\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
