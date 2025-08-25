from rapidfuzz import fuzz

def similar(a: str, b: str) -> int:
    """Token-based fuzzy similarity 0..100."""
    return fuzz.token_set_ratio(a, b)

def is_potential_match(title_a: str, title_b: str, min_score: int = 86) -> bool:
    return similar(title_a, title_b) >= min_score
