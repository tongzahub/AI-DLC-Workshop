"""OEE calculation. OEE = Availability x Performance x Quality.

Written 2024; formulas taken from the old Excel sheet.
"""


def compute_oee(planned_minutes: float, downtime_minutes: float,
                ideal_cycle_time: float, total_count: int, good_count: int) -> dict:
    run_time = planned_minutes - downtime_minutes

    availability = run_time / planned_minutes

    # pieces we *should* have been able to make in the run time vs what we made
    performance = (ideal_cycle_time * total_count) / run_time

    quality = good_count / total_count

    return {
        "availability": round(availability, 4),
        "performance": round(performance, 4),
        "quality": round(quality, 4),
        "oee": round(performance * quality, 4),
    }
