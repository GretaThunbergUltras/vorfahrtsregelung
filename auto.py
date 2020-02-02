#!/usr/bin/python3

from botlib.bot import Bot
from botlib.sonar import Sonar
from time import sleep

class Vorfahrt:
    APPROACH_POWER, DEFAULT_POWER = 30, 50
    RIGHT_MIN, RIGHT_MAX = 50, 100
    FRONT_MIN, FRONT_MAX = 50, 100

    def __init__(self):
        self._bot = Bot()

    def sensor_in_range(self, sensor, vmin, vmax):
        return vmin < self._bot.sonar().read(sensor) < vmax
    
    def is_right_free(self):
        return self.sensor_in_range(Sonar.RIGHT45, self.RIGHT_MIN, self.RIGHT_MAX)
    
    def is_front_free(self):
        return self.sensor_in_range(Sonar.FRONT, self.FRONT_MIN, self.FRONT_MAX)

    def wait_till_front_free(self):
        while not self.is_front_free():
            sleep(0.1)

    def follow_line(self):
        from threading import Thread

        linetracker = self._bot.linetracker()

        def follow():
            for improve in linetracker:
                if improve:
                    self._bot.drive_steer(improve)
                    # TODO: is this needed
                    sleep(0.1)

        thread = Thread(group=None, target=follow, daemon=True)
        thread.start()

    def run(self):
        # Ein neuer Thread kümmert sich darum, dass das Auto
        # der Linie folgt
        self.follow_line()

        # Solange wir keine Kreuzungslinie erkannt haben
        # fahren wir weiter
        self._bot.drive_power(self.DEFAULT_POWER)
        
        # Kreuzungslinie erkannt
        # Geschwindigkeit verringern
        self._bot.drive_power(self.APPROACH_POWER)
        
        # Wurde ein Auto während des Annährens an 
        # die Kreuzung erkannt
        car_detected = False

        # Solange wir keine Stoplinie erkannt haben
        # Stoplinie erkannt

        # Haben wir ein Auto während des Annährens gesehen?
        if car_detected:
            # Wenn Ja, anhalten
            self._bot.drive_power(0)

            # Warten bis die Kreuzung frei ist
            self.wait_till_front_free()

            # Nochmal rechts gucken ob ein zweites Auto nachkommt
            while not self.is_right_free():
                # Wieder warten bis die Kreuzung frei ist
                self.wait_till_front_free()
        
        # Weiterfahren
        self._bot.drive_power(self.DEFAULT_POWER)

if __name__ == '__main__':
    Vorfahrt().run()
