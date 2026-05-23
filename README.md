# Blackjack Simulator & RL Environment

Acest proiect este o platformă completă de simulare pentru jocul de Blackjack, dezvoltată în Python, utilizând o arhitectură stratificată. Proiectul servește atât ca un joc interactiv (Web / Console), cât și ca un mediu de testare pentru algoritmi de Reinforcement Learning și analize statistice ale strategiilor de tip Card Counting.

## 🏛️ Arhitectura Sistemului
Aplicația respectă cu strictețe principiile ingineriei software, fiind structurată pe trei niveluri arhitecturale izolate, modelate și rafinate complet în diagrame de structură și interacțiune UML:

* **Presentation Layer:** 
    * *Web:* Interfață Web receptivă realizată cu Flask, HTML5, CSS3 și JavaScript modern (AJAX prin API-uri REST/JSON).
    * *Console (CLI):* `GameMenu` pentru gestionarea stărilor text și a meniurilor de control inițiale.
* **Business Logic / Domain Layer:** Motor de joc complex (`BlackJackGame`) care funcționează ca un Mediator/Controller pentru entitățile de domeniu (`Player`, `Dealer`, `Hand`, `Shoe`, `Card`) și gestionează regulile stricte de cazinou. Comunicarea cu datele se face prin intermediul `PlayerService`.
* **Data Access Layer (ORM):** Strat de persistență izolat prin `PlayerRepository`, care mapează obiectele de domeniu pe tabelele SQL prin intermediul SQLAlchemy (ORM) și o bază de date SQLite.


## 🗺️ Modelare și Proiectare UML 
Evoluția sistemului și interacțiunile dintre straturi au fost documentate complet prin intermediul diagramelor UML standardizate (localizate în `/documentation` în format StarUML `.mdj`):

### 1. Diagrama de Cazuri de Utilizare (Use Case Diagram)
Definește granițele sistemului și interacțiunea Actorului (`User`) cu funcționalitățile software, structurate pe 3 Iterații majore de dezvoltare:
* **Iterația 1 (Gestiune & Autentificare):** UC 1 (Înregistrare), UC 2 (Autentificare/Login), UC 3 (Vizualizare Balanță), UC 4 (Salvare Profil).
* **Iterația 2 (Mecanici de Bază):** UC 5 (Distribuire inițială cărți / Deal), UC 6 (Acțiune "Hit"), UC 7 (Acțiune "Stand").
* **Iterația 3 (Logică Avansată):** UC 8 (Acțiune "Double Down"), UC 9 (Acțiune "Split"), UC 10 (Determinare Rezultat și Plată).

### 2. Diagrama de Clase Rafinată (Design Class Diagram)
Trecerea de la modelul conceptual la cel de proiectare software. Clasele sunt organizate structural în pachete (Packages) corespunzătoare straturilor arhitecturale:
* Evidențiază relațiile de **Compoziție** puternică.
* Definește relațiile de **Asociere** și **Dependență** dintre straturi.

### 3. Diagramele de Interacțiune (Sequence Diagrams)
Fiecare scenariu din cele 10 cazuri de utilizare dispune de o diagramă de secvență dedicată, ce ilustrează trecerea mesajelor în timp real între straturile sistemului:
* **Autentificare:** Fluxul complet de verificare a parolei prin Service și Repository.
* **Mecanica Rundei:** Ciclul de extragere a cărților din `Shoe` și delegarea lor către obiectele `Hand` corespunzătoare pentru actualizarea scorurilor, urmat de bucla automată (`loop`) a Dealer-ului.
* **Strategii Avansate:** Modificarea structurală a datelor la execuția `Split` (instanțierea unei noi mâini, divizarea cărților și preluarea mizei din balanță) și dublarea mizelor la `Double Down`.


## 📌 Funcționalități Implementate (MVP & Core Mechanics)
Aplicația oferă un flux complet și robust de joc, acoperind toate scenariile standard și avansate de Blackjack reflectate în modelele UML:

* **Sistem de Autentificare Securizat (UC 1-2):** Mecanism de login și înregistrare gestionat de `PlayerService`, utilizând hashing criptografic (prin `werkzeug.security`) pentru parole.
* **Gestiune Balanță & Persistență (UC 3-4):** Sincronizare automată și sigură a soldului jucătorului în baza de date la finalul fiecărei runde sau la părăsirea jocului, prevenind pierderile de progres.
* **Shoe Management (UC 5):** Suport pentru pachete multiple cu reamestecare automată declanșată matematic la atingerea indicatorului "Cut Card".
* **Advanced Hand & Split Logic (UC 6, 8, 9):**
    * Gestionare dinamică a valorii Asului (calcul în timp real între *Soft* și *Hard* hand pentru prevenirea bust-ului prematur).
    * *Double Down:* Dublarea mizei curente cu retragere de fonduri și oferirea unei singure cărți suplimentare.
    * *Split:* Împărțirea unei mâini cu perechi identice în două mâini complet independente, gestionate nativ cu propriile mize și fluxuri de joc separate.
* **Dealer Automation (UC 7):** Inteligență artificială deterministă pentru dealer (Dealer stands on all 17s - trage obligatoriu sub 17, se oprește la $\ge$ 17).
* **Evaluare și Plăți (UC 10):** Calcul automat al rezultatelor rundei (Win, Loss, Push) și aplicarea ratelor de plată specifice (ex: 3:2 pentru Blackjack natural).


## 🧪 Asigurarea Calității & Unit Testing
Pentru verificarea corectitudinii matematice și a fluxurilor arhitecturale, proiectul include o suită completă de teste unitare automate localizate în directorul `/tests`, implementate cu framework-ul standard `unittest`.

* **Testare Deterministică prin Mocking:** Utilizarea `unittest.mock.MagicMock` pentru simularea stării pachetului (`Shoe`), permițând injectarea de cărți controlate pentru a testa scenarii complexe (ex: simulare de Split valid, forțarea comportamentului de Stand al dealerului sau ajustarea valorii Asului).
* **Aria de acoperire a testelor:**
    * `test_hand.py`: Validarea calculului corect al scorurilor și algoritmului adaptiv pentru Ași (1 sau 11).
    * `test_shoe.py`: Verificarea corectitudinii dimensionale a pachetului și a declanșării mecanismului de reamestecare.
    * `test_player.py`: Testarea tranzacțiilor financiare (pariuri invalide, fonduri insuficiente) și fragmentarea mâinilor la split.
    * `test_game_mechanics.py`: Testarea completă a interacțiunilor complexe din motorul de joc (Double Down, tura dealerului, distribuirea inițială și acordarea plăților).

Rularea testelor din radacină:
```bash
python -m unittest discover tests
```

## 🚀 Roadmap & Future Features
* **Expert System:** Integrarea sistemului Hi-Lo de numărare a cărților (inclusiv abaterile Illustrious 18) pentru asistarea deciziilor jucătorului în timp real.
* **AI Training Platform:** Dezvoltarea și integrarea agenților de învățare prin consolidare (Reinforcement Learning) folosind algoritmi **Q-Learning** și **QV-Learning** pe stările motorului de joc.
* **Monte Carlo Simulations:** Generarea curbelor de învățare, a matricilor de decizie optimă și a datelor statistice de validare prin simulări masive multi-threaded.

## 🛠️ Tehnologii Utilizate
* **Backend Framework & Core:** Python 3.x, Flask (arhitectură REST API pentru comunicarea asincronă cu interfața web).
* **Frontend Layer:** JavaScript (ES6+ / Fetch API / Vanilla JSON), Jinja2 templates, HTML5, CSS3.
* **Database & ORM:** SQLAlchemy (Object-Relational Mapping), SQLite3 (bază de date locală relațională).
* **Testing Suite:** Framework-ul standard `unittest` din Python, integrat cu module de Mocking (`unittest.mock.MagicMock`).
* **Instrumente de Proiectare:** UML 2.5 (StarUML pentru modelarea diagramelor de Pachete, Diagramei de Clase Rafinate și Diagramelor de Secvență pentru Use Cases 1-10).

***Proiect de licență dezvoltat de Acul Mathyas.***