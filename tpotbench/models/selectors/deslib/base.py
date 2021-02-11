from typing import Any, Dict
from abc import abstractmethod

import numpy as np

from ..selector_model import SelectorModel


class DESSelectorModel(SelectorModel):

    @abstractmethod
    def __init__(
        self,
        name: str,
        model_params: Dict[str, Any],
        classifier_paths: Dict[str, str],
    ) -> None:
        super().__init__(name, model_params, classifier_paths)

    @property
    @abstractmethod
    def selector(self) -> Any:
        raise NotImplementedError

    def ensemble_selector(self) -> bool:
        return True

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.selector.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.selector.predict_proba(X)

    def selections(self, X: np.ndarray) -> np.ndarray:
        competences = self.competences(X)
        selections = self.selector.select(competences)
        return selections

    def competences(self, X: np.ndarray) -> np.ndarray:
        distances, neighbors = self.selector._get_region_competence(X)

        if self._uses_proba():
            classifier_probabilities = self.selector._predict_proba_base(X)
            competences = self.selector.estimate_competence(
                query=X, neighbors=neighbors, probabilities=classifier_probabilities,
                distances=distances)
        else:
            classifier_predictions = self.selector._predict_proba_base(X)
            competences = self.selector.estimate_competence_from_proba(
                query=X, neighbors=neighbors, predicitons=classifier_predictions,
                distances=distances)

        return competences

    def _uses_proba(self):
        return (
            hasattr(self.selector, 'estimate_competence_from_proba')
            and self.selector.needs_proba
        )
