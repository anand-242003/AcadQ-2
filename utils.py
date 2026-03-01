def get_score_color(score: float) -> str:
    if score >= 60:
        return "#FFFFFF"
    if score >= 40:
        return "#F59E0B"
    return "#EF4444"


def get_score_grade(score: float) -> str:
    if score >= 75:
        return "A"
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


CHART_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family='-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif',
        color='#A0A0A0',
        size=11,
    ),
    margin=dict(t=20, b=16, l=8, r=16),
    height=340,
)

C = {
    "c1": "#FFFFFF",
    "c2": "#10B981",
    "c3": "#F59E0B",
    "c4": "#EF4444",
    "c5": "#3B82F6",
    "grid": "#1E1E1E",
    "axis": "#A0A0A0",
}
