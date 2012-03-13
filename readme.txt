

     -=================================-
               StopGateGui
     -=================================-
	 
				versioon 0.3.4
			uuendatud 1.02.2011


| Sisukord
+==========-

	1. Sissejuhatus
		1.a M�ngust
	2. Installeerimine
	3. M�ngu kasutamine
		3.a Tavam�ng
		3.b Bottide lisamine
		3.c Logide vaatamine ja -lisamine
	4. Lisad
	5. Kontaktandmed
	6. TODO
	
	
| 1. Sissejuhatus
+=================-
	
	StopGateGui on kasutajaliides, mis on kirjutatud
	2011. aasta m�nguprogrammeerimise v�istluse 
	jaoks Karl Aksel Puulmanni poolt kasutades Pythonit
	ja pygame.
	
	Lisaks kasutajaliidesele on m�eldud ka sellele, et
	kasutaja saaks oma botte kiiresti ja lihtsalt lisada
	ning anal��sida serverist (http://gg.cs.ut.ee) v�etud
	logisid.

	
| 1. M�ngust
+============-

	Stop-Gate'i m�ngitakse ruudukujulisel m�ngulaual 
	m��tmetega 12x12. Nuppudena kasutatakse nuppe 
	m��tmetega 2x1, st m�ngulauale asetatuna katavad nad 
	�ra t�pselt kaks m�ngulaua ruutu.

	�ksteise vastu m�ngivad kaks m�ngijat, kes sooritavad 
	k�ike kordam��da, kusjuures k�igu sooritamiseks peab 
	m�ngija asetama lauale �he nupu. Alustaja peab oma nupud 
	paigutama vertikaalselt, tema vastasm�ngija horisontaalselt. 
	Kaotab see, kes esimesena k�iku sooritada ei saa.

	Nuppe on m�lemal m�ngijal piisavalt m�ngulaua t�itmiseks 
	ja samal m�ngulaua ruudul ei tohi olla �le �he nupu. 
	M�ngu alguses on laud t�hi.
	
	Autor on teinud v�ikese muudatuse v�rreldes m�ngujuhisega,
	nimelt on �lemine vasak ruut kordinaatidega (0, 0) ja parem 
	alumine ruut (11, 11). Muudatus oli tehtud pidades silmas
	�ldiseid lauam�ngude �lesehitusi ja et seisude lugemine
	oleks kasutajale lihtsam. N�udeid bottidele see ei m�juta, 
	pilt ilmub ekraanile lihtsalt 90 kraadise nurga all.
	
	
| 2. Installeerimine
+===================-
	
	StopGateGui vajab t��ks :
		python versioon 2.5 v�i 2.6
			http://www.python.org/download/releases/2.6/
		pygame mis sobib vastavale versioonile
			http://www.pygame.org/download.shtml
	Windowsi kasutajad pakkige salvestage python kausta 
	C:\Python25 v�i C:\Python26.

			
| 3. M�ngu kasutamine
+=====================-
	
	Windowsi all m�ngu k�ivitamiseks tehke topeltkl�ps 
	launcher.bat'il.
	Linuxis tuleks kasutada start.sh'd
	
	Lisaks on v�imalik minna k�sureal StopGateGui kausta ning
	seej�rel sisestada k�sk "python StopGate.py". Sellisel
	juhul peab olema pythoni kodukaust olema lisatud PATHi.

	Kui lisada argumentidena kaks numbrit, siis paneb arvuti 
	m�ngima kaks boti v�i inimm�ngija. 
	N�iteks "python StopGate.py 0 3" paneb m�ngima esimese 
	ja neljanda boti (kui on alla 4 boti, siis selle asemel 
	inimm�ngija).

	
| 3.a Tavam�ng
+==============-
	
	Uut m�ngu saab alustada vajutades tekkinud aknas nupul 
	"Uus m�ng" ning seej�rel valides kaks m�ngijat. Inimene 
	on tavam�ngija, �lej��nud valikutest on erinevad botid.
	Seej�rel tuleks vajutada nuppu "Alusta m�ngu".
	
	Inimm�ngija saab asetada nuppe liikudes hiirega m�nele ruudule 
	ja vajutades vasakut hiireklahvi.
	
	Peale m�ngu algust saab siseneda men��sse kasutades klahvi 
	"ESC" v�i klikkides paremal all nurgas olevat teksti.
	
	Paremal �leval olev skooritabel n�itab, mitmele eri ruudule 
	on kummagil m�ngijal veel v�imalik k�ia. Tegu ei ole kindlasti
	optimaalse hindamiss�steemiga.
	
	"M�ngu k�ik" n�itab seni tehtud k�ike (mis v�ljastatakse ka 
	konsooli). Lisaks v�ljastatakse sinna m�ngu tulemused ja
	vajadusel lisainfo (nt kui bot tegi vigase k�igu).
	
	"Statistika" n�itab, palju on kumbki m�ngija kulutanud aega 
	oma viimasele k�igule ja palju kokku.
	

| 3.b Bottide lisamine
+======================-
	
	Oma botti saab lisada muutes settings.ini faili ja lisades 
	sinna l�ppu uus rida, mis sisaldab faili nime (.py faili 
	korral ka laiendit) ja roboti nime, mida eraldab 
	v�rdusm�rk. 
	N�iteks: uus_bot.py MinuRobot
	See fail tuleks seej�rel t�sta /Scripts kausta.
	

| 3.c Logide vaatamine ja lisamine
+==================================-

	Logisid saab vaadata klikkides men��s nupul "Logi vaataja",
	valides logi ja vajutades nuppu "Alusta m�ngu"
	
	Kui esitamine on alanud, saab m�ngus navigeerida kasutades
	vasakut ja paremat nooleklahvi.
	
	Logisid saab lisades, t�stes m�ni serverist kopeeritud logi
	v�i salvestatud lehek�lg /Logs kausta.
	PS: Logide vormingus tuleb s�ilitada esimesed viis rida
		("Vertikaalne (alustaja).." jne).


| 4. Lisad
+==========-
	
	\Extra kausta alt v�ib leida j�rgnevad scriptid:
	logcrawler.py - k�sureaprogramm, mis v�tab argumentideks
					kaks t�isarvu ja mis t�mbab serverist
					k�ik logid sellest vahemikust ning t��tleb 
					nad
	
	ranker.py - 	k�sureaprogramm, mis kuvab samas kaustas
					olevate logide p�hjal statistikat.
					Lisaks kui programmile anda argumendiks
					boti nimi, v�ljastab t�psemat infot
					selle boti kohta.
	

| 5. Kontakt
+============-
	
	Autor - Karl Aksel Puulmann
	email - oxymaccy@gmail.com
	
	Teated vigadest ja ettepanekud on teretulnud.

| 6. TODO
+=========-
	
	Lisada k�ik edasi/tagasi nupud logide vaatamisele
	Nime muutmise v�imalus inimm�ngijatele
	Klaviatuuriklahvidega men��s liikumine intuitiivsemaks
	T�psem ajahaldus (mitte arvestada joonistamiseks kulunud
		aega).
	Valikulised hindamisskeemid