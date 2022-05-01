"""Default configuration
"""

# Copyright (c) 2018 Shoppimon LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DEFAULT_BIND_URL = 'tcp://127.0.0.1:5555'

default_config = {
    'logging':  {
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)-15s %(name)-15s %(levelname)s %(message)s'
            }
        },
        'filters': {},
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'stream': 'ext://sys.stderr',
                'formatter': 'default',
                'filters': [],
            }
        },
        'loggers': {},
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
        },
    },
}
