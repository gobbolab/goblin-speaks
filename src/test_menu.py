from player.base import BasePlayer

class TestMenu:
    def __init__(self, player: BasePlayer):
        self.player = player

    def run(self):
        menu_options = {
            "1": ("Play", self.player.play),
            "2": ("Test Animatronic", self.player.test_animatronic),
            "3": ("Test Dispenser", self.player.test_dispenser),
            "4": ("Step Dispenser", self.player.step_dispenser),
            "5": ("Test Audio", self.player.test_audio),
            "6": ("Test Activator", self.player.test_activator),
            "0": ("Exit", None)
        }

        while True:
            print("\nMenu:")
            for key, (description, _) in menu_options.items():
                print(f"{key}. {description}")

            choice = input("Enter your choice: ")

            if choice == "0":
                print("Exiting...")
                break

            selected_option = menu_options.get(choice)

            if selected_option:
                description, func = selected_option
                func() 
            else:
                print("Invalid input.")
