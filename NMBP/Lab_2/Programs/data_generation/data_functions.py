#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

def GetRandomYear():
  return random.randint(2000, 2010)

def GetRandomMonth():
  return random.randint(1,12)

def GetRandomDay():
  return random.randint(1,28)



titles = ["Absalom, Absalom!",
"A che punto è la notte",
"After Many a Summer Dies the Swan",
"Ah, Wilderness!",
"Alien Corn",
"The Alien Corn",
"All Passion Spent",
"All the King's Men",
"Alone on a Wide, Wide Sea",
"An Acceptable Time",
"Antic Hay",
"An Evil Cradling",
"Arms and the Man",
"As I Lay Dying",
"A Time to Kill",
"Behold the Man",
"Beneath the Bleeding",
"Beyond the Mexique Bay",
"Blithe Spirit",
"Blood's a Rover",
"Blue Remembered Earth",
"Blue Remembered Hills",
"Bonjour Tristesse",
"Brandy of the Damned",
"Bury My Heart at Wounded Knee",
"Butter In a Lordly Dish",
"By Grand Central Station I Sat Down and Wept",
"Cabbages and Kings",
"Carrion Comfort",
"A Catskill Eagle",
"The Children of Men",
"Clouds of Witness",
"A Confederacy of Dunces",
"Consider Phlebas",
"Consider the Lilies",
"Cover Her Face",
"The Cricket on the Hearth",
"The Curious Incident of the Dog in the Night-Time",
"The Daffodil Sky",
"Dance Dance Dance",
"A Darkling Plain",
"Death Be Not Proud",
"The Doors of Perception",
"Down to a Sunless Sea",
"Dulce et Decorum Est",
"Dying of the Light",
"East of Eden",
"Ego Dominus Tuus",
"Endless Night",
"Everything is Illuminated",
"Eyeless in Gaza",
"Fair Stood the Wind for France",
"Fame Is the Spur",
"A Fanatic Heart",
"The Far-Distant Oxus",
"A Farewell to Arms",
"Far From the Madding Crowd",
"Fear and Trembling",
"For a Breath I Tarry",
"For Whom the Bell Tolls",
"Frequent Hearses",
"From Here to Eternity",
"A Glass of Blessings",
"The Glory and the Dream",
"The Golden Apples of the Sun",
"The Golden Bowl",
"Gone with the Wind",
"The Grapes of Wrath",
"Great Work of Time",
"The Green Bay Tree",
"A Handful of Dust",
"Have His Carcase",
"The Heart Is a Lonely Hunter",
"The Heart Is Deceitful Above All Things",
"His Dark Materials",
"The House of Mirth",
"How Sleep the Brave",
"I Know Why the Caged Bird Sings",
"I Sing the Body Electric",
"I Will Fear No Evil",
"If I Forget Thee Jerusalem",
"If Not Now, When?",
"In a Dry Season",
"In a Glass Darkly",
"In Death Ground",
"In Dubious Battle",
"An Instant in the Wind",
"It's a Battlefield",
"Jacob Have I Loved",
"O Jerusalem!",
"Jesting Pilate",
"The Last Enemy",
"The Last Temptation",
"The Lathe of Heaven",
"Let Us Now Praise Famous Men",
"Lilies of the Field",
"This Lime Tree Bower",
"The Line of Beauty",
"The Little Foxes",
"Little Hands Clapping",
"Look Homeward, Angel",
"Look to Windward",
"The Man Within",
"Many Waters",
"A Many-Splendoured Thing",
"The Mermaids Singing",
"The Millstone",
"The Mirror Crack'd from Side to Side",
"Moab Is My Washpot",
"The Monkey's Raincoat",
"A Monstrous Regiment of Women",
"The Moon by Night",
"Mother Night",
"The Moving Finger",
"The Moving Toyshop",
"Mr Standfast",
"Nectar in a Sieve",
"The Needle's Eye",
"Nine Coaches Waiting",
"No Country for Old Men",
"No Highway",
"Noli Me Tangere",
"No Longer at Ease",
"Now Sleeps the Crimson Petal",
"Number the Stars",
"Of Human Bondage",
"Of Mice and Men",
"Oh! To be in England",
"The Other Side of Silence",
"The Painted Veil",
"Pale Kings and Princes",
"The Parliament of Man",
"Paths of Glory",
"A Passage to India",
"O Pioneers!",
"Postern of Fate",
"Precious Bane",
"The Proper Study",
"Quo Vadis",
"Recalled to Life",
"Ring of Bright Water",
"The Road Less Traveled",
"A Scanner Darkly",
"Shall not Perish",
"The Skull Beneath the Skin",
"The Soldier's Art",
"Some Buried Caesar",
"Specimen Days",
"The Stars' Tennis Balls",
"Stranger in a Strange Land",
"Such, Such Were the Joys",
"A Summer Bird-Cage",
"The Sun Also Rises",
"Surprised by Joy",
"A Swiftly Tilting Planet",
"Taming a Sea Horse",
"Tender Is the Night",
"Terrible Swift Sword",
"That Good Night",
"That Hideous Strength",
"Things Fall Apart",
"This Side of Paradise",
"Those Barren Leaves",
"Thrones, Dominations",
"Tiger! Tiger!",
"A Time of Gifts",
"Time of our Darkness",
"Time To Murder And Create",
"Tirra Lirra by the River",
"To a God Unknown",
"To Sail Beyond the Sunset",
"To Say Nothing of the Dog",
"To Your Scattered Bodies Go",
"The Torment of Others",
"Unweaving the Rainbow",
"Vanity Fair",
"Vile Bodies",
"The Violent Bear It Away",
"Waiting for the Barbarians",
"The Waste Land",
"The Way of All Flesh",
"The Way Through the Woods",
"The Wealth of Nations",
"What's Become of Waring",
"When the Green Woods Laugh",
"Where Angels Fear to Tread",
"The Widening Gyre",
"Wildfire at Midnight",
"The Wind's Twelve Quarters",
"The Wings of the Dove",
"The Wives of Bath",
"The World, the Flesh and the Devil",
"The Yellow Meads of Asphodel"]

def GetRandomTitle():
  index = random.randint(0,len(titles) - 1)
  return titles[index]



authors = ["William Faulkner",
"Carlo Fruttero and Franco Lucentini",
"Aldous Huxley",
"Eugene O'Neill",
"Sidney Howard",
"W. Somerset Maugham",
"Vita Sackville-West",
"Robert Penn Warren",
"Michael Morpurgo",
"Madeleine L'Engle",
"Aldous Huxley",
"Brian Keenan",
"George Bernard Shaw",
"William Faulkner",
"John Grisham",
"Michael Moorcock",
"Val McDermid",
"Aldous Huxley",
"Noël Coward",
"James Ellroy",
"Alastair Reynolds",
"Rosemary Sutcliff",
"Françoise Sagan",
"Colin Wilson",
"Dee Brown",
"Agatha Christie",
"Elizabeth Smart",
"O. Henry",
"Dan Simmons",
"Robert B. Parker",
"P. D. James",
"Dorothy L. Sayers",
"John Kennedy Toole",
"Iain M. Banks",
"Iain Crichton Smith",
"P. D. James",
"Charles Dickens",
"Mark Haddon",
"H. E. Bates",
"Haruki Murakami",
"Philip Reeve",
"John Gunther",
"Aldous Huxley",
"David Graham",
"Wilfred Owen",
"George R. R. Martin",
"John Steinbeck",
"William Butler Yeats",
"Agatha Christie",
"Jonathan Safran Foer",
"Aldous Huxley",
"H. E. Bates",
"Howard Spring",
"Edna O'Brien",
"Katharine Hull and Pamela Whitlock",
"Ernest Hemingway",
"Thomas Hardy",
"Søren Kierkegaard",
"Roger Zelazny",
"Ernest Hemingway",
"Edmund Crispin",
"James Jones",
"Barbara Pym",
"William Manchester",
"Ray Bradbury",
"Henry James",
"Margaret Mitchell",
"John Steinbeck",
"John Crowley",
"Louis Bromfield",
"Evelyn Waugh",
"Dorothy L. Sayers",
"Carson McCullers",
"JT LeRoy",
"Philip Pullman",
"Edith Wharton",
"H. E. Bates",
"Maya Angelou",
"Ray Bradbury",
"Robert A. Heinlein",
"William Faulkner",
"Primo Levi",
"Peter Robinson",
"Sheridan Le Fanu",
"David Weber & Steve White",
"John Steinbeck",
"André Brink",
"Graham Greene",
"Katherine Paterson",
"Dominique Lapierre and Larry Collins",
"Aldous Huxley",
"Richard Hillary",
"Val McDermid",
"Ursula K. Le Guin",
"James Agee",
"William Edmund Barrett",
"Conor McPherson",
"Alan Hollinghurst",
"Lillian Hellman",
"Dan Rhodes",
"Thomas Wolfe",
"Iain M. Banks",
"Graham Greene",
"Madeleine L'Engle",
"Han Suyin",
"Val McDermid",
"Margaret Drabble",
"Agatha Christie",
"Stephen Fry",
"Robert Crais",
"Laurie R. King",
"Madeleine L'Engle",
"Kurt Vonnegut",
"Agatha Christie",
"Edmund Crispin",
"John Buchan",
"Kamala Markandaya",
"Margaret Drabble",
"Mary Stewart",
"Cormac McCarthy",
"Nevil Shute",
"José Rizal",
"Chinua Achebe",
"H. E. Bates",
"Lois Lowry",
"W. Somerset Maugham",
"John Steinbeck",
"H. E. Bates",
"André Brink",
"W. Somerset Maugham",
"Robert B. Parker",
"Paul Kennedy",
"Humphrey Cobb",
"E. M. Forster",
"Willa Cather",
"Agatha Christie",
"Mary Webb",
"Isaac Asimov",
"Henryk Sienkiewicz",
"Reginald Hill",
"Gavin Maxwell",
"M. Scott Peck",
"Philip K. Dick",
"William Faulkner",
"P. D. James",
"Anthony Powell",
"Rex Stout",
"Michael Cunningham",
"Stephen Fry",
"Robert A. Heinlein",
"George Orwell",
"Margaret Drabble",
"Ernest Hemingway",
"C. S. Lewis",
"Madeleine L'Engle",
"Robert B. Parker",
"F. Scott Fitzgerald",
"Bruce Catton",
"NJ Crisp",
"C. S. Lewis",
"Chinua Achebe",
"F. Scott Fitzgerald",
"Aldous Huxley",
"Dorothy L. Sayers",
"Rudyard Kipling short story",
"Patrick Leigh Fermor",
"Stephen Gray",
"Lawrence Block",
"Jessica Anderson",
"John Steinbeck",
"Robert A. Heinlein",
"Connie Willis",
"Philip José Farmer",
"Val McDermid",
"Richard Dawkins",
"William Makepeace Thackeray",
"Evelyn Waugh",
"Flannery O'Connor",
"J.M. Coetzee",
"T. S. Eliot",
"Samuel Butler",
"Colin Dexter",
"Adam Smith",
"Anthony Powell",
"H. E. Bates",
"E. M. Forster",
"Robert B. Parker",
"Mary Stewart",
"Ursula Le Guin",
"Henry James",
"Susan Swan",
"Mary Elizabeth Braddon",
"H. E. Bates"]

def GetRandomAuthor():
  index = random.randint(0,len(authors) - 1)
  return authors[index]



paragraphs = ["Nostra aetate, in qua genus humanum in dies arctius unitur et necessitudines inter varios populos augentur, Ecclesia attentius considerat quae sit sua habitudo ad religiones non-christianas. In suo munere unitatem et caritatem inter homines, immo et inter gentes, fovendi ea imprimis hic considerat quae hominibus sunt communia et ad mutuum consortium ducunt.",
"Homines a variis religionibus responsum exspectant de reconditis condicionis humanae aenigmatibus, quae sicut olim et hodie corda hominum intime commovent, quid sit homo, quis sensus et finis vitae nostrae, quid bonum et quid peccatum, quem ortum habeant dolores et quem finem, quae sit via ad veram felicitatem obtinendam, quid mors, iudicium et retributio post mortem, quid demum illud ultimum et ineffabile mysterium quod nostram existentiam amplectitur, ex quo ortum sumimus et quo tendimus.",
"Iam ab antiquo usque ad tempus hodiernum apud diversas gentes invenitur quaedam perceptio illius arcanae virtutis, quae cursui rerum et eventibus vitae humanae praesens est, immo aliquando agnitio Summi Numinis vel etiam Patris. Quae perceptio atque agnitio vitam earum intimo sensu religioso penetrant. Religiones vero cum progressu culturae connexae subtilioribus notionibus et lingua magis exculta ad easdem quaestiones respondere satagunt.",
"Ita in Hinduismo homines mysterium divinum scrutantur et exprimunt inexhausta fecunditate mythorum et acutis conatibus philosophiae, atque liberationem quaerunt ab angustiis nostrae condicionis vel per formas vitae asceticae vel per profundam meditationem vel per refugium ad Deum cum amore et confidentia.",
"In Buddhismo secundum varias eius formas radicalis insufficientia mundi huius mutabilis agnoscitur et via docetur qua homines, animo devoto et confidente, sive statum perfectae liberationis acquirere, sive, vel propriis conatibus vel superiore auxilio innixi, ad summam illuminationem pertingere valeant. Sic ceterae quoque religiones, quae per totum mundum inveniuntur, inquietudini cordis hominum variis modis occurrere nituntur proponendo vias, doctrinas scilicet ac praecepta vitae, necnon ritus sacros.",
"Ecclesia catholica nihil eorum, quae in his religionibus vera et sancta sunt, reicit. Sincera cum observantia considerat illos modos agendi et vivendi, illa praecepta et doctrinas, quae, quamvis ab iis quae ipsa tenet et proponit in multis discrepent, haud raro referunt tamen radium illius Veritatis, quae illuminat omnes homines. Annuntiat vero et annuntiare tenetur indesinenter Christum, qui est via et veritas et vita , in quo homines plenitudinem vitae religiosae inveniunt, in quo Deus omnia Sibi reconciliavit.",
"Filios suos igitur hortatur, ut cum prudentia et caritate per colloquia et collaborationem cum asseclis aliarum religionum, fidem et vitam christianam testantes, illa bona spiritualia et moralia necnon illos valores socio-culturales, quae apud eos inveniuntur, agnoscant, servent et promoveant.",
"Ecclesia cum aestimatione quoque Muslimos respicit qui unicum Deum adorant, viventem et subsistentem, misericordem et omnipotentem, Creatorem caeli et terrae, homines allocutum, cuius occultis etiam decretis toto animo se submittere student, sicut Deo se submisit Abraham ad quem fides islamica libenter sese refert. Iesum, quem quidem ut Deum non agnoscunt, ut prophetam tamen venerantur, matremque eius virginalem honorant Mariam et aliquando eam devote etiam invocant. Diem insuper iudicii expectant cum Deus omnes homines resuscitatos remunerabit. Exinde vitam moralem aestimant et Deum maxime in oratione, eleemosynis et ieiunio colunt.",
"Quodsi in decursu saeculorum inter Christianos et Muslimos non paucae dissensiones et inimicitiae exortae sint, Sacrosancta Synodus omnes exhortatur, ut, praeterita obliviscentes, se ad comprehensionem mutuam sincere exerceant et pro omnibus hominibus iustitiam socialem, bona moralia necnon pacem et libertatem communiter tueantur et promoveant.",
"Mysterium Ecclesiae perscrutans, Sacra haec Synodus meminit vinculi, quo populus Novi Testamenti cum stirpe Abrahae spiritualiter coniunctus est.",
"Ecclesia enim Christi agnoscit fidei et electionis suae initia iam apud Patriarchas, Moysen et Prophetas, iuxta salutare Dei mysterium, inveniri. Confitetur omnes Christifideles, Abrahae filios secundum fidem , in eiusdem Patriarchae vocatione includi et salutem Ecclesiae in populi electi exitu de terra servitutis mystice praesignari. Quare nequit Ecclesia oblivisci se per populum illum, quocum Deus ex ineffabili misericordia sua Antiquum Foedus inire dignatus est, Revelationem Veteris Testamenti accepisse et nutriri radice bonae olivae, in quam inserti sunt rami oleastri Genti. Credit enim Ecclesia Christum, Pacem nostram, per crucem Iudaeos et Gentes reconciliasse et utraque in Semetipso fecisse unum.",
"Semper quoque prae oculis habet Ecclesia verba Apostoli Pauli de cognatis eius, quorum adoptio est filiorum et gloria et testamentum et legislatio et obsequium et promissa, quorum patres et ex quibus est Christus secundum carnem, filius Mariae Virginis. Recordatur etiam ex populo iudaico natos esse Apostolos, Ecclesiae fundamenta et columnas, atque plurimos illos primos discipulos, qui Evangelium Christi mundo annuntiaverunt.",
"Teste Sacra Scriptura, Ierusalem tempus visitationis suae non cognovit, atque Iudaei magna parte Evangelium non acceperunt, immo non pauci diffusioni eius se opposuerunt. Nihilominus, secundum Apostolum, Iudaei Deo, cuius dona et vocatio sine paenitentia sunt, adhuc carissimi manent propter Patres. Una cum Prophetis eodemque Apostolo Ecclesia diem Deo soli notum expectat, quo populi omnes una voce Dominum invocabunt et servient ei umero uno.",
"Cum igitur adeo magnum sit patrimonium spirituale Christianis et Iudaeis commune, Sacra haec Synodus mutuam utriusque cognitionem et aestimationem, quae praesertim studiis biblicis et theologicis atque fraternis colloquiis obtinetur, fovere vult et commendare.",
"Etsi auctoritates Iudaeorum cum suis asseclis mortem Christi urserunt, tamen ea quae in passione Eius perpetrata sunt nec omnibus indistincte Iudaeis tunc viventibus, nec Iudaeis hodiernis imputari possunt. Licet autem Ecclesia sit novus populus Dei, Iudaei tamen neque ut a Deo reprobati neque ut maledicti exhibeantur, quasi hoc ex Sacris Litteris sequatur. Ideo curent omnes ne in catechesi et in verbi Dei praedicatione habenda quidquam doceant, quod cum veritate evangelica et spiritu Christi non congruat.",
"Praeterea, Ecclesia, quae omnes persecutiones in quosvis homines reprobat, memor communis cum Iudaeis patrimonii, nec rationibus politicis sed religiosa caritate evangelica impulsa, odia, persecutiones, antisemitismi manifestationes, quovis tempore et a quibusvis in Iudaeos habita, deplorat.",
"Ceterum Christus, uti semper tenuit et tenet Ecclesia, propter peccata omnium hominum voluntarie passionem suam et mortem immensa caritate obiit, ut omnes salutem consequantur. Ecclesiae praedicantis ergo est annuntiare crucem Christi tamquam signum universalis Dei amoris et fontem omnis gratiae.",
"Nequimus vero Deum omnium Patrem invocare, si erga quosdam homines, ad imaginem Dei creatos, fraterne nos gerere renuimus. Habitudo hominis ad Deum Patrem et habitudo hominis ad homines fratres adeo connectuntur, ut Scriptura dicat, qui non diligit, non novit Deum.",
"Fundamentum ergo tollitur omni theoriae vel praxi quae inter hominem et hominem, inter gentem et gentem, discrimen quoad humanam dignitatem et iura exinde dimanantia inducit.",
"Ecclesia igitur quamvis hominum discriminationem aut vexationem stirpis vel coloris, condicionis vel religionis causa factam tamquam a Christi mente alienam, reprobat. Proinde, Christifideles Sacra Synodus, vestigia Sanctorum Apostolorum Petri et Pauli premens, ardenter obsecrat ut conversationem... inter gentes habentes bonam, si fieri potest, quod in eis est cum omnibus hominibus pacem habeant, ita ut vere sint filii Patris qui in caelis est."]

def GetRandomText():
  index = random.randint(0,len(paragraphs) - 1)
  return paragraphs[index]



pictures = ["sea.jpeg",
"island.jpeg",
"utopia.jpeg",
"hill.jpeg",
"arcadia.jpeg",
"oasis.jpeg",
"cloud.jpeg",
"waterfall.jpeg",
"mountain.jpeg",
"lake.jpeg",
"river.jpeg",
"desert.jpeg",
"delta.jpeg",
"quagmire.jpeg",
"mesa.jpeg",
"pasture.jpeg"]

def GetRandomPicture():
  index = random.randint(0,len(pictures) - 1)
  return pictures[index]



