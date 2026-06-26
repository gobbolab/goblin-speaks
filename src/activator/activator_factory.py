from src.config import Config
from .gs_button import GSButton

class ActivatorFactory:
    """Factory for creating activator instances based on configuration"""
    
    _activators = {
        'gs_button': GSButton,
    }
    
    @staticmethod
    def create(activator_type: str = None) -> object:
        config = Config()
        
        if activator_type is None:
            activator_type = config.get('activator.type', 'gs_button')
        
        if activator_type not in ActivatorFactory._activators:
            raise ValueError(f"Unknown activator type: {activator_type}")
        
        activator_class = ActivatorFactory._activators[activator_type]
        print(f"Creating activator: {activator_type}")
        return activator_class()
