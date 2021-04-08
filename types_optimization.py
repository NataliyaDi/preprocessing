import numpy as np


def check_and_cast_df_col(df, col_index, dtype):
    """
    Check if the column of DataFrame `df` with index `col_index` get in `dtype`.

    :param dtype:
    :param col_index:
    :param df: датафрейм с фичами
    :return: None
    """
    # integers and floats have different `info` which should be checked.
    if np.issubdtype(df[col_index].dtypes, np.integer):
        info = np.iinfo(dtype)
    elif np.issubdtype(df[col_index].dtypes, np.float):
        info = np.finfo(dtype)
    else:
        return False


def try_to_cast(df, col_index, dtypes):
    """
    Cast the column with index `col_index` in the first suitable type from array `dtypes`

    :param dtypes:
    :param col_index:
    :param df: df with features
    :return: None
    """
    for dtype in dtypes:
        if check_and_cast_df_col(df, col_index, dtype):
            break


def optimization_datatype(_df):
    """
    Optimization data types across features. Save data in the most optimal type in terms of memory.

    :param _df: df with features
    :return:
    """
    logging.info("Start optimization")
    for bin_feat in binary_feat:
        try_to_cast(_df, bin_feat, [np.int8])
    # all except binary features, dates, primary keys
    for col in set(_df.columns) - set(binary_feat) - set(key_feat):
        if np.issubdtype(_df[col].dtypes, np.integer):  # if the value is integer
            if _df[col].min() >= 0:  # if could be unsigned
                # then cast in unsigned int
                try_to_cast(_df, col, (np.uint8, np.uint16, np.uint32))
            else:  # else in int
                try_to_cast(_df, col, (np.int8, np.int16, np.int32))
        # cast float
        elif np.issubdtype(_df[col].dtypes, np.float):
            try_to_cast(_df, col, (np.float16, np.float32, np.float64))
