This is a short description of the project. It's current use case is to track D&D 3.5e characters, but with each component built to allow for some flexibility with other d20 systems (D&D 5e, Pathfinder, etc). Flexibility is desired, but not the main focus of this build. Refactoring will be required should there ever be a drive to expand to other systems.

This project is based in Python 3.7. Dependencies are currently none.

Short term goals are, in order of completion:

1. Making the character tracker accurately track all information needed in a session. 
  * Items: Weapons, Armour, etc
  * Class basics: BAB, Saves, etc
  * Class extras: Spells, Bardic Song, etc
1. Include a GUI to actually be able to use it in a session.
  * Qt/Tk wrapper for Android phones
  * PyGame/Qt/Tk wrapper for Linux laptops.
  * No current plans for iOS or Windows.


Long terms goals include, but aren't limited to:

1. Add a sharing function / party tracker. Effectively expand to multi character support.
1. Add support for NPC tracking
1. Integrate with a project like PyMap and get multitouch table support. (dream big, amirite?)
