def auto_erkannt(abstand_min, abstand_max):
    abstand = abstandssensor()
    return abstand_min < abstand < abstand_max

def auto_rechts():
    kamera.rechts()
    return auto_erkannt(0, 1)

def kreuzung_frei():
    kamera.mitte()
    return auto_erkannt(0, 1)

def main():
    # Solange wir keine Kreuzungslinie erkannt haben
    # fahren wir weiter
    while not kreuzungslinie.erkannt():
        folge()
    
    # Kreuzungslinie erkannt
    # Geschwindigkeit verringern
    speed.decrease()
    
    # Wurde ein Auto während des Annährens an 
    # die Kreuzung erkannt
    auto_an_kreuzung = False

    # Solange wir keine Stoplinie erkannt haben
    while not stoplinie.erkannt():
        # Weiterfahren
        folge()
        # Merken, wenn rechts ein Auto erkannt wurde
        if auto_rechts():
            auto_an_kreuzung = True
    
    # Stoplinie erkannt

    # Haben wir ein Auto während des Annährens gesehen?
    if auto_an_kreuzung:
        # Wenn Ja, anhalten
        stop()
        # Warten bis die Kreuzung frei ist
        while not kreuzung_frei():
            pass
        # Nochmal rechts gucken ob ein zweites Auto nachkommt
        while auto_rechts():
            # Wieder warten bis die Kreuzung frei ist
            kreuzung_frei()
    
    # Weiterfahren
    speed.increase()
    folge()
