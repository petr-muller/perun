"""Tests of regression analysis functionality.

Every model is tested on a set of provided examples and the computation results are compared with
the expected values. This ensures that the regression analysis formulas are correct.
Sources (if any) to examples are provided in the test functions.

The postprocessby CLI is tested in test_cli module.
"""

from perun.postprocess.regression_analysis.run import postprocess

__author__ = 'Jiri Pavela'


def profile_filter(generator, rule):
    """Finds concrete profile by the rule in profile generator.

    Arguments:
        generator(generator): stream of profiles as tuple: (name, dict)
        rule(str): string to search in the name

    Returns:
        dict: first profile with name containing the rule
    """
    # Loop the generator and test the rule
    for profile in generator:
        if rule in profile[0]:
            return profile[1]
    # No match found
    return None


def compare_results(expected, actual, eps=0.0001):
    """Compare two float values with eps tolerance.

    Arguments:
        expected(float): the expected result value
        actual(float): the actual result value
        eps(float): the tolerance value
    Returns:
        None
    """
    assert abs(abs(expected) - abs(actual)) < eps


def generate_models_by_uid(profile, uid_sequence):
    """Provides computed models results for each uid in the specified uid sequence.

    Arguments:
        profile(dict): the whole profile with 'models' results
        uid_sequence(list of str): list of uid values to search for
    Returns:
        generator: stream of lists with models dictionaries according to uid sequence
    """
    models = profile['profile']['global']['models']
    for uid in uid_sequence:
        yield [m for m in models if m['uid'] == uid]


def test_const_model(postprocess_profiles):
    """Test the constant model computation.

    The r^2 coefficient computation is currently not supported

    Both data sets were created manually as no constant regression analysis example was found.

    Expects to pass all assertions.
    """
    # Get the profile with exponential model testing data
    const_model = profile_filter(postprocess_profiles, 'const_model')
    assert const_model is not None

    # Perform the analysis
    code, _, profile = postprocess(
        const_model, method='full', regression_models=['const'], steps=1)
    assert code.value == 0
    models = generate_models_by_uid(profile, ['const::test1', 'const::test2'])

    # Example no. 1:
    # constant line: y = 3
    # expected results:
    #   a = b0 = 3.0
    #   b = b1 = 0.0
    #   r^2    = 0.0 - coefficient computation is currently unavailable
    model = next(models)[0]
    compare_results(model['r_square'], 0.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 3.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 0.0)

    # Example no. 2:
    # constant line: y = 2.5
    # expected results:
    #   a = b0 = 2.5
    #   b = b1 = 0.0
    #   r^2    = 0.0 - coefficient computation is currently unavailable
    model = next(models)[0]
    compare_results(model['r_square'], 0.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 2.5)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 0.0)


def test_linear_model(postprocess_profiles):
    """Test the linear model computation.

    Contains one sourced and one created example.

    Expects to pass all assertions.
    """
    # Get the profile with exponential model testing data
    linear_model = profile_filter(postprocess_profiles, 'linear_model')
    assert linear_model is not None

    # Perform the analysis
    code, _, profile = postprocess(
        linear_model, method='full', regression_models=['linear'], steps=1)
    assert code.value == 0
    models = generate_models_by_uid(profile, ['linear::test1', 'linear::test2'])

    # Example no. 1:
    # source: Probability and Statistics for Engineering and the Sciences, 8th ed., example 12.4
    # expected results:
    #   a = b0 = 75.212432
    #   b = b1 = -0.20938742
    #   r^2    = 0.791
    model = next(models)[0]
    compare_results(model['r_square'], 0.791, 0.001)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 75.212432)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], -0.20938742)

    # Example no. 2:
    # linear line: 8 + 2.5x
    # expected results:
    #   a = b0 = 8
    #   b = b1 = 2.5
    #   r^2    = 1.0
    model = next(models)[0]
    compare_results(model['r_square'], 1.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 8)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 2.5)


def test_quad_model_using_power(postprocess_profiles):
    """Test the quadratic model computation which is done using the power model method.

    Contains only one created example.

    Expects to pass all assertions.
    """
    # Get the profile with quadratic model testing data
    quad_model = profile_filter(postprocess_profiles, 'quad_model')
    assert quad_model is not None

    # Perform the analysis of quadratic-expected models using the power analysis, which should
    # produce correct quadratic-like results
    code, _, profile = postprocess(quad_model, method='full', regression_models=['power'], steps=1)
    assert code.value == 0
    models = generate_models_by_uid(profile, ['quad::test1'])

    # Example no. 1:
    # quadratic curve: x^2
    # expected results:
    #   a = b0 = 1.0
    #   b = b1 = 2.0
    #   r^2    = 1.0
    model = next(models)[0]
    compare_results(model['r_square'], 1.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 1.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 2.0)


def test_log_model(postprocess_profiles):
    """Test the logarithmic model computation.

    Contains one sourced and one created example.

    Expects to pass all assertions.
    """
    # Get the profile with logarithmic model testing data
    pow_model = profile_filter(postprocess_profiles, 'log_model')
    assert pow_model is not None

    # Perform the analysis
    code, _, profile = postprocess(pow_model, method='full', regression_models=['log'], steps=1)
    assert code.value == 0
    models = generate_models_by_uid(profile, ['log::test1', 'log::test2'])

    # Example no. 1:
    # link: 'https://mathbits.com/MathBits/TISection/Statistics2/logarithmic.htm'
    # expected results:
    #   a = b0 = 6.099
    #   b = b1 = 6.108
    #   r^2    = 0.9863058
    model = next(models)[0]
    compare_results(model['r_square'], 0.9863058)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 6.099, 0.01)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 6.108, 0.01)

    # Example no. 2:
    # logarithmic curve: 0 + 0.434294482 * ln(x)
    # expected results:
    #   a = b0 = 0
    #   b = b1 = 0.434294482
    #   r^2    = 1.0
    model = next(models)[0]
    compare_results(model['r_square'], 1.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 0.434294482)


def test_power_model(postprocess_profiles):
    """Test the power model computation.

    Contains two sourced and one created example.

    Expects to pass all assertions.
    """
    # Get the profile with power model testing data
    pow_model = profile_filter(postprocess_profiles, 'pow_model')
    assert pow_model is not None

    # Perform the analysis
    code, _, profile = postprocess(pow_model, method='full', regression_models=['power'], steps=1)
    assert code.value == 0
    models = generate_models_by_uid(profile, ['pow::test1', 'pow::test2', 'pow::test3'])

    # Example no. 1:
    # link: 'http://www.real-statistics.com/regression/power-regression/'
    # expected results:
    #   a = b0 = 16.6575389
    #   b = b1 = 0.23438143
    #   r^2    = 0.56822483
    model = next(models)[0]
    compare_results(model['r_square'], 0.56822483)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 16.6575389)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 0.23438143)

    # Example no. 2:
    # link: 'https://mathbits.com/MathBits/TISection/Statistics2/power.htm'
    # expected results:
    #   a = b0 = 24.12989312
    #   b = b1 = 0.65949782
    #   r^2    = 0.999992507
    model = next(models)[0]
    compare_results(model['r_square'], 0.999992507)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 24.12989312)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 0.65949782)

    # Example no. 3:
    # power curve: 3 * x^3
    # expected results:
    #   a = b0 = 3
    #   b = b1 = 3
    #   r^2    = 1.0
    model = next(models)[0]
    compare_results(model['r_square'], 1.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 3.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 3.0)


def test_exp_model(postprocess_profiles):
    """Test the exponential model computation.

    Contains two sourced and one created example.

    Expects to pass all assertions.
    """
    # Get the profile with exponential model testing data
    exp_model = profile_filter(postprocess_profiles, 'exp_model')
    assert exp_model is not None

    # Perform the analysis
    code, _, profile = postprocess(exp_model, method='full', regression_models=['exp'], steps=1)
    assert code.value == 0
    models = generate_models_by_uid(profile, ['exp::test1', 'exp::test2', 'exp::test3'])

    # Example no. 1:
    # link: 'https://www.youtube.com/watch?v=aw-GluLZIWA'
    # expected results:
    #   a = b0 = 0.1377
    #   b = b1 = 1.023778
    #   r^2    = 0.9652
    model = next(models)[0]
    compare_results(model['r_square'], 0.9652)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 0.1377)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 1.023778)

    # Example no. 2:
    # link: 'http://www.real-statistics.com/regression/exponential-regression-models/
    # exponential-regression/'
    # expected results:
    #   a = b0 = 14.0513516
    #   b = b1 = 1.016221137
    #   r^2    = 0.88161289
    model = next(models)[0]
    compare_results(model['r_square'], 0.88161289)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 14.0513516)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 1.016221137)

    # Example no. 3:
    # exponential curve y = 1 * 2^x
    # expected results:
    #   a = b0 = 1.0
    #   b - b1 = 2.0
    #   r^2    = 1.0
    model = next(models)[0]
    compare_results(model['r_square'], 1.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b0'][0], 1.0)
    compare_results([c['value'] for c in model['coeffs'] if c['name'] == 'b1'][0], 2.0)
