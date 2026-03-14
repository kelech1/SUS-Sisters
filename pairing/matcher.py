import pandas as pd


INTEREST_WEIGHT = 3
COURSE_WEIGHT = 2
YEAR_WEIGHT = 1


def _parse_interests(value) -> set:
    """Convert a comma-separated interests string into a lowercase set."""
    if pd.isna(value) or not str(value).strip():
        return set()
    return {i.strip().lower() for i in str(value).split(",")}


def _score(big: pd.Series, little: pd.Series) -> float:
    """
    Score a potential big/little pairing. Higher = better match.

    +3 per shared interest
    +2 if same course
    +1 if same year group
    """
    score = 0.0

    big_interests = _parse_interests(big.get("interests", ""))
    lil_interests = _parse_interests(little.get("interests", ""))
    score += len(big_interests & lil_interests) * INTEREST_WEIGHT

    if pd.notna(big.get("course")) and pd.notna(little.get("course")):
        if str(big["course"]).strip().lower() == str(little["course"]).strip().lower():
            score += COURSE_WEIGHT

    if pd.notna(big.get("year_group")) and pd.notna(little.get("year_group")):
        if str(big["year_group"]).strip() == str(little["year_group"]).strip():
            score += YEAR_WEIGHT

    return score


def pair_sisters(
    big_sisters: pd.DataFrame,
    little_sisters: pd.DataFrame,
) -> tuple:
    """
    Match little sisters to big sisters based on shared interests, course, and year group.

    Each big sister gets at least one little sister. If there are more little sisters
    than big sisters, the best-scoring big sister receives a second little sister,
    repeating until all little sisters are assigned.

    Args:
        big_sisters:    DataFrame with columns: name, interests, course, year_group
        little_sisters: DataFrame with columns: name, interests, course, year_group

    Returns:
        (pairs_df, unmatched_df)
        pairs_df     -- columns: big_sister, little_sister, match_score
        unmatched_df -- empty DataFrame (all littles are always assigned)
    """
    big_sisters = big_sisters.copy().reset_index(drop=True)
    little_sisters = little_sisters.copy().reset_index(drop=True)

    # Normalise column names to lowercase with underscores
    big_sisters.columns = [c.strip().lower().replace(" ", "_") for c in big_sisters.columns]
    little_sisters.columns = [c.strip().lower().replace(" ", "_") for c in little_sisters.columns]

    # Build full score matrix: score_matrix[b_idx][l_idx] = float
    score_matrix = {}
    for b_idx, big in big_sisters.iterrows():
        score_matrix[b_idx] = {}
        for l_idx, little in little_sisters.iterrows():
            score_matrix[b_idx][l_idx] = _score(big, little)

    assigned_littles = set()
    pairs = []

    # First pass: give every big sister their single best available little sister
    for b_idx, big in big_sisters.iterrows():
        available = {l: s for l, s in score_matrix[b_idx].items() if l not in assigned_littles}
        if not available:
            break
        best_l = max(available, key=available.get)
        assigned_littles.add(best_l)
        pairs.append({
            "big_sister": big["name"],
            "little_sister": little_sisters.loc[best_l, "name"],
            "match_score": round(score_matrix[b_idx][best_l], 2),
        })

    # Second pass: assign any remaining little sisters to the highest-scoring big
    remaining = [l for l in little_sisters.index if l not in assigned_littles]
    for l_idx in remaining:
        scores = {b_idx: score_matrix[b_idx][l_idx] for b_idx in score_matrix}
        best_b = max(scores, key=scores.get)
        pairs.append({
            "big_sister": big_sisters.loc[best_b, "name"],
            "little_sister": little_sisters.loc[l_idx, "name"],
            "match_score": round(score_matrix[best_b][l_idx], 2),
        })

    pairs_df = pd.DataFrame(pairs, columns=["big_sister", "little_sister", "match_score"])
    pairs_df = pairs_df.sort_values("match_score", ascending=False).reset_index(drop=True)
    unmatched_df = pd.DataFrame(columns=["name"])

    return pairs_df, unmatched_df