def calculate_evidence_signal(evidence):
    """
    Converts retrieved evidence relevance into a normalized signal.
    Evidence is supporting context, not proof of truth.
    """

    if not evidence:
        return {
            "evidence_score": 0.0,
            "evidence_strength": "No Evidence",
            "source_count": 0
        }

    scores = []

    for item in evidence:
        try:
            score = float(item.get("relevance", 0))
            scores.append(max(0, min(100, score)))
        except (TypeError, ValueError):
            continue

    if not scores:
        return {
            "evidence_score": 0.0,
            "evidence_strength": "No Evidence",
            "source_count": 0
        }

    # Strongest sources matter more than weak sources.
    scores.sort(reverse=True)

    top_scores = scores[:3]

    evidence_score = sum(top_scores) / len(top_scores)

    if evidence_score >= 70:
        strength = "Strong"
    elif evidence_score >= 45:
        strength = "Moderate"
    elif evidence_score >= 20:
        strength = "Weak"
    else:
        strength = "Very Weak"

    return {
        "evidence_score": round(evidence_score, 2),
        "evidence_strength": strength,
        "source_count": len(evidence)
    }


def combine_verification_scores(
    multimodal_score,
    evidence
):
    """
    Combines multimodal analysis with web evidence.

    Evidence does NOT override a strong visual contradiction.
    """

    evidence_data = calculate_evidence_signal(evidence)

    evidence_score = evidence_data["evidence_score"]

    multimodal_score = max(
        0,
        min(100, float(multimodal_score))
    )

    # Evidence has limited influence.
    final_score = (
        multimodal_score * 0.75
        + evidence_score * 0.25
    )

    # Prevent weak web evidence from making a contradictory
    # image look trustworthy.
    if multimodal_score < 30 and evidence_score < 60:
        final_score = min(final_score, 39)

    if final_score >= 65:
        decision = "Likely Consistent"

    elif final_score >= 40:
        decision = "Needs Verification"

    else:
        decision = "Potentially Misleading"

    return {
        "multimodal_score": round(multimodal_score, 2),
        "evidence_score": round(evidence_score, 2),
        "final_score": round(final_score, 2),
        "decision": decision,
        "evidence_strength":
            evidence_data["evidence_strength"],
        "source_count":
            evidence_data["source_count"]
    }