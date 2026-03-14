import pandas as pd
from datetime import datetime


def export_to_excel(pairs_df: pd.DataFrame, output_path: str = None) -> str:
    """
    Export pairing results to a formatted Excel file.

    Args:
        pairs_df:    DataFrame with columns: big_sister, little_sister, match_score
        output_path: Optional file path. Defaults to timestamped filename.

    Returns:
        The path the file was saved to.
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"pairing_results_{timestamp}.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pairs_df.to_excel(writer, index=False, sheet_name="Pairs")

        workbook = writer.book
        worksheet = writer.sheets["Pairs"]

        # Auto-size columns
        for col in worksheet.columns:
            max_len = max(len(str(cell.value or "")) for cell in col) + 4
            worksheet.column_dimensions[col[0].column_letter].width = max_len

    return output_path