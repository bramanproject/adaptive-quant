# utils/validation.py

import pandas as pd


class Validation:

    @staticmethod
    def validate_dataframe(df: pd.DataFrame):

        required = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        for column in required:

            if column not in df.columns:

                raise ValueError(
                    f"Missing column: {column}"
                )

        if len(df) < 250:

            raise ValueError(
                "Not enough historical data"
            )

        if df.isnull().sum().sum() > 0:

            raise ValueError(
                "Dataset contains NaN values"
            )

        return True
