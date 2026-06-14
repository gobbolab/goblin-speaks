from src.config import Config
from .gs_card import GSCardDispenser

class DispenserFactory:
    """Factory for creating dispenser instances based on configuration"""
    
    _dispensers = {
        'gs_card': GSCardDispenser,
    }
    
    @staticmethod
    def create(dispenser_type: str = None) -> object:
        """
        Create a dispenser instance based on configuration or specified type.
        
        Args:
            dispenser_type: Optional type override. If not provided, reads from config.
        
        Returns:
            Dispenser instance
        
        Raises:
            ValueError: If dispenser type is not found or not configured
        """
        config = Config()
        
        if dispenser_type is None:
            dispenser_type = config.get('dispenser.type', 'gs_card')
        
        if dispenser_type not in DispenserFactory._dispensers:
            raise ValueError(f"Unknown dispenser type: {dispenser_type}")
        
        dispenser_class = DispenserFactory._dispensers[dispenser_type]
        print(f"Creating dispenser: {dispenser_type}")
        return dispenser_class()