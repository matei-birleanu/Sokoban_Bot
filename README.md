# README SOKOBAN  
**Author:** Bîrleanu Teodor Matei (334CA)  
**Date:** 27.04.2024

---

## Tema 1: Inteligență Artificială

Acest proiect implementează și compară două algoritmi de căutare pentru rezolvarea puzzle-ului Sokoban:  
- **Learning Real-Time A*** (LRTA*)  
- **Beam Search**

Am introdus modificări conceptuale și tehnice pentru adaptarea euristicilor și îmbunătățirea performanței.

---

## 1. LRTA* (Learning Real-Time A*)

### 1.1 Prezentare generală
LRTA* este o variantă online a A* care nu păstrează o frontieră completă, ci ia decizii pas cu pas. Euristica este adaptivă: se învață și se actualizează la fiecare pas.

### 1.2 Detalii de implementare
- **Frontieră**: Nu există frontieră; se păstrează doar nodul curent.  
- **Euristică adaptivă**: Un dicționar `H[state]` stochează valoarea euristicii pentru fiecare stare; dacă nu există, se inițializează.  
- **Generare succesor**: La fiecare pas, se generează toți succesorii, se evaluează costul `f = g + h`, se alege succesorul cu cel mai mic `f` și se actualizează `H[current]`.  
- **Oprire**: Când se atinge starea finală sau se depășește numărul maxim de pași permis.

### 1.3 Rezultate – Număr de pași
![LRTA* Steps](sokoban_images/chart_0.png)

| Heuristic       | Easy1 | Easy2 | Medium1 | Medium2 | Hard1 | Hard2 | Large1  | Large2  | Super_hard1 |
|-----------------|------:|------:|--------:|--------:|------:|------:|--------:|--------:|------------:|
| Manhattan       |    92 |    18 |     198 |    4681 |  2093 |  4681 |    2802 |    9300 |         568 |
| Hungarian       |   340 |    18 |     206 |    5564 |   679 |   786 |    1225 |   99009 |         369 |
| BFS_static      |   214 |    18 |      45 |    8053 |   308 |   417 |     921 |   75685 |        1668 |
| BFS_heuristic   |   210 |    18 |      37 |   10059 |   308 |   529 |     887 |   27427 |        1636 |
| Greedy          |   340 |    18 |     206 |    9037 |   679 |  1146 |    1225 |   93513 |         316 |
| Advanced        |   210 |    18 |      45 |    5997 |   308 |   529 |     887 |  145831 |        2478 |
| BFS_Hung        |   150 |    18 |      45 |    5997 |    64 |  1039 |    1209 |  143675 |        2478 |
| Misplace_box    |  1048 |   578 |   18793 |   24097 | 10632 |  1420 |  109649 | 1000001 |      625765 |
| Box_to_goal     |  1016 |   550 |    2359 |    3716 |   803 |  1783 |   16530 |   67152 |        1604 |

**Observații LRTA***:  
- **Misplace_box** este cea mai slabă: sute de mii până la milioane de pași pe hărți mari.  
- **Manhattan** e eficientă pe hărți mici, dar costă mult pe hărți mari.  
- **BFS_static** și **BFS_heuristic** reduc semnificativ spațiul de căutare pe testele mari.

![LRTA* Expanded States](sokoban_images/chart_4.png)

---

## 2. Beam Search

### 2.1 Prezentare generală
Beam Search ține un set restrâns de stări („beam”) și extinde doar cele mai promițătoare la fiecare pas, conform unei euristici.

### 2.2 Detalii de implementare
- Pornire dintr-o singură stare, nu din `k` stări aleatorii.  
- Se evită re-expandarea cu un set `visited`.  
- Fiecare element din beam este un tuplu: `(stare, lista_de_stări, număr_mutări)`.  
- Se alege scorul euristic maxim pentru candidații neexplorați.

### 2.3 Rezultate – Număr de pași
![Beam Search Steps](sokoban_images/chart_3.png)

| Heuristic       | Easy1 | Easy2 | Medium1 | Medium2 | Hard1 | Hard2 | Large1 | Large2 | Super_hard1 |
|-----------------|------:|------:|--------:|--------:|------:|------:|-------:|-------:|------------:|
| Manhattan       |    18 |    10 |      12 |      37 |    31 |    91 |    162 |    116 |          40 |
| Hungarian       |    18 |    10 |      12 |      29 |    38 |    42 |     26 |     33 |          38 |
| BFS_static      |    18 |    10 |      31 |      36 |    26 |    46 |     12 |     24 |          40 |
| BFS_heuristic   |    18 |    10 |      12 |      24 |    31 |    36 |     26 |     46 |          40 |
| Greedy          |    18 |    10 |      12 |      29 |    38 |    42 |     26 |     33 |          41 |
| Advanced        |    18 |    10 |      12 |      24 |    31 |    36 |     26 |     46 |          40 |
| BFS_Hung        |    18 |    10 |      12 |      24 |    31 |    36 |     26 |     46 |          40 |
| Misplace_box    |    30 |    10 |      35 |      28 |    31 |   132 |     54 |    131 |          57 |
| Box_to_goal     |    18 |    10 |      12 |      37 |    31 |    91 |    162 |    116 |          40 |

**Observații Beam Search**:  
- Reduce ordinea de mărime a numărului de pași de la LRTA* la zeci–sute.  
- Performanță uniformă pe testele easy și medium (10–35 pași).  
- Diferențele între euristici sunt atenuate.

![Beam Search Expanded States](sokoban_images/chart_8.png)

---

## 3. Euristici folosite
- **Manhattan**: Sumă de distanțe Manhattan.  
- **Misplace_box**: Număr de cutii neplasate.  
- **Box_to_goal**: Suma distanțelor minime cutie–țintă; suportă Manhattan și Euclidian.  
- **Greedy**: Matching cutie–țintă pas cu pas + distanța jucător–cutie.  
- **Hungarian**: Matching global optim (Hungarian) + distanța jucător–cutie.  
- **BFS_static**: BFS preprocesat per țintă, cache distanțe statice.  
- **BFS_heuristic**: BFS dinamic multi-țintă și de la jucător.  
- **Advanced**: BFS_heuristic + detectare deadlock + penalizări + Manhattan.  
- **BFS_Hung**: Combinează deadlock, BFS static, matching optim și deplasare jucător.

---

## 4. Concluzii generale
- **LRTA*** evidențiază diferențe mari între euristici pe hărți mari.  
- **Beam Search** menține ierarhiile, dar comprima spațiul de căutare cu câteva mii de ori.  
- Euristica rămâne critică: chiar și în Beam Search, una slabă costă câteva mii de stări.

---

## 5. Performanță – Timp de rulare
![Running Time Comparison](sokoban_images/chart_9.png)

---

## 6. Referințe
1. Real-time search (LRTA*) – Turing CS PUB RO [Link](https://turing.cs.pub.ro/blia_2003/Real-time_search_1.htm)  
2. Introduction to Beam Search – GeeksforGeeks [Link](https://www.geeksforgeeks.org/introduction-to-beam-search-algorithm/)  
3. Heuristics for Sokoban – ScienceDirect [Link](https://www.sciencedirect.com/science/article/pii/S0004370215000867)  
4. Sokoban solver tips – StackOverflow [Link](https://stackoverflow.com/questions/4237462/sokoban-solver-tips)  
