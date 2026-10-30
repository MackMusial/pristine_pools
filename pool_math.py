"""Example module so the test suite has something real to check.
Replace with your team's actual code."""


def chlorine_status(free_chlorine_ppm: float) -> str:
    """Classify a free chlorine reading. Typical target range is 1-3 ppm."""
    if free_chlorine_ppm < 0:
        raise ValueError("ppm can't be negative")
    if free_chlorine_ppm < 1:
        return "low"
    if free_chlorine_ppm > 3:
        return "high"
    return "ok"
