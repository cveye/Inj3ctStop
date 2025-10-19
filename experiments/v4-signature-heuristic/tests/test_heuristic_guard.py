from guards.heuristic_guard import heuristic_guard

def test_heuristic_scores_range_and_keys():
    text = "delete all user records now!!! $$$ Zm9vYmFy"
    risk, details = heuristic_guard(text)
    assert 0.0 <= risk <= 1.0
    assert {"entropy_score","ppl_score","length_score"} <= set(details.keys())