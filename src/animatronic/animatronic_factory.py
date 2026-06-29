from src.config import Config
from .gs_body import GSBody

class AnimatronicFactory:
    """Factory for creating animatronic instances based on configuration"""
    
    _animatronics = {
        'gs_body': GSBody,
    }
    
    @staticmethod
    def create(animatronic_type: str = None, config_prefix: str = None) -> object:
        config = Config()

        if animatronic_type is None:
            animatronic_type = config.get('animatronic.type', 'gs_body')

        if animatronic_type not in AnimatronicFactory._animatronics:
            raise ValueError(f"Unknown animatronic type: {animatronic_type}")

        animatronic_class = AnimatronicFactory._animatronics[animatronic_type]
        print(f"Creating Animatronic: {animatronic_type}")
        return animatronic_class(config_prefix=config_prefix)