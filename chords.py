"""Text chord diagrams for guitar lesson handouts."""
import functools

# Frets for each string, low E (string 6) to high E (string 1).
# 0 = open, -1 = muted, positive number = fret to press.
CHORDS = {
    "C": [0, 3, 2, 0, 1, 0],
    "G": [3, 2, 0, 0, 0, 3],
    "D": [-1, -1, 0, 2, 3, 2],
    "E": [0, 2, 2, 1, 0, 0],
    "Am": [-1, 0, 2, 2, 1, 0],
    "Em": [0, 2, 2, 0, 0, 0],
}


def fret_symbol(fret):
    """Turn one fret number into what the diagram shows."""
    if fret == -1:
        return "X"
    if fret == 0:
        return "O"
    return str(fret)


def titled(func):
    """Decorator: put the chord name and an underline above the diagram."""
    @functools.wraps(func)
    def wrapper(name):
        heading = "Chord: " + name
        return heading + "\n" + "-" * len(heading) + "\n" + func(name)
    return wrapper


@titled
def diagram(name):
    """Return the six diagram lines for a chord, string 6 first."""
    lines = []
    for index, fret in enumerate(CHORDS[name]):
        string_number = 6 - index
        lines.append(f"{string_number}: {fret_symbol(fret)}")
    return "\n".join(lines)


def main():
    name = input("Enter a chord name: ").strip()
    if name not in CHORDS:
        print("Chord not found.")
        return
    print(diagram(name))


if __name__ == "__main__":
    main()