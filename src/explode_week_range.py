import pandas as pd
import re
import pathlib


def explode_week_range(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize the "Week #" field by stripping and replacing any whitespace with a single space
    df['Week #'] = df['Week #'].str.strip().str.replace(r'\s+', ' ', regex=True)

    # Function to explode a single row's week field
    def explode_row(week):
        parts = week.split(',')
        expanded_weeks = []

        for part in parts:
            part = part.strip()

            try:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    expanded_weeks.extend(range(start, end + 1))
                else:
                    expanded_weeks.append(int(part))
            except ValueError:
                # If we can't parse the part, just append it as is
                expanded_weeks.append(part)

        return expanded_weeks

    # Apply the explosion to each row
    exploded_rows = []
    for index, row in df.iterrows():
        weeks = explode_row(row['Week #'])
        for week in weeks:
            new_row = row.copy()
            new_row['Week #'] = week
            exploded_rows.append(new_row)

    exploded_df = pd.DataFrame(exploded_rows)

    return exploded_df


path = pathlib.Path(
    "/Users/mkbabb/Library/CloudStorage/GoogleDrive-mbabb@ncsu.edu/Shared drives/FI-LEADS-CVM/Curriculum Map/data/curriculum-tmp.csv"
)
df = pd.read_csv(path)

exploded_df = explode_week_range(df)
exploded_path = path.parent / 'curriculum-exploded.csv'

exploded_df.to_csv(exploded_path, index=False)
