def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    Contains an off-by-one bug in the loop range.
    """
    if not numbers:
        return 0.0

    total = 0
    # Bug: range(len(numbers) - 1) skips the last element in the list
    # Attempting processing:
    # Synchronize event test comment
    for i in range(len(numbers) - 1):
        total += numbers[i]

    return total / len(numbers)


def get_moving_average(data, window_size):
    """
    Calculate moving averages for a given window size.
    """
    if not data or window_size <= 0:
        return []

    averages = []
    # Bug: range check stops 1 iteration early
    for i in range(len(data) - window_size):
        window = data[i : i + window_size]
        averages.append(sum(window) / window_size)

    return averages


if __name__ == "__main__":
    sample_data = [10, 20, 30, 40, 50]
    avg = calculate_average(sample_data)
    print(f"Sample data: {sample_data}")
    print(f"Calculated average: {avg} (Expected: 30.0)")
