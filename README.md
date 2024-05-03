Service design to help clients, using RESTful api , and JSON as response

Bokhanteringssystem.
Bokhanteringssystem är ett enkelt system som tillåter användare att lista, lägga till, ta bort och söka efter böcker. Systemet erbjuder också integration med Open Library API för att hämta ytterligare information om böcker.

Komma igång...
För att komma igång med projektet behöver du följa stegen nedan:

\_\_Klona GitHub-repot: Klona projektets GitHub-repository till din lokala maskin med följande kommando:

git clone <https://github.com/BedoKharboutli/API-RESTful.git>

\_\_Installera dependencies: Navigera till projektets rotkatalog och installera de nödvändiga paketen med följande kommando:

pip install -r requirements.txt

\_\_Starta projektet: Starta projektet genom att köra huvudskriptet med följande kommando:

"python main.py"

---

API-dokumentation...
API-dokumentationen för projektet finns nedan:

GET /api/docs hämtar själva api dokumentationen som json-fil
GET /books: Hämtar en lista över alla tillgängliga böcker i systemet.
POST /books: Lägger till en ny bok i systemet. Förväntar sig JSON-data med fält för "name" och "author".
GET /book/<id>: Hämtar information om en specifik bok baserat på dess ID.
DELETE /book/<id>: Tar bort en specifik bok från systemet baserat på dess ID.
GET /books/<name>: Söker efter böcker från Open Library API baserat på boknamn. Returnerar detaljerad information om matchande böcker.
För att använda API:et, använd en lämplig HTTP-klient (t.ex. Postman) för att göra förfrågningar till de angivna endpoints.

---

Teknologi...
Projektet är byggt med följande teknologier:

Flask: Framework för att skapa server med Python.
SQLAlchemy: för databashantering.
Flask-RESTful: för att enkelt skapa RESTful API:er.
