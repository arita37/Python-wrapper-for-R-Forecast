from rpy2 import robjects
from rpy2.robjects.packages import importr


forecast = importr('forecast')
# TODO: replace with a Python function that extracts the first(only) element
frequency = robjects.r('frequency')       
NULL = robjects.NULL
NA = robjects.NA_Real

def ts(data, start=1, frequency=1):
  '''
  Turns the provided data into an R time series. 
  
  Args:
    data - Python sequence representing values of a regular time series.
    start - default 1; a number or 2-tuple to use as start index of sequence.
      If 2-tuple, it is (period, step), e.g. March 2010 is (2010, 3).
    frequency - default 1; number of points in each time period.
        e.g. 12 for monthly data with an annual period

  Returns:
    an object that maps to an R time series (class 'ts')
  '''
  ts = robjects.r('ts')
  rdata = robjects.FloatVector(data)
  if type(start) == tuple:
    start = robjects.r.c(*start)
  time_series = ts(rdata, start=start, frequency=frequency)  
  return time_series
  
  
def meanf(x, h=10, lam=NULL):
  '''
  Perform a mean forecast on the provided data by calling meanf() 
  from R Forecast.
  
  Args:
    x - an R time series, obtained from forecast_wrapper.ts()
    h - default 10; the forecast horizon.
    lam - BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    an object that maps to an R object of class 'forecast'
  '''
  return forecast.meanf(x, h, **{'lambda' : lam})
  
  
def thetaf(x, h=10):
  '''
  Perform a theta forecast on the provided data by calling thetaf() 
  from R Forecast. The theta forecast is equivalent to a random walk 
  forecast (rwf in R Forecast) with drift, with the drift equal to half 
  the slope of a linear regression model fitted to with a trend. The 
  theta forecast did well in the M3 competition.
  
  Args:
    x - an R time series, obtained from forecast_wrapper.ts()
    h - default 10; the forecast horizon.

  Returns:
    an object that maps to an R object of class 'forecast'
  '''
  return forecast.thetaf(x, h)


def naive(x, h=10, lam=NULL):
  '''
  Perform a naive forecast on the provided data by calling naive() 
  from R Forecast. This is also called the 'Last Observed Value' 
  forecast. The point forecast is a constant at the last observed value.
  
  Args:
    x - an R time series, obtained from forecast_wrapper.ts()
    h - default 10; the forecast horizon.
    lam - BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    an object that maps to an R object of class 'forecast'
  '''
  return forecast.naive(x, h, **{'lambda' : lam})


def snaive(x, h=None, lam=NULL):
  '''
  Perform a seasonal naive forecast on the provided data by calling 
  snaive() from R Forecast. This is also called the 'Last Observed 
  Seasonal Value' forecast. The point forecast is the value of the 
  series one full period in the past.
  
  Args:
    x - an R time series, obtained from forecast_wrapper.ts()
      For this forecast method, x should be periodic.
    h - Forecast horizon; default is 2 full periods of a periodic series
    lam - BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    an object that maps to an R object of class 'forecast'
  '''
  if h is None:
    h = 2 * frequency(x)[0]
  return forecast.snaive(x, h, **{'lambda' : lam})


def rwf(x, h=10, drift=False, lam=NULL):
  '''
  Perform a random walk forecast on the provided data by calling 
  rwf() from R Forecast. The forecast can have drift, which allows 
  a trend in the mean prediction, but by default, it does not.
  
  Args:
    x - an R time series, obtained from forecast_wrapper.ts()
    h - default 10; the forecast horizon.
    drift - default False. If True, a random walk with drift model is fitted.
    lam - BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    an object that maps to an R object of class 'forecast'
  '''
  return forecast.rwf(x, h, drift, **{'lambda' : lam})


def ets(x, h=None, model_spec='ZZZ', damped=NULL, alpha=NULL, 
        beta=NULL, gamma=NULL, phi=NULL, additive_only=False, lam=NULL,
        opt_crit='lik', nmse=3, ic='aicc', allow_multiplicative_trend=False):
  '''
  Automatically select and fit an exponential smoothing model on the 
  provided data using the ets() function from the R Forecast package, 
  and use it to produce a forecast over the given horizon.
  
  Args:
    x - an R time series, obtained from forecast_wrapper.ts()
        For this forecast method, x should be periodic.
    h - Forecast horizon; default is 2 full periods of a periodic series,
        or 10 steps for non-seasonal series.
    model_spec - Default is 'ZZZ'. A 3-letter string denoting the model type.
        Letters denote error, trend, and seasonal parts: A=additive, 
        N=none, M=multiplicative, Z=automatically selected. Legal 
        values for first part are (A, M, Z), all values are legal 
        for other parts.
    damped - If True, use a damped trend model. 
        Default is NULL, which tries damped/undamped models and 
        selects best model according to the selected ic.
    alpha - Smoothing parameter for error term. 
        Default is NULL, which fits this value.
    beta - Smoothing paramter for trend component. 
        Default is NULL, which fits this value.
    gamma - Smoothing parameter for seasonal component. 
        Default is NULL, which fits this value.
    phi - Damping parameter. Default is NULL, which fits this value.
    additive_only - Default False. If True, only try additive models.
    lam - BoxCox transformation parameter. The default is R's NULL value.
        If NULL, no transformation is applied. Otherwise, a Box-Cox 
        transformation is applied before forecasting and inverted after.
    opt_crit - Optimization criterion. Default is 'lik' for log-likelihood. 
        Other values are 'mse' (mean squared error), 'amse' (MSE averaged 
        over first nmse forecast horizons), 'sigma' (standard deviation of 
        residuals), and 'mae' (mean absolute error).
    nmse - number of steps in average MSE, if 'amse' is opt_crit.
        Restricted to 1 <= nmse <= 10.
    ic - information crierion. Default is 'aicc' for bias-corrected AIC.
        Other values are 'aic' for regular AIC, or 'bic' for BIC.
    allow_multiplicative_trend - Default is False. If True, consider models 
        with a multiplicative trend component. That type of model may grow 
        explosively.
        
  Returns:
    an object that maps to an R object of class 'forecast'
  '''
  kwargs = {'allow.multiplicative.trend' : allow_multiplicative_trend, 
            'additive.only' : additive_only, 
            'opt.crit' : opt_crit,
            'lambda' : lam}
  ets_model = forecast.ets(x, model=model_spec, damped=damped, alpha=alpha, 
                       beta=beta, gamma=gamma, phi=phi, ic=ic, **kwargs)
  if h is None:
    if frequency(x)[0] > 1:
      h = 2 * frequency(x)[0]
    else:
      h = 10
  # NB: default lambda is correct - it will be taken from model
  return forecast.forecast_ets(ets_model, h)


def auto_arima(x, h=None, d=NA, D=NA, max_p=5, max_q=5, max_P=2, max_Q=2,
               max_order=5, max_d=2, max_D=1, start_p=2, start_q=2, 
               start_P=1, start_Q=1, stationary=False, seasonal=True, 
               ic='aicc', xreg=NULL, newxreg=NULL, test='kpss', 
               seasonal_test='ocsb', lam=NULL):
  '''
  Use the auto.arima function from the R Forecast package to automatically 
  select an arima model order, fit the model to the provided data, and 
  generate a forecast.
  
  Args:
    x - an R time series, obtained from forecast_wrapper.ts()
        For this forecast method, x should be periodic.
    h - Forecast horizon; default is 2 full periods of a periodic series,
        or 10 steps for non-seasonal series.
    d - order of first differencing. Default is NA, which selects this 
        value based on the value of 'test' (KPSS test by default).
    D - order of seasonal differencing. Default is NA, which selects this 
        value based on 'seasonal_test' (OCSB test by default).
    max_p - maximum value for non-seasonal AR order
    max_q - maximum value for non-seasonal MA order
    max_P - maximum value for seasonal AR order
    max_Q - maximum value for seasonal MA order
    max_order - maximum value of p + q + P + Q
    start_p - starting value for non-seasonal AR order
    start_q - starting value for non-seasonal MA order
    start_P - starting value for seasonal AR order
    start_Q - starting value for seasonal MA order
    stationary - Default is False. If True, only consider stationary models.
    seasonal - Default is True. If False, only consider non-seasonal models.
    ic - information crierion. Default is 'aicc' for bias-corrected AIC.
        Other values are 'aic' for regular AIC, or 'bic' for BIC.
    xreg - An optional vector or matrix of regressors, which must have one 
        row/element for each point in x. Default is NULL, for no regressors.
    newxreg - If regressors were used to fit the model, then they must be 
        supplied for the forecast period as newxreg.
    test - Test to use to determine number of first differences. Default 
        is 'kpss', for the KPSS test. Other values are 'adf' for augmented 
        Dickey-Fuller, or 'pp' for Phillips-Perron.
    seasonal_test - Test to use to determine number of seasonal differences.
        Default is 'ocsb' for the Osborn-Chui-Smith-Birchenhall  test. 
        The alternative is 'ch' for the Canova-Hansen test. 
    lam - BoxCox transformation parameter. The default is R's NULL value.
        If NULL, no transformation is applied. Otherwise, a Box-Cox 
        transformation is applied before forecasting and inverted after.

  Returns:
    an object that maps to an R object of class 'forecast'
  '''
  kwargs = {'max.p' : max_p, 'max.q' : max_q, 'max.P' : max_P, 
            'max.Q' : max_Q, 'max.order' : max_order, 'max.d' : max_d, 
            'max.D' : max_D, 'start.p' : start_p, 'start.q' : start_q, 
            'start.P' : start_P, 'start.Q' : start_Q, 
            'seasonal.test' : seasonal_test, 'lambda' : lam}
  arima_model = forecast.auto_arima(x, d=d, D=D, stationary=stationary, 
                                    seasonal=seasonal, ic=ic, xreg=xreg, 
                                    test=test, **kwargs)
  if h is None:
    if frequency(x)[0] > 1:
      h = 2 * frequency(x)[0]
    else:
      h = 10
  # NB: default lambda is correct - it will be taken from model
  return forecast.forecast_Arima(arima_model, h, xreg=newxreg)






