# models/__init__.py
from .database import (
    Database,
    PeriodeModel,
    MatiereModel,
    EnseignantModel,
    FiliereModel,
    CorrespondreModel
)
from .module2_models import (
    EtudiantModel,
    EnseignementModel,
    AssisterModel,
    MessageModel
)

__all__ = [
    'Database',
    'PeriodeModel',
    'MatiereModel',
    'EnseignantModel',
    'FiliereModel',
    'CorrespondreModel',
    'EtudiantModel',
    'EnseignementModel',
    'AssisterModel',
    'MessageModel'
]