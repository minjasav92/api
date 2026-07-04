from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Knjiga(BaseModel):
    naslov: str
    autor: str
    ocena: int

class AzurirajKnjigu(BaseModel):
    naslov: Optional[str] = None
    autor: Optional[str] = None
    ocena: Optional[int] = None

knjige = {}
sledeci_id = 1

@app.get("/knjige")
def sve_knjige():
    return knjige

@app.get("/knjiga/{knjiga_id}")
def jedna_knjiga(knjiga_id: int):
    if knjiga_id not in knjige:
        return {"Error": "Knjiga ne postoji"}
    return knjige[knjiga_id]

@app.post("/dodaj-knjigu")
def dodaj_knjigu(knjiga: Knjiga):
    global sledeci_id
    if not 1 <= knjiga.ocena <= 5:
        return {"Error": "Ocena mora biti između 1 i 5"}
    knjige[sledeci_id] = knjiga
    sledeci_id += 1
    return knjige[sledeci_id - 1]

@app.put("/ocijeni/{knjiga_id}")
def ocijeni(knjiga_id: int, knjiga: AzurirajKnjigu):
    if knjiga_id not in knjige:
        return {"Error": "Knjiga ne postoji"}
    if knjiga.naslov is not None:
        knjige[knjiga_id].naslov = knjiga.naslov
    if knjiga.autor is not None:
        knjige[knjiga_id].autor = knjiga.autor
    if knjiga.ocena is not None:
        if not 1 <= knjiga.ocena <= 5:
            return {"Error": "Ocena mora biti između 1 i 5"}
        knjige[knjiga_id].ocena = knjiga.ocena
    return knjige[knjiga_id]

@app.delete("/obrisi/{knjiga_id}")
def obrisi(knjiga_id: int):
    if knjiga_id not in knjige:
        return {"Error": "Knjiga ne postoji"}
    obrisana = knjige[knjiga_id]
    del knjige[knjiga_id]
    return {"Obrisano": obrisana}