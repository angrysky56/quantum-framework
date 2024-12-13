"""Core system components initialization."""
from .emotional_processor import EmotionalProcessor
from .ethical_processor import EthicalProcessor
from .synergistic_processor import SynergisticProcessor
from .refusal_processor import RefusalProcessor

__all__ = [
    'EmotionalProcessor',
    'EthicalProcessor',
    'SynergisticProcessor',
    'RefusalProcessor'
]