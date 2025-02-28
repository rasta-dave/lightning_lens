import os
import pytest
import pandas as pd
import numpy as np
import tempfile
from unittest.mock import patch, MagicMock

# Importing the functions from the visualizer script
from src.scripts.visualizer import (
    create_output_directory
)

class TestVisualizer:

    @pytest.fixture
    def sample_predictions(self):
        """ Create a sample predictions Dataframe """
        return pd.DataFrame({
            'channel_id': ['ch1', 'ch2', 'ch3', 'ch4', 'ch5'],
            'timestamp': pd.date_range(start='2024-01-01', periods=5),
            'balance_velocity': np.random.rand(5),
            'liquidity_stress': np.random.uniform(0, 1, 5),
            'hour_of_day': np.random.randint(0, 24, 5),
            'day_of_week': np.random.randint(0, 7, 5),
            'balance_ratio': np.random.uniform(0, 1, 5),
            'predicted_optimal_ratio': np.random.uniform(0, 1, 5),
            'current_ratio': np.random.uniform(0, 1, 5),
            'adjustment_needed': np.random.uniform(-0.5, 0.5, 5)
        })
    
    @pytest.fixture
    def temp_csv(self, sample_predictions):
        """ Create a temporary CSV file with sample predictions """
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            sample_predictions.to_csv(tmp.name, index=False)
            return tmp.name
        
    @pytest.fixture
    def cleanup_files(self):
        """ Fixture to clean up any files created during testing """
        files_to_remove = []
        yield files_to_remove
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_create_output_directory(self):
        """ Test creating output directory """
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = os.path.join(temp_dir, "visualization")
            result = create_output_directory(test_dir)

            assert os.path.exists(test_dir)
            assert result == test_dir
            