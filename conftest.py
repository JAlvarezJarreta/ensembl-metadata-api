# See the NOTICE file distributed with this work for additional information
#   regarding copyright ownership.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
import logging
from pathlib import Path

import pytest
from _pytest.config import Config

pytest_plugins = ("ensembl.plugins.pytest_unittest",)


def pytest_configure(config: Config) -> None:
    pytest.dbs_dir = Path(__file__).parent / 'src' / 'ensembl' / 'production' / 'metadata' / 'api' / 'sample'
