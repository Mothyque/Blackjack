# Blackjack Simulator & RL Environment

Acest proiect este o platformă completă de simulare pentru jocul de Blackjack, dezvoltată în Python, utilizând o arhitectură stratificată. Proiectul servește atât ca un joc interactiv (Web / Console), cât și ca un mediu de testare pentru algoritmi de Reinforcement Learning și analize statistice ale strategiilor de tip Card Counting.

## 🏛️ Arhitectura Sistemului
Aplicația respectă cu strictețe principiile ingineriei software, fiind structurată pe trei niveluri arhitecturale izolate, modelate și rafinate complet în diagrame de structură și interacțiune UML:

* **Presentation Layer:** 
    * *Web:* Interfață Web receptivă realizată cu Flask, HTML5, CSS3 și JavaScript modern (AJAX prin API-uri REST/JSON).
    * *Console (CLI):* `GameMenu` pentru gestionarea stărilor text și a meniurilor de control inițiale.
* **Business Logic / Domain Layer:** Motor de joc complex (`BlackJackGame`) care funcționează ca un Controller pentru entitățile de domeniu (`Player`, `Dealer`, `Hand`, `Shoe`, `Card`) și gestionează regulile stricte de cazinou. Comunicarea cu datele se face prin intermediul `PlayerService`.
* **Data Access Layer (ORM):** Strat de persistență izolat prin `PlayerRepository`, care mapează obiectele de domeniu pe tabelele SQL prin intermediul SQLAlchemy (ORM) și o bază de date SQLite.

---

## 📌 Funcționalități Implementate (MVP & Core Mechanics)
Aplicația oferă un flux complet și robust de joc, acoperind toate scenariile standard și avansate de Blackjack (Use Cases 1-10):

* **Sistem de Autentificare Securizat (UC 1-2):** Mecanism de login și înregistrare gestionat de `PlayerService`, utilizând hashing criptografic (prin `werkzeug.security`) pentru parole.
* **Gestiune Balanță & Persistență (UC 3-4):** Sincronizare automată și sigură a soldului jucătorului în baza de date la finalul fiecărei runde sau la părăsirea jocului, prevenind pierderile de progres.
* **Shoe Management (UC 5):** Suport pentru pachete multiple (6 pachete standard) cu reamestecare automată (reshuffle) declanșată matematic la atingerea indicatorului "Cut Card".
* **Advanced Hand & Split Logic (UC 6, 8, 9):** * Gestionare dinamică a valorii Asului (calcul în timp real între *Soft* și *Hard* hand pentru prevenirea bust-ului prematur).
    * *Double Down:* Dublarea mizei curente cu retragere de fonduri și oferirea unei singure cărți suplimentare.
    * *Split:* Împărțirea unei mâini cu perechi identice în două mâini complet independente, gestionate nativ cu propriile mize și fluxuri de joc separate.
* **Dealer Automation (UC 7):** Inteligență artificială deterministă pentru dealer (Dealer stands on all 17s - trage obligatoriu sub 17, se oprește la $\ge$ 17).
* **Evaluare și Plăți (UC 10):** Calcul automat al rezultatelor rundei (Win, Loss, Push) și aplicarea ratelor de plată specifice (ex: 3:2 pentru Blackjack natural).

---

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