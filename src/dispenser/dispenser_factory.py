from src.config import Config
from .gs_card import GSCardDispenser

class DispenserFactory:
    """Factory for creating dispenser instances based on configuration"""
    
    _dispensers = {
        'gs_card': GSCardDispenser,
    }
    
    @staticmethod
    def create(dispenser_type: str = None, config_prefix: str = None) -> object:
        config = Config()

        if dispenser_type is None:
            dispenser_type = config.get('dispenser.type', 'gs_card')

        if dispenser_type not in DispenserFactory._dispensers:
            raise ValueError(f"Unknown dispenser type: {dispenser_type}")

        dispenser_class = DispenserFactory._dispensers[dispenser_type]
        return dispenser_class(config_prefix=config_prefix)