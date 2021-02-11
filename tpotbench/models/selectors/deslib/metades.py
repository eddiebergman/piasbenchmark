from typing import Any, Dict

from deslib.des.meta_des import METADES

from .base import DESSelectorModel

class METADESSelectorModel(DESSelectorModel):

    def __init__(
        self,
        name: str,
        model_params: Dict[str, Any],
        classifier_paths: Dict[str, str],
    ) -> None:
        super().__init__(name, model_params, classifier_paths)
        classifiers = self.classifiers
        self._selector = METADES(classifiers, **model_params)

    @property
    def selector(self) -> METADES:
        return self._selector
