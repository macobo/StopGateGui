

     -=================================-
               StopGateGui
     -=================================-
	 
				versioon 0.3.4
			uuendatud 1.02.2011


| Sisukord
+==========-

	1. Sissejuhatus
		1.a Mängust
	2. Installeerimine
	3. Mängu kasutamine
		3.a Tavamäng
		3.b Bottide lisamine
		3.c Logide vaatamine ja -lisamine
	4. Lisad
	5. Kontaktandmed
	6. TODO
	
	
| 1. Sissejuhatus
+=================-
	
	StopGateGui on kasutajaliides, mis on kirjutatud
	2011. aasta mänguprogrammeerimise võistluse 
	jaoks Karl Aksel Puulmanni poolt kasutades Pythonit
	ja pygame.
	
	Lisaks kasutajaliidesele on mõeldud ka sellele, et
	kasutaja saaks oma botte kiiresti ja lihtsalt lisada
	ning analüüsida serverist (http://gg.cs.ut.ee) võetud
	logisid.

	
| 1. Mängust
+============-

	Stop-Gate'i mängitakse ruudukujulisel mängulaual 
	mõõtmetega 12x12. Nuppudena kasutatakse nuppe 
	mõõtmetega 2x1, st mängulauale asetatuna katavad nad 
	ära täpselt kaks mängulaua ruutu.

	Üksteise vastu mängivad kaks mängijat, kes sooritavad 
	käike kordamööda, kusjuures käigu sooritamiseks peab 
	mängija asetama lauale ühe nupu. Alustaja peab oma nupud 
	paigutama vertikaalselt, tema vastasmängija horisontaalselt. 
	Kaotab see, kes esimesena käiku sooritada ei saa.

	Nuppe on mõlemal mängijal piisavalt mängulaua täitmiseks 
	ja samal mängulaua ruudul ei tohi olla üle ühe nupu. 
	Mängu alguses on laud tühi.
	
	Autor on teinud väikese muudatuse võrreldes mängujuhisega,
	nimelt on ülemine vasak ruut kordinaatidega (0, 0) ja parem 
	alumine ruut (11, 11). Muudatus oli tehtud pidades silmas
	üldiseid lauamängude ülesehitusi ja et seisude lugemine
	oleks kasutajale lihtsam. Nõudeid bottidele see ei mõjuta, 
	pilt ilmub ekraanile lihtsalt 90 kraadise nurga all.
	
	
| 2. Installeerimine
+===================-
	
	StopGateGui vajab tööks :
		python versioon 2.5 või 2.6
			http://www.python.org/download/releases/2.6/
		pygame mis sobib vastavale versioonile
			http://www.pygame.org/download.shtml
	Windowsi kasutajad pakkige salvestage python kausta 
	C:\Python25 või C:\Python26.

			
| 3. Mängu kasutamine
+=====================-
	
	Windowsi all mängu käivitamiseks tehke topeltklõps 
	launcher.bat'il.
	Linuxis tuleks kasutada start.sh'd
	
	Lisaks on võimalik minna käsureal StopGateGui kausta ning
	seejärel sisestada käsk "python StopGate.py". Sellisel
	juhul peab olema pythoni kodukaust olema lisatud PATHi.

	Kui lisada argumentidena kaks numbrit, siis paneb arvuti 
	mängima kaks boti või inimmängija. 
	Näiteks "python StopGate.py 0 3" paneb mängima esimese 
	ja neljanda boti (kui on alla 4 boti, siis selle asemel 
	inimmängija).

	
| 3.a Tavamäng
+==============-
	
	Uut mängu saab alustada vajutades tekkinud aknas nupul 
	"Uus mäng" ning seejärel valides kaks mängijat. Inimene 
	on tavamängija, ülejäänud valikutest on erinevad botid.
	Seejärel tuleks vajutada nuppu "Alusta mängu".
	
	Inimmängija saab asetada nuppe liikudes hiirega mõnele ruudule 
	ja vajutades vasakut hiireklahvi.
	
	Peale mängu algust saab siseneda menüüsse kasutades klahvi 
	"ESC" või klikkides paremal all nurgas olevat teksti.
	
	Paremal üleval olev skooritabel näitab, mitmele eri ruudule 
	on kummagil mängijal veel võimalik käia. Tegu ei ole kindlasti
	optimaalse hindamissüsteemiga.
	
	"Mängu käik" näitab seni tehtud käike (mis väljastatakse ka 
	konsooli). Lisaks väljastatakse sinna mängu tulemused ja
	vajadusel lisainfo (nt kui bot tegi vigase käigu).
	
	"Statistika" näitab, palju on kumbki mängija kulutanud aega 
	oma viimasele käigule ja palju kokku.
	

| 3.b Bottide lisamine
+======================-
	
	Oma botti saab lisada muutes settings.ini faili ja lisades 
	sinna lõppu uus rida, mis sisaldab faili nime (.py faili 
	korral ka laiendit) ja roboti nime, mida eraldab 
	võrdusmärk. 
	Näiteks: uus_bot.py MinuRobot
	See fail tuleks seejärel tõsta /Scripts kausta.
	

| 3.c Logide vaatamine ja lisamine
+==================================-

	Logisid saab vaadata klikkides menüüs nupul "Logi vaataja",
	valides logi ja vajutades nuppu "Alusta mängu"
	
	Kui esitamine on alanud, saab mängus navigeerida kasutades
	vasakut ja paremat nooleklahvi.
	
	Logisid saab lisades, tõstes mõni serverist kopeeritud logi
	või salvestatud lehekülg /Logs kausta.
	PS: Logide vormingus tuleb säilitada esimesed viis rida
		("Vertikaalne (alustaja).." jne).


| 4. Lisad
+==========-
	
	\Extra kausta alt võib leida järgnevad scriptid:
	logcrawler.py - käsureaprogramm, mis võtab argumentideks
					kaks täisarvu ja mis tõmbab serverist
					kõik logid sellest vahemikust ning töötleb 
					nad
	
	ranker.py - 	käsureaprogramm, mis kuvab samas kaustas
					olevate logide põhjal statistikat.
					Lisaks kui programmile anda argumendiks
					boti nimi, väljastab täpsemat infot
					selle boti kohta.
	

| 5. Kontakt
+============-
	
	Autor - Karl Aksel Puulmann
	email - oxymaccy@gmail.com
	
	Teated vigadest ja ettepanekud on teretulnud.

| 6. TODO
+=========-
	
	Lisada käik edasi/tagasi nupud logide vaatamisele
	Nime muutmise võimalus inimmängijatele
	Klaviatuuriklahvidega menüüs liikumine intuitiivsemaks
	Täpsem ajahaldus (mitte arvestada joonistamiseks kulunud
		aega).
	Valikulised hindamisskeemid