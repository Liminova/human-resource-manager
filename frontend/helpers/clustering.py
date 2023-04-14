def clustering(entries: list[str], size: int) -> list[list[str]]:
    """Takes a list of entries and returns a list of clusters"""
    clusters = []
    counter = 0

    for entry in entries:
        if counter == 0:
            clusters.append([])
        clusters[-1].append(entry)
        counter += 1
        if counter == size:
            counter = 0

    return clusters
