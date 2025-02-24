# Vaizdo Įrašo Kokybės Analizė ir Klasterizacija

Ši programa skirta atlikti vaizdo įrašo kokybės analizę ir klasterizaciją. Ji išskiria kadrus iš įvesto vaizdo įrašo, apskaičiuoja kiekvieno kadro kokybės metrikas ir pagal jas suskirsto kadrus į grupes. Programa suteikia galimybę naudoti dvi skirtingas kokybės vertinimo metodikas:

- **Laplazo operatoriaus metrika** – tradicinis metodas, skirtas įvertinti kadrų aštrumą (blur). Mažesnė Laplaso variacijos reikšmė rodo labiau suliejusį ir galimai sugadintą kadrą.
- **BRISQUE modelis** – modernus AI pagrindu veikiantis metodas, skirtas objektyviai įvertinti vaizdo kokybę. Aukštesnis BRISQUE balas rodo blogesnę kokybę.

Tai Python pagrindu veikiančios programos, skirtos:

- Išskirstyti įvestą vaizdo įrašą į atskirus kadrus.

- Įvertinti kiekvieno kadro kokybę (pvz., sugadinimą dėl kameros judėjimo naudojant Laplaso operatoriaus dispersiją bei apšvietimo lygį).

- Naudojant klasterizavimo metodus (pvz., K-Means), suskirstyti kadrus į grupes pagal sugadinimo laipsnį.

- Identifikuoti labiausiai sugadintus kadrus ir pažymėti juos raudonu rėmeliu naujame vaizdo įraše arba paruoštoje analizės ataskaitoje.

## Funkcionalumas

**Kadrų išskyrimas:** Naudoja OpenCV biblioteką kadrų išskyrimui iš įvesto vaizdo įrašo.
**Kadro kokybės įvertinimas:** 
  - Įvertina kadrų aštrumą, matuojant Laplaso operatoriaus dispersiją.
  - Apskaičiuoja vidutinį kadrų apšvietimo lygį.
  - Arba/ir Naudojant BRISQUE modelį, objektyviai įvertinama vaizdo kokybė.
**Klasterizacija:** Naudoja normalizuotus duomenis ir K-Means algoritmą, kad suskirstytų kadrus į grupes.
**Sugadintų kadrų identifikavimas:** Pasirenkamas klasteris su mažiausiu blur metrikos vidurkiu, laikomas labiausiai sugadintų kadrų grupe.
**Vizualus pažymėjimas:** Sugadinti kadrai pažymimi raudonu rėmeliu ir įrašomi į naują vaizdo įrašą.
**Duomenų vizualizacija:** Programa generuoja diagramą, kurioje pavaizduotas kadrų aštrumo metrikos pasiskirstymas bei klasterių susiskirstymas.

## Diegimo instrukcijos

1. **Suklonuokite repozitoriją:**

```bash
git clone https://github.com/monikutee/video_frames_analysis.git
cd video_frames_analysis
```

2. **Sukurkite virtualią aplinką ir aktyvuokite ją:**

```bash
python -m venv venv
# Linux/MacOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

3. **Įdiekite priklausomybes:**

```bash
pip install -r requirements.txt
```

## Naudojimo instrukcijos

Norint analizuoti vaizdo įrašą **su BRISQUE** rodikliu:

```bash
python video_brisque.py --video input.mp4 --output output_brisque.mp4
```

Norint analizuoti vaizdo įrašą **be BRISQUE** rodikliu:

```bash
python laplacian.py --video input.mp4 --output output_laplacian.mp4
```

## Programos Veikimo Principas

**Kadrų išskyrimas:**
Naudojant cv2.VideoCapture, iš įvesto vaizdo įrašo išskiriami visi kadrai, o taip pat gaunama vaizdo kadrų dažnio (FPS) reikšmė.

**Metrikų apskaičiavimas:**
 - Laplaso metrika: Apskaičiuojama naudojant cv2.Laplacian.
 - Apšvietimo lygis: Nustatomas apskaičiuojant vidutinę kadrų šviesumą.
 - BRISQUE balas: Apskaičiuojamas naudojant BRISQUE modelio biblioteką.
   
**Duomenų normalizavimas ir klasterizacija:**
Gauti trijų savybių duomenys normalizuojami naudojant StandardScaler, o K-Means algoritmas suskirsto kadrus į tris grupes.

**Blogiausios kokybės kadrų identifikavimas:**
Klasteris su aukščiausiu vidutiniu BRISQUE arba blur balu laikomas blogiausios kokybės grupės atstovu.

**Rezultatų išvestis:**
Sugadinti kadrai pažymimi raudonu rėmeliu, o naujas vaizdo įrašas įrašomas nurodytu keliu. Taip pat pateikiama diagrama, rodanti kadrų blur metrikos pasiskirstymą bei klasterių susiskirstymą.

## Iškilusios problemos

BRISQUE sunkiai instaliavosi ant MacOS, problemos del libsvm-official, bet stackoverflow padėjo.

