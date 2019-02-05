"""Abstract Formatter class
"""
class BaseFormatter:
    """Abstract Formatter class
    """
    def apply(self, labels):
        """Abstract method for applying formatter.

        Arguments:
            label tuple (list): All elements are str type,
                [0] : (goods, rates, arrows)
                [1] : (town1, rates, arrows)
                ~ (Max) [5] : (town5, ratws, arrows)

        Return:
            Formatted string (str)
            Empty string if failed
        """
        raise NotImplementedError()

    def is_valid(self, label):
        """Check the name of town is valid

        Arguments:
            label (tuple): (townname, rates, arrows)
                           All elements are str type

        Return:
            True if valid
            False if invalid
        """
        if not label[0] or label[0] == "UNKNOWN":
            return False
        return True

class FoxyFormatter(BaseFormatter):
    """Concreate formatter class for foxytrixy

        Refer to https://www.trevii.com/foxytrixy/UWO/
    """
    ARROW_DICT = {"0" : "u", "1" : "n", "2" : "d"} # up / neutral / down

    def apply(self, labels):
        try:
            if len(labels) < 2:
                raise Exception

            
            l_price = ['"%s" %s%s;' % (town[0], town[1], self.ARROW_DICT[town[2]])
                       for town in labels[1:] 
                       if self.is_valid(town)]
            result = '?price "{0}" : {1}'.format(labels[0][0], " ".join(l_price))
            
            return result
        except:
            return ""
