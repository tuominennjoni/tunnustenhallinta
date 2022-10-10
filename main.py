import tkinter as Tk
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# generaattori
def salasananGenerointi():
    salasana_boksi.delete(0, END)
    kirjaimet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numerot = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symboolit = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # arvotaan kirjainten, symboolien ja numeroiden määrä - 8-10 kirjainta, 2,4 symboolia ja 2-4 numeroa
    salasana_kirjaimet = random.randint(8,10)
    salasana_symboolit = random.randint(2,4)
    salasana_numerot = random.randint(2,4)

    # salasanan määrittäminen
    salasana = [random.choice(kirjaimet) for i in range(salasana_kirjaimet)]
    salasana += [random.choice(symboolit) for i in range(salasana_symboolit)]
    salasana += [random.choice(numerot) for i in range(salasana_numerot)]
    
    random.shuffle(salasana) # shuffletaan kirjaimet, symbolit ja numerot keskenään
    salasana = ''.join(salasana)
    salasana_boksi.insert(0, salasana)
    pyperclip.copy(salasana) # kopioidaan salasana
            
def tallennetaanData(): # tallennetaan kirjautumistiedot json tiedostoon        
        #tallennetaan data mikä on syötetty
        verkkosivu = verkkosivu_boksi.get()
        kayttajanimi = kayttaja_boksi.get()
        salasana = salasana_boksi.get()
        uusiData = {
            verkkosivu:{
                'email': kayttajanimi,
                'salasana': salasana
            }
        }
        
        # tarkistetaan, että käyttäjä on syöttänyt tietoa jokaiseen tekstiboksiin
        if len(verkkosivu) == 0 or len(kayttajanimi) == 0 or len(salasana) == 0:       
            messagebox.showerror(title='Virhe', icon='warning', message='Täytä kaikki laatikot!') # jos käyttäjä ei ole syöttänyt tietojaan kaikkiin kohtiin, niin suoritetaan showerror funktio
                       
        else:
            #vahvistetaan tallennus käyttäjältä
            tiedot_OK = messagebox.askokcancel(title='Tallenna tiedot', message=f'Olet tallentamassa nämä tiedot:\nVerkkosivu: {verkkosivu}\nEmail: {kayttajanimi}\nSalasana: {salasana}\n\n\nHaluatko tallentaa nämä tiedot?' )
            if tiedot_OK: #tallennetaan käyttäjän lisäämä data json tiedostoon
                try:
                    with open('tunnukset.json', mode='r') as tunnus: # avataan json tiedosto lukua varten
                        tiedot = json.load(tunnus)
                        
                except FileNotFoundError:
                    with open('tunnukset.json', mode='w') as tunnus: # avataan json tiedosto kirjoitusta varten
                        json.dump(uusiData, tunnus, indent=2) # dump funktiolla saadaan data json muotoon
                        
                else:
                    tiedot.update(uusiData) #päivitetään käyttäjänm lisäämä data                                  
                    with open('tunnukset.json', mode='w') as tunnus: #tallennetaan data json tiedostoon
                        json.dump(tiedot, tunnus, indent=2) # json muotoon
                
                finally: # tyhjennetään boksit                   
                    verkkosivu_boksi.delete(0,END)
                    salasana_boksi.delete(0, END)
                    kayttaja_boksi.delete(0, END)
                                       
def salisGenNro():
     salasana_boksi.delete(0, END) # tyhjenettään boksi aina kun ollaan generoitu salis
     numerot = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # numerot
    
     salasana_numerot = [random.choice(numerot) for _ in range(random.randint(8, 12))] # randomilla 8-12 pitkä salasana numeroilla
     random.shuffle(salasana_numerot) # shuffletaan
     salasana = ''.join(salasana_numerot)
     salasana_boksi.insert(0, salasana) # insertataan salistekstiboksiin
     pyperclip.copy(salasana) # kopioidaan
                          
def etsiSalasana():
    verkkosivu = verkkosivu_boksi.get()
    
    if len(verkkosivu) == 0:
        messagebox.showwarning(title="Tietoja puuttuu", message="Syötä verkkosivu, jonka tiedot haluat katsoa")  
    try:
        with open("tunnukset.json", mode="r") as salis:
            data = json.load(salis)
    except FileNotFoundError: # tämä ei toimi
        messagebox.showerror(title="Virhe", message="Verkkosivulle ei ole lisätty tunnuksia")
    else:
        if verkkosivu in data:
            etsidata = data[verkkosivu]
            etsiknimi = etsidata['email']
            etsisalis = etsidata['salasana']
            kopioidaan = messagebox.askokcancel(title=verkkosivu, message=f"Sähköposti/käyttäjänimi: {etsiknimi}\nSalasana: {etsisalis}"
                                                                             f"\n\nKopioidaanko salasana?")
            if kopioidaan:
            #print(salis)
                pyperclip.copy(etsisalis) # kopioidaan salis
                messagebox.showinfo(title="Onnistui", message="Salasana on kopioitu!")
            
            
# TKINTER                  
gui = Tk()
gui.iconbitmap(r'C:\ValOhjSovellus\lukkoicon.ico') # iconi, täytyy hakea polulla kun halusi exen tehdä. Tuli erroria muuten.
gui.geometry("740x450") # ikkunan koko
gui.title("Tunnusten ja salasanojen hallinta") # otsikko
gui['background']='black' # tausta

LOGO = PhotoImage(file="C:\ValOhjSovellus\logo.png") # määritellään logon mitat yms ja sama homma piti hakea polulla tai muuten error exee tehdessä
canvas = Canvas(width=155, height=130, highlightthickness=0)
canvas.config()
canvas.create_image(80, 60, image=LOGO)
canvas.grid(column=1, row=0, pady=30)

FONTTI1 = ("Vertana", 10, "bold") # fontit
FONTTI2 = ("Vertana", 15, "bold")

# labelit
verkkosivu_teksti = Label(text='Verkkosivu', font=FONTTI2, background='black', foreground='white') # labeleitten määrittelyt = teksti, fontti, taustaväri ja tekstin väri
verkkosivu_teksti.grid(row=1, column=0, padx=30) # rivi, kolumni ja väli tekstibokseihin

kayttaja_teksti = Label(text= 'Sähköposti/Käyttäjänimi', font=FONTTI2, background='black', foreground='white')
kayttaja_teksti.grid(row=2, column=0, padx=30)

salasana_teksti = Label(text='Salasana', font=FONTTI2, background='black', foreground='white')
salasana_teksti.grid(row=3, column=0, padx=30)

# tekstiboksit
verkkosivu_boksi = Entry(width=25) # tekstiboksin leveys 25 kaikissa
verkkosivu_boksi.focus() # default paikka tekstin kirjoittamiseen
verkkosivu_boksi.grid(column=1, row=1, padx=30) # kolumni, rivi ja väli buttoneihin = padx 

kayttaja_boksi = Entry(width=25)
kayttaja_boksi.grid(column=1, row=2, padx=30)

salasana_boksi = Entry(width=25)
salasana_boksi.grid(column=1, row=3, padx=30)

# napit
salasanaNappi = Button(width=18, command=salasananGenerointi) # napin painallus suorittaa salasanaGenerointi funktion
salasanaNappi.config(text='Generoi salasana', font=FONTTI1, background='gray', foreground='white') # teksti, fontti, tausta ja tekstin väri
salasanaNappi.grid(column=3, row=3, pady=3) # kolumni, rivi ja väli alla olevaan = pady

etsiNappi = Button(width=18, command=salisGenNro) # napin painallus suorittaa salasanan generoinnin pelkillä numeroilla - funktion
etsiNappi.config(text='Generoi numeroilla', font=FONTTI1, background='gray', foreground='white') 
etsiNappi.grid(column=3, row=4, pady=3) 

lisaaNappi = Button(width=18, command=tallennetaanData) # napin painallus suorittaa tallennetaanData funktion
lisaaNappi.config(text='Lisää', font=FONTTI1, background='gray', foreground='white') 
lisaaNappi.grid(column=3, row=1, pady=3) 

etsiNappi = Button(width=18, command=etsiSalasana) # napin painallus suorittaa etsiSalasana funktion
etsiNappi.config(text='Etsi salasana', font=FONTTI1, background='gray', foreground='white') 
etsiNappi.grid(column=3, row=2) # kolumni ja rivi

gui.mainloop()