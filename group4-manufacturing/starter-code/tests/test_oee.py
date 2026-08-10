from app.oee import compute_oee


def test_oee_normal_day():
    r = compute_oee(planned_minutes=480, downtime_minutes=0,
                    ideal_cycle_time=0.5, total_count=900, good_count=880)
    assert r["availability"] == 1.0
    assert 0 < r["oee"] <= 1.0


def test_quality_factor():
    r = compute_oee(planned_minutes=480, downtime_minutes=0,
                    ideal_cycle_time=0.5, total_count=100, good_count=50)
    assert r["quality"] == 0.5
