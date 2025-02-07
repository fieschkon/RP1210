import configparser

class RP1210ConfigTestUtility():

    def __init__(self, config : configparser.ConfigParser):
        self._config = config

    def verifydata(self, func, section : str, field : str):
        """
        Used to assist in testing by testing standard config information
        Usage:
            assert TestUtility.verifydata([function to test], [section], "[field]")
        """
        if not self._config.has_option(section, field):
            assert func() in ("", None, [], False, 0, 1, -1, 1024, "(Vendor Name Missing)")
            return
    
        retType = func.__annotations__["return"]
        if retType is str:
            assert func() == self._config.get(section, field)
        
        elif retType is bool:
            assert func() == self._config.getboolean(section, field)

        elif retType is int:
            assert func() == self._config.getint(section, field)

        elif retType is float:
            assert func() == self._config.getfloat(section, field)
            
        elif retType is list[int]:
            list_vals = self._config.get(section, field).split(',')
            if list_vals != ['']:
                list_vals = list(map(int, list_vals))
            else:
                list_vals = []
            assert func() == list_vals

        elif retType is list[str]:
            list_vals = self._config.get(section, field).split(',')
            if list_vals != ['']:
                list_vals = list(map(str, list_vals))
            else:
                list_vals = []
            assert func() == list_vals

    def verifydevicedata(self, func, device_id, field):
        section = "DeviceInformation" + str(device_id)
        return self.verifydata(func, section, field)

    def verifyprotocoldata(self, func, protocol_id, field):
        section = "ProtocolInformation" + str(protocol_id)
        return self.verifydata(func, section, field)
