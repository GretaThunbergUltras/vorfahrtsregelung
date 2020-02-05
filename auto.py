#!/usr/bin/python3

from botlib.bot import Bot
from botlib.sonar import Sonar
from time import sleep

class Vorfahrt:
    APPROACH_POWER, DEFAULT_POWER = 40, 40
    RIGHT_MIN, RIGHT_MAX = 10, 40
    FRONT_MIN, FRONT_MAX = 0, 30
    COLLECT_TIMES = 2

    def __init__(self):
        self._bot = Bot()
        self._bot.calibrate()

    def sensor_in_range(self, sensor, vmin, vmax):
        # Mehrere Werte des selben Sensors lesen um schlechte Werte auszugleichen.
        vals = [self._bot.sonar().read(sensor) for _ in range(self.COLLECT_TIMES)]

        # `None` repräsentiert einen Lesefehlschlag. Diese Werte müssen ausgenommen werden.
        no_err_vals = list(filter(lambda x: x != None, vals))

        # Durch 0 teilen führt zu fehler. Außerdem wurde kein valider Wert gelesen.
        if 0 == len(no_err_vals):
            return False

        median = sum(no_err_vals) / float(len(no_err_vals))

        print('sensor', sensor, vals, median)

        # Wenn der ermittelte Durschnitt in der Reichweiter ist -> return True
        return vmin < median < vmax
    
    def is_right_free(self):
        return not self.sensor_in_range(Sonar.RIGHT45, self.RIGHT_MIN, self.RIGHT_MAX)
    
    def is_front_free(self, sensor):
        return not self.sensor_in_range(sensor, self.FRONT_MIN, self.FRONT_MAX)

    def wait_till_way_free(self):
        right45, right, left = False, False, False
        # Führe diese Schleife aus, bis alle Sensoren 'frei' sind
        while not (right45 and right and left):
            print('weg nicht frei', right45, right, left)

            right45 = self.is_right_free()
            right = self.is_front_free(Sonar.RIGHT_FRONT)
            left = self.is_front_free(Sonar.LEFT_FRONT)

            sleep(0.1)

    def wait_at_crossing(self):
        print('auto an kreuzung erkannt')
        
        # Line tracking während des Haltens deaktivieren
        self._track_paused = True
        self._bot.drive_power(0)
        self._bot.drive_steer(0)

        sleep(1)

        # Warten bis die Kreuzung frei ist
        self.wait_till_way_free()
        
        # Line tracking fortsetzen
        self._track_paused = False
        print('kreuzung frei')

    def run(self):
        # Ein neuer Thread kümmert sich darum, dass das Auto
        # der Linie folgt
        # self.follow_line()
        self._bot.linetracker().autopilot(True)

        # Solange wir keine Kreuzungslinie erkannt haben
        # fahren wir weiter
        self._bot.drive_power(self.DEFAULT_POWER)

        try:
            while True:
                # Haben wir ein Auto beim Fahren gesehen?
                if not self.is_right_free():
                    self.wait_at_crossing()
                    self._bot.drive_power(self.DEFAULT_POWER)

            # Geschwindigkeit verringern
            # self._bot.drive_power(self.APPROACH_POWER)
            
            # Wurde ein Auto während des Annährens an 
            # die Kreuzung erkannt
            # car_detected = False

            # Haben wir ein Auto während des Annährens gesehen?
            # if car_detected:
                # Wenn Ja, anhalten

            # Weiterfahren
            self._bot.drive_power(self.DEFAULT_POWER)
            self._track_paused = False

            input('stop?')
        except KeyboardInterrupt:
            pass

        self._bot.stop_all()

if __name__ == '__main__':
    Vorfahrt().run()
