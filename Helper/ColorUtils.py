import random
from pyfiglet import Figlet
from colorama import Fore, Style

class ColorUtils:
    @staticmethod
    def _display_logo() -> None:
        """Displays the logo in the console with a pink gradient."""
        figlet = Figlet("Elite", width=200)
        logo = figlet.renderText("Nexus SelfBot")
        
        start_rgb = (255, 182, 193)  
        end_rgb = (255, 105, 180)   
        
        steps = len(logo.replace(" ", "").replace("\n", ""))  
        if steps == 0:
            return  
        
        def rgb_to_ansi(r1, g1, b1):
            """Converts RGB to ANSI escape code."""
            return f'\033[38;2;{r1};{g1};{b1}m'

        def interpolate(start, end, fac):
            """Interpolates between two points."""
            return round(start + (end - start) * fac)

        index = 0
        for line in logo.splitlines():
            colored_line = ""
            for char in line:
                if char != " ":
                    factor = index / steps
                    r = interpolate(start_rgb[0], end_rgb[0], factor)
                    g = interpolate(start_rgb[1], end_rgb[1], factor)
                    b = interpolate(start_rgb[2], end_rgb[2], factor)
                    colored_line += rgb_to_ansi(r, g, b) + char
                    index += 1
                else:
                    colored_line += char
            print(colored_line)
        print(Style.RESET_ALL)