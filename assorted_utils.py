
import numpy as np
def robust_std(input_arr: np.ndarray) -> float:
    """Compute the median absolute deviation assuming normally
    distributed data. This is a robust statistic.

    Parameters
    ----------
    input_arr: np.ndarray
        A numeric, 1d numpy array
    Returns
    -------
    float:
        A robust estimation of standard deviation.
    Notes
    -----
    If `input_arr` is an empty array or contains any NaNs, will return NaN.
    """
    mad = np.median(np.abs(input_arr - np.median(input_arr)))
    return 1.4826*mad




def noise_std(input_arr: np.ndarray, filter_length: int = 31) -> float:
    """Compute a robust estimation of the standard deviation of the
    noise in a signal `input_arr`. The noise is left after subtracting
    a rolling median filter value from the signal. Outliers are removed
    in 2 stages to make the estimation robust.

    Parameters
    ----------
    input_arr: np.ndarray
        1d array of signal (perhaps with noise)
    filter_length: int (default=31)
        Length of the median filter to compute a rolling baseline,
        which is subtracted from the signal `input_arr`. Must be an odd number.

    Returns
    -------
    float:
        A robust estimation of the standard deviation of the noise.
        If any valurs of `input_arr` are NaN, returns NaN.
    """
    if any(np.isnan(input_arr)):
        return np.NaN
    noise = input_arr - median_filter(input_arr, filter_length)
    # first pass removing positive outlier peaks
    # TODO: Confirm with scientific team that this is really what they want
    # (method is fragile if possibly have 0 as min)
    filtered_noise_0 = noise[noise < (1.5 * np.abs(noise.min()))]
    rstd = robust_std(filtered_noise_0)
    # second pass removing remaining pos and neg peak outliers
    filtered_noise_1 = filtered_noise_0[abs(filtered_noise_0) < (2.5 * rstd)]
    return robust_std(filtered_noise_1)
