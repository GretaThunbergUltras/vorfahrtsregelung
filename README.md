# Vorfahrtsregelung

> Ein erster Schwarmroboter fährt geradeaus und ein zweiter Schwarmroboter nähert sich von links. Der von links kommende zweite Schwarmroboter registriert den ersten Schwarmroboter und gewährt Vorfahrt.

## Voraussetzungen

- Linien auf dem Boden halten das Auto in der Spur
- Eine Kreuzung hat an einer Einfahrt immer zwei Linien
    - Kreuzungslinie: Der Roboter drosselt seine Geschwindigkeit und hält Ausschau nach anderen Robotern.
    - Haltelinie: Der Roboter stoppt hier wenn er während des Anfahrens ein Auto von rechts erkannt hat.

![Kreuzungsdiagramm](docs/kreuzung.svg)

## Struktogramm

![Struktogramm](docs/struktogramm.png)

Tool: [Struktogrammeditor](http://whiledo.de/index.php?p=struktogrammeditor)

Run

``` powershell
java -jar struktogrammeditor*.jar
```
## Nützliche Links

Bildauswertungs Library:
- OpenCV: https://opencv.org/
- ImageAI: http://imageai.org
