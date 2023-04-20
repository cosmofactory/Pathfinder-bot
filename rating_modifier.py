import scipy.stats as st


def rating_modifier(rating, number_of_ratings):
    """Uses confidence interval algorithm.
    Finds better correlation between rating and amount of ratings.
    """

    std = 0.3
    confidence_level = 0.95
    z_value = st.norm.ppf((1 + confidence_level) / 2)

    lower_bound = rating - z_value * (std / (number_of_ratings ** 0.5))
    upper_bound = rating + z_value * (std / (number_of_ratings ** 0.5))

    return (rating - (upper_bound-lower_bound))
