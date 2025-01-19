import random
import math
import datetime
import sys

import haravasto



#Globaalit muuttujat
tila = {
    "kentta":[]
}

MIINAT_LIPUTETTU = 0
TYHJAT_LIPUTETTU = 0

#Funktiot
def kasittele_hiiri(x_koord, y_koord, painike, muokkausnappaimet):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin.
    """
    painikkeet = {
        haravasto.HIIRI_VASEN:"vasen",
        haravasto.HIIRI_KESKI:"keski",
        haravasto.HIIRI_OIKEA:"oikea"
    }

    #Muuttaa isot koordinaatit ruutu muotoon
    ruutu_x = math.floor(x_koord/40)
    ruutu_y = math.floor(y_koord/40)

    #VASEN NAPPI TOIMINNOT
    if painikkeet[painike] == "vasen":
        if kentta[ruutu_y][ruutu_x] == " ":
            tulvataytto(kentta, ruutu_x, ruutu_y)
        elif kentta[ruutu_y][ruutu_x] in range(1, 9):
            tulvataytto(kentta, ruutu_x, ruutu_y)
            kentta[ruutu_y][ruutu_x] = str(kentta[ruutu_y][ruutu_x])

     
    #OIKEA NAPPI TOIMINNOT
    global TYHJAT_LIPUTETTU
    if painikkeet[painike] == "oikea":
        if kentta[ruutu_y][ruutu_x] == " " or kentta[ruutu_y][ruutu_x] in range (1, 9):
            TYHJAT_LIPUTETTU += 1
            kentta[ruutu_y][ruutu_x] = "f"
        elif kentta[ruutu_y][ruutu_x] == "f":
            TYHJAT_LIPUTETTU -= 1
            kentta[ruutu_y][ruutu_x] = " "
    
    global MIINAT_LIPUTETTU
    if painikkeet[painike] == "oikea":
        if kentta[ruutu_y][ruutu_x] == "x":
            kentta[ruutu_y][ruutu_x] = "f"
            MIINAT_LIPUTETTU = MIINAT_LIPUTETTU + 1
 


    #Peli ohi logiikka
    if painikkeet[painike] == "vasen" and kentta[ruutu_y][ruutu_x] == "x":
        havio()
    
    #Peli voitto logiikka
    if MIINAT_LIPUTETTU == miinojen_maara and TYHJAT_LIPUTETTU == 0:
        voitto()
   
def voitto():
    """"
    LATAA TILASTOT TEKSTITIEDOSTOON VOITON
    """
    print("VOITIT")
    aika = datetime.datetime.now()
    with open("tilastot.txt", "a") as file_to_write:
        file_to_write.write(f"\nVOITTO, PVÄ MÄÄRÄ {aika}, KORKEUS: {korkeus}, "
                            f"LEVEYS: {leveys}, MIINOJEN LUKUMÄÄRÄ: {miinojen_maara}")
    haravasto.lopeta()

def havio():
    """"
    LATAA TILASTOT TEKSTITIEDOSTOON HÄVIÖN
    """
    print("HÄVISIT")
    aika = datetime.datetime.now()
    with open("tilastot.txt", "a") as file_to_write:
        file_to_write.write(f"\nHÄVIÖ, PVÄ MÄÄRÄ {aika}, KORKEUS: {korkeus}, "
                            f"LEVEYS: {leveys}, MIINOJEN LUKUMÄÄRÄ: {miinojen_maara}")
    haravasto.lopeta()

def tulvataytto(kentta, aloitus_x, aloitus_y):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    koordinaattiparilista = [(aloitus_y, aloitus_x)]
    if kentta[aloitus_y][aloitus_x] == "x":
        pass
    else:
        while koordinaattiparilista:

            koordinaatit_y, koordinaatit_x = koordinaattiparilista.pop()

            kentta[koordinaatit_y][koordinaatit_x] = "0"

            for i in range(max(0, koordinaatit_y-1), min(len(kentta), koordinaatit_y+2)):
                for j in range(max(0, koordinaatit_x-1), min(len(kentta[0]), koordinaatit_x+2)):
                    if kentta[i][j] == " ":
                        koordinaattiparilista.append((i, j))
                    elif kentta[i][j] in range(1, 9):
                        kentta[i][j] = str(kentta[i][j])

def miinoita_ja_numeroita(kentta, jaljella, miinojen_lkm):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin. Ja asettaa  miinojen ympärille numerot.
    """
    #miinojen paikkojen generointi
    miinojen_y_x = random.sample(jaljella, miinojen_lkm)
    for miinay_miinax in miinojen_y_x:
        miinan_y, miinan_x = miinay_miinax
        kentta[miinan_x][miinan_y] = "x"
    
        #numeroiden ympärille laitto
        for i in range(max(0, miinan_x-1), min(len(kentta), miinan_x+2)):
            for j in range(max(0, miinan_y-1), min(len(kentta[0]), miinan_y+2)):
                if kentta[i][j] == "x":
                    pass
                elif kentta[i][j] in range(1, 8):
                    kentta[i][j] += 1
                else:
                    kentta[i][j] = 1
        
def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.aloita_ruutujen_piirto()
    haravasto.piirra_tausta()
    for i, rivit in enumerate(kentta):
        for i_1, ruudut in enumerate(rivit):
            if kentta[i][i_1] == "x" or kentta[i][i_1] in range (1,8):
                haravasto.lisaa_piirrettava_ruutu(" ", 40*i_1, 40*i)           
            else:
                haravasto.lisaa_piirrettava_ruutu(ruudut, 40*i_1, 40*i)

    haravasto.piirra_ruudut()

def main(kentta, jaljella, miinojen_maara):
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(leveys * 40, korkeus * 40)
    miinoita_ja_numeroita(kentta, jaljella, miinojen_maara)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()

def katso_tilastot():
    """
    PRINTTAA TILASTOT TEKSTITIEDOSTON SISÄLLÖN
    """
    with open("tilastot.txt", "r") as lue:
        print(lue.read())

#Pääohjelma
if __name__ == "__main__":
    print("Pelatakasesi paina: P(eli)")
    print("Katsoaksesi tilastoja paina: T(ilastot)")
    print("Poistuaksesi paina: L(opeta)")
    valittu_peliosio = input("Valitse: ").lower().strip()
    if valittu_peliosio == "p":
        try:
            korkeus = int(input("ANNA KENTÄN KORKEUS: "))
            leveys = int(input("ANNA KENTÄN LEVEYS: "))
            miinojen_maara = int(input("ANNA MIINOJEN MÄÄRÄ: "))
        except ValueError:
            print("ANNAS VAAN NUMEROITA ILMAN VÄLILYÖNTEJÄ")

        #Luo kentän
        kentta = []
        for rivi in range(korkeus):
            kentta.append([])
            for sarake in range(leveys):
                kentta[-1].append(" ")

        tila["kentta"] = kentta

        jaljella = []
        for x in range(int(leveys)):
            for y in range(int(korkeus)):
                jaljella.append((x, y))
        
        main(kentta, jaljella, miinojen_maara)

    elif valittu_peliosio == "t":
        katso_tilastot()
    elif valittu_peliosio == "l":
        sys.exit()
    else:
        print("VALITTES UUSIKS")
