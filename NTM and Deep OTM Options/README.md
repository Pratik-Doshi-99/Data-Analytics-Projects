Intuitively, the price of an Out of the Money Option (OTM) reflects the market’s perception of the
probability that the option will expire in the money. The uncertainty about the pandemic’s (COVID-19)
impact on the economy and cash flows of companies makes large market moves more probable. This further
implies that the price of deep OTM options relative to near the money (NTM) options will be higher. We
devised a simple algorithm to test this hypothesis. The algorithm simply iterates through the closing
price of a given stock and fetches the prices of the deep OTM and NTM options. We further analyse the
output of the algorithm to understand whether the ratio of price of deep OTM and NTM options increased
in the months of February, March and April 2020. In the sample of 10 stocks (the one used throughout 
the study) across industries it was found that the call options of 9 stocks showed significant increase
in the ratio from February (pre-COVID) to March (during COVID). The put options gave an ambiguous result
with significant increase in the ratio for only 6 stocks in the same period.

The Algorithm:
Please refer to the powerpoint presentation for information about the calculation of the strike price of 
NTM and OTM options. The algorithm is capable of extracting data for arbitrarily defined depth values.
It can also handle multiple depth values. This is taken care by the steps variable

step_list = [4, 5, 6]  -> implies that the algorithm will individually collect data for OTM options (both call
and put options) that are 4, 5 and 6 units away from the NTM options. (refer to ppt for calculation table.

The algorithm requires the following inputs:
1) base_folder: The folder where all the files will be extracted
2) logs_folder: The folder where all the log files will be stored
3) start: datetime object representing the date from which the data will be 
          extracted
4) end: datetime object representing the date till which the data will be 
          extracted
5) step_list: the list containing all values of the depth variable for which
          data has to be extracted
6) min_step: the csv file which contains the sample of stocks whose options have
          to be analysed alongwith the multiple in which that stock's option must be
          expressed. Details of columns in OptionData.py
7) expiries: dictionary that mentions the expiry date for options given the month (represented by the key
          value of the dictionary). This particular parameter prevents the algorithm from being
          used for more than 1 year. To fetch data for more than 1 year period, one will have to define
          multiple such dictionaries and make certain changes in the main iteration.
          
 Note:
 It should be noted that if any of the parameters is wrongly inputed, the algorithm will not work.
 The expiries dictioary must mention the expiry dates for the months in a year. The start and end date must
 refer to that same year. If the depth variable is too high, very few observations will be extracted (due to
 liquidity constraints for such deep OTM options). If the min_step dataframe has wrong values of the multiple, the
 algorithm will return null tables because it wont be able to determine the correct strike prices.
 
