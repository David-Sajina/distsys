# DIST-SYS Projekt 01
Prvi projekt DIST-SYS
0. Fake E-ucenje API microservis (M0). Sastoji se od DB i jedne rute koja
vraća github linkove na zadaće. Prilikom pokretanja servisa, provjerava
se postoje li podaci u DB. Ukoliko ne postoje, pokreće se funkcija koja
popunjava DB s testnim podacima (10000). Kad microservis zaprimi
zahtjev za dohvaćanje linkova, uzima maksimalno 100 redataka podataka
iz DB-a.
• Hints
– Fake Dataset (224MB compressed, 1GB uncompressed)
1. Microservis asinkrono poziva e-učenje API (M1), te prosljeđuje podatke
kao dictionary Worker tokenizer (WT) microservisu.
2. WT microservis uzima dictionary. Uzima samo redove gdje username
počinje na w. Prosljeđuje kod 4. microservisu.
3. WT microservis uzima dictionary. Uzima samo redove gdje username
počinje na d. Prosljeđuje kod 4. microservisu.
4. microservis sastoji od rute (/gatherData) sprema se Python kod u listu.
Ako ima više od 10 elemenata unutar liste asinkrono se kreiraju svi file-ovi
iz liste.

EXTRA

1.Proširen Fake M1. Nakon što dobije kolekciju URL-ova asinkrono preuzima
repozitorije sa zadaćama. Asinkrono asinkrono čita red po red Python
datoteke (M1+), te prosljeđuje stringove WTMs.
<br>
• Hints : GitPython, base64

• Ideja je da baza bude prazna kad se prvi put pokrecu svi microservisi. Ako
taj dio zelite testirati dal vam radi, samo kreirajte novu bazu podataka
(koja ce biti prazna) i upišite Fake dataset podatke koje trebaju. Slobodno
dodajte jos jedan column u DB u kojem ce se nalaziti content file-a iz Fake
dataset-a (trebali bi ste naci jedan key unutar tog json-a).