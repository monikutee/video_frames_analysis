## Vaizdo Įrašo Kokybės Analizė ir Klasterizacija

Ši programa skirta atlikti vaizdo įrašo kokybės analizę ir klasterizaciją. Ji išskiria kadrus iš įvesto vaizdo įrašo, apskaičiuoja kiekvieno kadro kokybės metrikas ir pagal jas suskirsto kadrus į grupes. Programa suteikia galimybę naudoti dvi skirtingas kokybės vertinimo metodikas:

- **Laplazo operatoriaus metrika** – tradicinis metodas, skirtas įvertinti kadrų aštrumą (blur). Mažesnė Laplaso variacijos reikšmė rodo labiau suliejusį ir galimai sugadintą kadrą.
- **BRISQUE modelis** – modernus AI pagrindu veikiantis metodas, skirtas objektyviai įvertinti vaizdo kokybę. Aukštesnis BRISQUE balas rodo blogesnę kokybę.

Tai Python pagrindu veikiančios programos, skirtos:

- Išskirstyti įvestą vaizdo įrašą į atskirus kadrus.

- Įvertinti kiekvieno kadro kokybę (pvz., sugadinimą dėl kameros judėjimo naudojant Laplaso operatoriaus dispersiją bei apšvietimo lygį).

- Naudojant klasterizavimo metodus (pvz., K-Means), suskirstyti kadrus į grupes pagal sugadinimo laipsnį.

- Identifikuoti labiausiai sugadintus kadrus ir pažymėti juos raudonu rėmeliu naujame vaizdo įraše arba paruoštoje analizės ataskaitoje.

# Funkcionalumas

**Kadrų išskyrimas:** Naudoja OpenCV biblioteką kadrų išskyrimui iš įvesto vaizdo įrašo.
**Kadro kokybės įvertinimas:** - Įvertina kadrų aštrumą, matuojant Laplaso operatoriaus dispersiją. - Naudojant BRISQUE modelį, objektyviai įvertinama vaizdo kokybė.
**Klasterizacija:** Naudoja normalizuotus duomenis ir K-Means algoritmą, kad suskirstytų kadrus į grupes.
**Sugadintų kadrų identifikavimas:** Pasirenkamas klasteris su mažiausiu blur metrikos vidurkiu, laikomas labiausiai sugadintų kadrų grupe.
**Vizualus pažymėjimas:** Sugadinti kadrai pažymimi raudonu rėmeliu ir įrašomi į naują vaizdo įrašą.
**Duomenų vizualizacija:** Programa generuoja diagramą, kurioje pavaizduotas kadrų aštrumo metrikos pasiskirstymas bei klasterių susiskirstymas.

komanda:

```bash
python video_brisque.py --video {analyze_video.mp4} --output {new_video_name.mp4}
```

pavyzdine komanda
brisque: python video_brisque.py --video test.mov --output output_b.mp4  
 laplacian: python laplacian.py --video test.mov --output output_l.mp4
