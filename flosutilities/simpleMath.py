def clip(min, max, value):
    """Limits a number between min and max

    Args:
        min (any number): Lower value
        max (any number): Upper value
        value (any number): The number to check

    Returns:
        any number: the cliped value
    """
    return min if value < min else max if value > max else value