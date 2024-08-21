import os
import random
from typing import Optional
import logging

from discord.ext import commands

import asyncio
import requests
from colorama import Fore, Style

from Helper.ColorUtils import ColorUtils

class CustomFormatter(logging.Formatter):
    """Custom log formatter to add color and symbols to log messages."""

    def format(self, record):
        level_colors = {
            logging.DEBUG: (Style.BRIGHT + Fore.LIGHTMAGENTA_EX, "?"),
            logging.INFO: (Style.BRIGHT + Fore.LIGHTMAGENTA_EX, "+"),
            logging.WARNING: (Style.BRIGHT + Fore.LIGHTMAGENTA_EX, "?"),
            logging.ERROR: (Style.BRIGHT + Fore.RED, "-"),
            logging.CRITICAL: (Style.BRIGHT + Fore.RED, "-"),
        }

        color, symbol = level_colors.get(record.levelno, (Fore.RESET, "?"))

        formatted_message = f"[{color}{symbol}{Fore.RESET}] {record.getMessage()}"
        return formatted_message


class NexusSelfbot(commands.Bot):
    def __init__(self, prefix: str = ">", token_file_path: str = "./assets/token.env"):
        """Initializes the Nexus-selfbot class."""
        super().__init__(command_prefix=prefix, self_bot=True)
        self.token_file_path: str = token_file_path
        self.token: Optional[str] = None
        self.saved_token: Optional[str] = None
        self.logger = self._load_logging()

        self.remove_command("help")

        @self.event
        async def on_ready():
            """Event handler for when the bot is ready."""
            await self._load_cogs()
            self.logger.info(f"Logged in as {Style.BRIGHT + Fore.LIGHTMAGENTA_EX}{self.user}{Fore.RESET}")
            self.logger.debug(f"Prefix: {Style.BRIGHT + Fore.LIGHTMAGENTA_EX}{self.command_prefix}{Fore.RESET}")


    def run(self, reconnect: bool = True) -> None:
        """Runs the bot."""
        super().run(
            token=self.token, reconnect=reconnect, log_formatter=CustomFormatter()
        )

    @staticmethod
    def _load_logging() -> None:
        """Sets up the logging configuration."""
        logger = logging.getLogger("Nexus-selfbot")
        if not logger.handlers:  
            handler = logging.StreamHandler()
            handler.setFormatter(CustomFormatter())
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        return logger
        
    def _return_token(self) -> str:
        """Returns the token."""
        return self.token

    @staticmethod
    def _clear_console() -> None:
        """Clears the console."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def _set_console_title(title: str = "Nexus selfbot") -> None:
        """Sets the console title."""
        os.system(
            "title " + title if os.name == "nt" else f'echo -ne "\\033]0;{title}\\007"'
        )

    def _load_token(self) -> str:
        """Loads or requests a token from the user."""
        if os.path.exists(self.token_file_path):
            with open(self.token_file_path, "r") as file:
                saved_token = file.read().strip()

            use_saved_token = (
                input(f"[{Style.BRIGHT + Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Use saved token? (y/n): ")
                .strip()
                .lower()
            )
            if use_saved_token == "y":
                return saved_token

        return input(f"[{Style.BRIGHT + Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Enter your token: ").strip()

    @staticmethod
    def _validate_token(token: str) -> bool:
        """Validates the provided Discord token."""
        response = requests.get(
            "https://discord.com/api/v9/users/@me", headers={"Authorization": token}
        )
        if response.ok: return True

    def _save_token(self, token: str) -> None:
        """Saves the token to a file."""
        with open(self.token_file_path, "w") as file:
            file.write(token)
        print(f"[{Style.BRIGHT + Fore.LIGHTMAGENTA_EX}+{Fore.RESET}] Token saved.")

    async def _load_cogs(self) -> None:
        """Loads all cogs from the 'cogs' directory."""
        for filename in os.listdir("./cogs"):
            if (
                filename.endswith(".py")
                and not filename.startswith("__")
                and not filename.endswith(".pyc")
            ):
                cog = filename[:-3]
                try:
                    await self.load_extension(f"cogs.{cog}")
                    print(f"[{Style.BRIGHT + Fore.LIGHTMAGENTA_EX}+{Fore.RESET}] {Fore.RESET}Loaded {Style.BRIGHT + Fore.GREEN + cog + Fore.RESET}.")
                except commands.ExtensionAlreadyLoaded:
                    pass
                except Exception as e:
                    print(f"[{Fore.RED}-{Fore.RESET}] Failed to load {cog}: {e}")
                await asyncio.sleep(0.2)

    def main(self) -> None:
        """Main method to run the bot."""
        self._clear_console()
        self._set_console_title()
        ColorUtils._display_logo()

        self.token = self._load_token()

        if not self._validate_token(self.token):
            print(f"[{Fore.RED}-{Fore.RESET}] Token is {Style.BRIGHT + Fore.RED}Invalid.{Fore.RESET}")
            return

        print(f"[{Style.BRIGHT + Fore.LIGHTMAGENTA_EX}+{Fore.RESET}] Token is {Style.BRIGHT + Fore.GREEN}Valid.{Fore.RESET}")

        if os.path.exists(self.token_file_path):
            with open(self.token_file_path, "r") as file:
                self.saved_token = file.read().strip()

        if self.token != self.saved_token:
            remember_token = (
                input(f"[{Style.BRIGHT + Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Remember token? (y/n): ")
                .strip()
                .lower()
            )
            if remember_token == "y":
                self._save_token(self.token)

        print(f"[{Fore.YELLOW}/{Fore.RESET}] Starting bot..", end="\r")
        self.run()


if __name__ == "__main__":
    pack_bot = NexusSelfbot()
    pack_bot.main()
