# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

#datatest-apps
def run():
    st.set_page_config(
        page_title="Eshows Data",
        page_icon="🎤",
    )

    st.write("# Sprints and data!")

    st.markdown(
        """
        Select an option:
        - Sprint Metrics: upload .csv files to analise the data, files can be generated in our [Scrum Data Dheet](https://docs.google.com/spreadsheets/d/1QHdAKnDqC_1pfwPu89BH1-zxe0Saj8xhqqDfb5nl10Y/edit?usp=sharing)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
