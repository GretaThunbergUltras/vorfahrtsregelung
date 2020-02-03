#!/usr/bin/python3

from botlib.bot import Bot
from botlib.sonar import Sonar
from time import sleep

class Vorfahrt:
    APPROACH_POWER, DEFAULT_POWER = 30, 30
    RIGHT_MIN, RIGHT_MAX = 20, 40
    FRONT_MIN, FRONT_MAX = 0, 30
    COLLECT_TIMES = 5

    def __init__(self):
        self._bot = Bot()
        self._bot.calibrate()
        input('start?')

    def sensor_in_range(self, sensor, vmin, vmax):
        vals = [self._bot.sonar().read(sensor) for _ in range(self.COLLECT_TIMES)]
        no_err_vals = filter(lambda x: x != None, vals)
        median = sum(no_err_vals) / float(len(no_err_vals))
        print('sensor', sensor, vals, median)
        return vmin < median < vmax
    
    def is_right_free(self):
        return not self.sensor_in_range(Sonar.RIGHT45, self.RIGHT_MIN, self.RIGHT_MAX)
    
    def is_front_free(self, sensor):
        return not self.sensor_in_range(sensor, self.FRONT_MIN, self.FRONT_MAX)

    def wait_till_way_free(self):
        right45, right, left = False, False, False
        while not (right45 and right and left):
            print('weg nicht frei', right45, right, left)
            right45 = self.is_right_free()
            right = self.is_front_free(Sonar.RIGHT_FRONT)
            left = self.is_front_free(Sonar.LEFT_FRONT)
            sleep(0.1)

    def follow_line(self):
        from multiprocessing import Process

        linetracker = self._bot.linetracker()
        self._track_paused = False

        def follow():
            for improve in linetracker:
                if improve != None:
                    self._bot.drive_steer(improve)
                    # TODO: is this needed
                    sleep(0.1)
                while self._track_paused:
                    sleep(0.1)

        self._track_thread = Process(group=None, target=follow, daemon=True)
        self._track_thread.start()

    def wait_at_crossing(self):
        print('auto an kreuzung erkannt')
        
        self._track_paused = True
        self._bot.drive_power(0)
        self._bot.drive_steer(0)

        sleep(1)

        # Warten bis die Kreuzung frei ist
        self.wait_till_way_free()

        print('kreuzung frei')

    def run(self):
        # Ein neuer Thread kümmert sich darum, dass das Auto
        # der Linie folgt
        self.follow_line()

        # Solange wir keine Kreuzungslinie erkannt haben
        # fahren wir weiter
        self._bot.drive_power(self.DEFAULT_POWER)

        while True:
            # Haben wir ein Auto beim Fahren gesehen?
            if not self.is_right_free():
                self.wait_at_crossing()
                break

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

        sleep(5)

        self._bot.stop_all()

if __name__ == '__main__':
    Vorfahrt().run()
