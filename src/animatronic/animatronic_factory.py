from src.config import Config
from .gs_body import GSBody

class AnimatronicFactory:
    """Factory for creating animatronic instances based on configuration"""
    
    _animatronics = {
        'gs_body': GSBody,
    }
    
    @staticmethod
    def create(animatronic_type: str = None) -> object:
        """
        Create an animatronic instance based on configuration or specified type.
        
        Args:
            animatronic_type: Optional type override. If not provided, reads from config.
        
        Returns:
            Animatronic instance
        
        Raises:
            ValueError: If animatronic type is not found or not configured
        """
        config = Config()
        
        if animatronic_type is None:
            animatronic_type = config.get('animatronic.type', 'gs_body')
        
        if animatronic_type not in AnimatronicFactory._animatronics:
            raise ValueError(f"Unknown animatronic type: {animatronic_type}")
        
        animatronic_class = AnimatronicFactory._animatronics[animatronic_type]
        print(f"Creating Animatronic: {animatronic_type}")
        return animatronic_class()