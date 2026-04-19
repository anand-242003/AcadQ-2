"""Utility functions and chart constants for AcadIQ."""


def get_score_color(score: float) -> str:
    """Return color for score display (light theme)."""
    if score >= 60:
        return "#1b6a5b"  # secondary/green
    if score >= 40:
        return "#ae2448"  # accent amber
    return "#ba1a1a"      # error red


def get_score_grade(score: float) -> str:
    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 75:
        return "A-"
    if score >= 70:
        return "B+"
    if score >= 60:
        return "B"
    if score >= 45:
        return "C"
    if score >= 30:
        return "D"
    return "F"


def get_result_label(score: float) -> str:
    if score >= 75:
        return "Excellent"
    if score >= 60:
        return "Good"
    if score >= 45:
        return "Average"
    if score >= 30:
        return "Below Average"
    return "Critical"


def validate_inputs(raw: dict) -> list:
    errors = []

    total_study = raw['study_hours'] + raw['self_study_hours'] + raw['online_classes_hours']
    if total_study > 20:
        errors.append(f"Total study time ({total_study:.1f} hrs/day) seems unrealistically high.")

    min_screen = raw['social_media_hours'] + raw['gaming_hours'] + raw['online_classes_hours']
    if raw['screen_time_hours'] < min_screen:
        errors.append(
            f"Screen time ({raw['screen_time_hours']} hrs) is less than "
            f"sub-components combined ({min_screen:.1f} hrs)."
        )

    total_day = (
        raw['study_hours'] + raw['self_study_hours'] + raw['online_classes_hours']
        + raw['social_media_hours'] + raw['gaming_hours']
        + raw['sleep_hours'] + raw['exercise_minutes'] / 60
    )
    if total_day > 24:
        errors.append(f"Combined hours ({total_day:.1f}) exceed 24 hours in a day.")

    if raw['sleep_hours'] < 4:
        errors.append("Sleep below 4 hours is extremely low.")

    if raw['burnout_level'] > 80 and raw['mental_health_score'] >= 9:
        errors.append("Very high burnout with very high mental health score are contradictory.")

    if raw['productivity_score'] > 85 and raw['study_hours'] < 1:
        errors.append("High productivity with less than 1 hour study seems inconsistent.")

    if raw['caffeine_intake_mg'] >= 580:
        errors.append("Caffeine intake at or above 580 mg/day exceeds safe daily limits.")

    return errors


# ─── Chart Configuration (Light Theme) ──────────────────────────────────────

CHART_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family='Inter, sans-serif',
        color='#544246',
        size=11,
    ),
    margin=dict(t=20, b=16, l=8, r=16),
    height=340,
)

C = {
    "c1": "#510122",   # primary
    "c2": "#1b6a5b",   # secondary
    "c3": "#ae2448",   # accent
    "c4": "#877276",   # muted
    "c5": "#6e1a37",   # primary-container
    "grid": "rgba(218,192,196,.15)",
    "axis": "#544246",
}
