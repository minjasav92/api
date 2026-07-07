from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
conn = sqlite3.connect("biblioteka.db", check_same_thread=False)
cursor = conn.cursor()
class Knjiga(BaseModel):
    naslov: str
    autor: str
    ocena: int
class AzurirajKnjigu(BaseModel):
    naslov: Optional[str] = None
    autor: Optional[str] = None
    ocena: Optional[int] = None
@app.get("/knjige")
def sve_knjige():
    cursor.execute("SELECT * FROM knjige")
    redovi = cursor.fetchall()
    rezultat = {}
    for red in redovi:
        rezultat[red[0]] = {
            "naslov": red[1],
            "autor": red[2],
            "ocena": red[3]
        }
    return rezultat
@app.get("/knjiga/{knjiga_id}")
def jedna_knjiga(knjiga_id: int):
    cursor.execute(
        "SELECT * FROM knjige WHERE id=?",
        (knjiga_id,)
    )
    red = cursor.fetchone()
    if red is None:
        raise HTTPException(status_code=404, detail="Knjiga ne postoji")
    return {
        "id": red[0],
        "naslov": red[1],
        "autor": red[2],
        "ocena": red[3]
    }
@app.post("/dodaj-knjigu")
def dodaj_knjigu(knjiga: Knjiga):
    if not 1 <= knjiga.ocena <= 5:
        raise HTTPException(status_code=400, detail="Ocena mora biti između 1 i 5")
    cursor.execute("""INSERT INTO knjige(naslov,autor,ocena)VALUES(?,?,?)""",(knjiga.naslov, knjiga.autor, knjiga.ocena))
    conn.commit()
    return {"Poruka": "Dodata"} 
@app.put("/oceni/{knjiga_id}")
def ocijeni(knjiga_id: int, knjiga: AzurirajKnjigu):
    cursor.execute(
        "SELECT * FROM knjige WHERE id=?",
        (knjiga_id,)
    )
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Knjiga ne postoji")
    if knjiga.naslov is not None:
        cursor.execute(
            "UPDATE knjige SET naslov=? WHERE id=?",
            (knjiga.naslov, knjiga_id)
        )
    if knjiga.autor is not None:
        cursor.execute(
            "UPDATE knjige SET autor=? WHERE id=?",
            (knjiga.autor, knjiga_id)
        )
    if knjiga.ocena is not None:

        if not 1 <= knjiga.ocena <= 5:
            raise HTTPException(status_code=400, detail="Ocena mora biti između 1 i 5")
        cursor.execute(
            "UPDATE knjige SET ocena=? WHERE id=?",
            (knjiga.ocena, knjiga_id)
        )
    conn.commit()
    return {"Poruka": "Ažurirano"}
@app.delete("/obrisi/{knjiga_id}")
def obrisi(knjiga_id: int):
    cursor.execute(
        "SELECT * FROM knjige WHERE id=?",
        (knjiga_id,)
    )
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Knjiga ne postoji")
    cursor.execute("DELETE FROM knjige WHERE id=?",(knjiga_id,) )
    conn.commit()
    return {"Poruka": "Obrisano"}