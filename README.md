# Blackjack Simulator & RL Environment

Acest proiect este o platformă completă de simulare pentru jocul de Blackjack, dezvoltată în Python, utilizând o arhitectură stratificată. Proiectul servește atât ca un joc interactiv, cât și ca un mediu de testare pentru algoritmi de Reinforcement Learning și analize statistice ale strategiilor de tip Card Counting.

## 🏛️ Arhitectura Sistemului
Aplicația respectă principiile ingineriei software, fiind structurată pe trei niveluri:
* **Presentation Layer:** Interfață Web realizată cu Flask, HTML5, CSS3 și JavaScript (AJAX).
* **Business Logic Layer:** Motor de joc complex (Game Engine) care gestionează regulile de cazinou, scorurile și stările jocului.
* **Data Access Layer (ORM):** Persistența datelor (utilizatori, balanțe) realizată prin SQLAlchemy și SQLite.

## 📌 Funcționalități Implementate (MVP)
În prezent, aplicația oferă un flux complet de joc cu următoarele caracteristici:
* **Sistem de Autentificare:** Login securizat cu hashing pentru parole.
* **Gestiune Balanță:** Salvarea automată a soldului în baza de date după fiecare rundă.
* **Shoe Management:** Suport pentru pachete multiple (ex: 6 pachete) cu reamestecare bazată pe "Cut Card".
* **Hand Logic:** Gestionare dinamică a Asului (Soft/Hard hands), Split și Double Down.
* **Dealer Logic:** Automatizare completă (Dealer stands on all 17s).

## 🚀 Roadmap & Future Features
* **Expert System:** Integrarea sistemului Hi-Lo de numărare a cărților (inclusiv abaterile Illustrious 18).
* **AI Training:** Dezvoltarea agenților de învățare prin consolidare folosind algoritmi **Q-Learning** și **QV-Learning**.
* **Monte Carlo Simulations:** Generarea curbelor de învățare și a datelor statistice prin simulări multi-threaded.

## 🛠️ Tehnologii Utilizate
* **Backend:** Python 3.x, Flask
* **Frontend:** JavaScript (ES6+), Jinja2
* **Database:** SQLAlchemy (ORM), SQLite
* **Metodologie:** Arhitectură stratificată, Design Patterns.

---
*Proiect de licență / Laborator Ingineria Programului dezvoltat de **Acul Mathyas**.*
