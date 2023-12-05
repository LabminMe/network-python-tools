# Install pyATS and the Genie parser
# pip install pyats genie

# Investigate Catalyst using pyATS and generating a JSON file
from pyats import aetest
from genie.testbed import load
from pprint import pprint
import json

class DeviceInfoTestcase(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed_name='testbed.yml'):
        self.testbed = load(testbed_name)

    @aetest.test
    def get_device_info(self):
        for device_name, device in self.testbed.devices.items():
            with device.connect(log_stdout=False) as device_conn:
                # Execute CLI command to get device information
                output = device_conn.parse('show version')

                # Extract relevant information
                device_info = {
                    'name': device_name,
                    'firmware_version': output.get('version', {}).get('system_version', 'N/A'),
                    'ip_address': device_conn.find_prompt(),
                    'uptime': output.get('uptime', 'N/A'),
                }

                # Print the information
                pprint(device_info)

                # Export to JSON file
                with open('device_info.json', 'w') as json_file:
                    json.dump(device_info, json_file, indent=4)

if __name__ == '__main__':
    aetest.main()
