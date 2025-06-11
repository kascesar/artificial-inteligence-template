"""
***

.. include:: ../TODO.md

***

.. include:: ../README.md
"""

import os
import warnings

import mlflow
import pandas as pd

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
warnings.filterwarnings("ignore", category=UserWarning)

if os.environ.get("MLFLOW_TRACKING_URI", None):
    mlflow_uri = os.environ.get("MLFLOW_TRACKING_URI", None)
    mlflow.set_tracking_uri(mlflow_uri)

mlflow.enable_system_metrics_logging()
mlflow.tensorflow.autolog(checkpoint_save_best_only=False)
