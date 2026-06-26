from eval.harness.verdict import decide_status


def _dims(anti=2, struct=2):
    return {
        "specificity": {"score": 2}, "anti_fabrication": {"score": anti},
        "action_quality": {"score": 2}, "honesty": {"score": 2},
        "structure": {"score": struct}, "skill_specific": {"score": 2},
    }


def test_scanner_hard_fail_overrides_pass():
    st = decide_status(run_status="OK", scanner_anti_fab=True,
                       judge_verdict="PASS", dimensions=_dims(), aggregate=11, mode="live")
    assert st == "ANTI_FAB_FAIL"


def test_dimension_zero_fails_even_if_aggregate_high():
    st = decide_status(run_status="OK", scanner_anti_fab=False,
                       judge_verdict="PASS", dimensions=_dims(struct=0),
                       aggregate=10, mode="live")
    assert st == "FAIL"


def test_clean_pass():
    st = decide_status(run_status="OK", scanner_anti_fab=False,
                       judge_verdict="PASS", dimensions=_dims(), aggregate=11, mode="live")
    assert st == "PASS"


def test_low_aggregate_fails():
    st = decide_status(run_status="OK", scanner_anti_fab=False,
                       judge_verdict="PASS", dimensions=_dims(), aggregate=9, mode="live")
    assert st == "FAIL"


def test_infra_error_propagates():
    st = decide_status(run_status="ERROR", scanner_anti_fab=False,
                       judge_verdict=None, dimensions={}, aggregate=None, mode="live")
    assert st == "ERROR"


def test_synthetic_ignores_anti_fab_dimension():
    st = decide_status(run_status="OK", scanner_anti_fab=False,
                       judge_verdict="PASS", dimensions=_dims(anti=0),
                       aggregate=10, mode="synthetic")
    assert st == "PASS"
