from .player import SequencePlayer
from audio import AudioPlayer
from animatronic.base import Animatronic
from dispenser.base import Dispenser
from activator.base import Activator


class SequenceTestMenu:
    def __init__(self, player: SequencePlayer):
        self.player = player

    def run(self):
        while True:
            menu_options = self._build_menu()

            print("\nMenu:")
            for key, (description, _) in menu_options.items():
                print(f"{key}. {description}")

            choice = input("Enter your choice: ")

            if choice == "0":
                print("Exiting...")
                break

            selected = menu_options.get(choice)
            if selected:
                _, func = selected
                func()
            else:
                print("Invalid input.")

    def _build_menu(self):
        options = {}
        key_num = 1

        for name in self.player.sequence_names:
            options[str(key_num)] = (
                f"Play Sequence ({name})",
                lambda n=name: self.player.play(n)
            )
            key_num += 1

        for name, component in self.player.components.items():
            if isinstance(component, Animatronic):
                options[str(key_num)] = (
                    f"Test Animatronic ({name})",
                    component.test
                )
                key_num += 1

            elif isinstance(component, Dispenser):
                options[str(key_num)] = (
                    f"Test Dispenser ({name})",
                    component.test
                )
                key_num += 1

            elif isinstance(component, AudioPlayer):
                for bank_name in component.bank_names:
                    options[str(key_num)] = (
                        f"Test Audio ({name} - {bank_name})",
                        lambda c=component, b=bank_name: c.play(b)
                    )
                    key_num += 1

            elif isinstance(component, Activator):
                def _test_activator(c=component):
                    print("Testing activator... waiting for trigger.")
                    def _callback():
                        print("\n*** Activator triggered successfully! ***\n")
                    c.start(_callback)

                options[str(key_num)] = (
                    f"Test Activator ({name})",
                    _test_activator
                )
                key_num += 1

        options["0"] = ("Exit", None)
        return options
