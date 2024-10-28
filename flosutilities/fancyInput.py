import getkey
import sys
import flosutilities.simpleMath as simpleMath


def inputYesNo(displayText, defaultValue = False) -> bool:
    """Fragt eine YES / NO Frage ab, bei der die Antwortmöglichkeit mit Pfeiltasten ausgewählt werden kann

    Args:
        displayText (int): Der vor den Optionen angezeigte Text
        defaultValue (bool, optional): Der vorausgewählte Wert. Defaults to False.

    Returns:
        bool: Die Auswahl
    """
    return bool(inputFromSelection(displayText, [("NO", "no"), ("YES", "yes")], defaultValue))
    
        
        
def inputFromSelection(displayText, options, defaultValue = 0, showBoxes = True) -> int:
    """Zeigt mehrere Optionen aus, die mit den Pfeiltasten ausgewählt und mit Enter bestätigt werden können.

    Args:
        displayText (str): Der Text, der vor den Optionen angezeigt wird (es wird ein Leerzeichen angehängt)
        options (list[(str, str), (str, str)]): Liste der Optionen [(selektiert, nicht selektiert), (selektiert, nicht selektiert), ...]
        defaultValue (int, optional): Die Standardmäßig ausgewählte Option Defaults to 0.
        showBoxes(bool): Stellt ein, ob die Boxen der Auswhl hinzugefügt werden sollen
        
    Returns:
        int: Die ausgwählte Option
    """
    lenOptions = len(options)
    currentValue = defaultValue
    while True:
        outText = displayText + " "
        for x in range(lenOptions):
            if x > 0:
                outText += " / "
            if x == currentValue:
                if showBoxes:
                    outText += "▮ "
                outText += options[x][0]
            else:
                if showBoxes:
                    outText += "▯ "
                outText += options[x][1]
                
        print(outText)
        
        while True:
            key = getkey.getkey()
            if key == getkey.keys.LEFT:
                currentValue += -1
                break
            elif key == getkey.keys.RIGHT:
                currentValue += 1
                break
            elif key == getkey.keys.ENTER:
                return currentValue
        
        currentValue = simpleMath.clip(0, lenOptions-1, currentValue)
        sys.stdout.write("\033[F\033[K")